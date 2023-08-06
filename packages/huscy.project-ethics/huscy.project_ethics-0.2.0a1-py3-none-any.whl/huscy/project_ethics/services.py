from huscy.project_ethics.filters import EthicFilter
from huscy.project_ethics.models import Ethic, EthicBoard, EthicFile


def create_ethic_file(ethic, filehandle, filetype, creator):
    filename = filehandle.name.split('/')[-1]

    return EthicFile.objects.create(
        ethic=ethic,
        filehandle=filehandle,
        filename=filename,
        filetype=filetype,
        uploaded_by=creator.get_full_name(),
    )


def get_ethic_files():
    return EthicFile.objects.all()


def get_or_create_ethics(project=None):
    queryset = Ethic.objects.order_by('pk')
    if project is not None:
        filters = dict(project=project.pk)
        filtered_queryset = EthicFilter(filters, queryset).qs
        if not filtered_queryset.exists():
            Ethic.objects.create(project=project)
        return filtered_queryset
    return queryset


def get_ethic_boards():
    return EthicBoard.objects.all()
