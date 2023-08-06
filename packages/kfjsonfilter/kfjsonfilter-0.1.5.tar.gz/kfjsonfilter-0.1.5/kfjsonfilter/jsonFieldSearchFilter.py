from django.db.models import Q
from django.utils.translation import ugettext as _
from rest_framework import filters
from rest_framework.settings import api_settings
from .utils import to_kwarg


class JsonFieldSearchFilter(filters.BaseFilterBackend):
    """
    Filter that only allows users to see their own objects .
    view. required params:
        json_field = '<data_json_field_name>'
        json_filters = [{'field': <field_name>, 'lookup': <lookup>}, ...]
        search_fields = [{'field': <field_name>, 'lookup': <lookup>}, ...]
    """

    def filter_queryset(self, request, queryset, view):
        filters_json = Q()
        try:
            if view.filter_param:
                pass
        except AttributeError:
            view.filter_param = api_settings.SEARCH_PARAM
        try:
            if view.json_filters:
                pass
        except AttributeError:
            view.json_filters = []
        try:
            if view.search_fields:
                pass
        except AttributeError:
            view.search_fields = []
        try:
            if view.json_field:
                pass
        except AttributeError:
            raise NotImplementedError(_('Must define json_field'))
        for param in request.query_params:
            if param == view.filter_param:
                for jsonQ in view.json_filters:
                    if request.query_params.get(param):
                        if jsonQ.get('lookup') == 'date_range':
                            if len(request.query_params.getlist(param)) == 2:
                                filters_json |= Q(
                                    **to_kwarg('{}__{}'.format(view.json_field, param),
                                               request.query_params.getlist(param)[1], append='__lte')
                                )
                                filters_json |= Q(
                                    **to_kwarg('{}__{}'.format(view.json_field, param),
                                               request.query_params.getlist(param)[0], append='__gte')
                                )
                        else:
                            filters_json |= Q(
                                **to_kwarg('{}__{}'.format(view.json_field, jsonQ.get('field')),
                                           request.query_params.get(param), append='__{}'.format(jsonQ.get('lookup')))
                            )
                for notJsonQ in view.search_fields:
                    if request.query_params.get(param):
                        if notJsonQ.get('lookup') == 'date_range':
                            if len(request.query_params.getlist(param)) == 2:
                                filters_json |= Q(
                                    **to_kwarg(param, request.query_params.getlist(param)[1], append='__lte')
                                )
                                filters_json |= Q(
                                    **to_kwarg(param, request.query_params.getlist(param)[0], append='__gte')
                                )
                        else:
                            filters_json |= Q(
                                **to_kwarg(notJsonQ.get('field'), request.query_params.get(param),
                                           append='__{}'.format(notJsonQ.get('lookup')))
                            )
        return queryset.filter(filters_json)
