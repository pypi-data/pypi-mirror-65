from django_filters import rest_framework as filters

from huscy.project_ethics import models


class EthicFilter(filters.FilterSet):
    class Meta:
        model = models.Ethic
        fields = (
            'project',
        )
