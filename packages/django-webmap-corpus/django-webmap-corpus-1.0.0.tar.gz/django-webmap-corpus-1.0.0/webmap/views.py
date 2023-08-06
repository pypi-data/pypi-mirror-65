"""Views for the webmap app."""
# from django.views.generic import TemplateView

from django import http
from django.contrib.gis.shortcuts import render_to_kml
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import cache_page, never_cache
from django.views.decorators.gzip import gzip_page

from . import models


@gzip_page
@never_cache              # don't cache KML in browsers
@cache_page(24 * 60 * 60)  # cache in memcached for 24h
def kml_view(request, layer_name):
    # find layer by slug or throw 404
    v = get_object_or_404(models.Layer, slug=layer_name, status__show=True)

    # all enabled pois in this layer
    points = models.Poi.visible.filter(marker__layer=v)
    return render_to_kml(
        "webmap/gis/kml/layer.kml", {
            'places': points,
            'markers': models.Marker.objects.all(),
            'site': get_current_site(request).domain,
        },
    )


def search_view(request, query):
    if len(query) < 3:
        return http.HttpResponseBadRequest('Insufficient query lenght')

    # first by name
    name_qs = models.Poi.visible.filter(Q(name__icontains=query))
    # then by description, address and marker name if not done before
    extra_qs = models.Poi.visible.filter(
        Q(desc__icontains=query) |
        Q(address__icontains=query) |
        Q(marker__name__icontains=query),
    ).exclude(id__in=name_qs)
    # union qs doesn't hold order, so transform to lists and join
    points = list(name_qs) + list(extra_qs)
    return render_to_kml(
        "webmap/gis/kml/layer.kml",
        {
            'places': points,
            'site': get_current_site(request).domain,
        },
    )
