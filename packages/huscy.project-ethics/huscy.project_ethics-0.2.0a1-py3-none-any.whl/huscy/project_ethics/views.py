from rest_framework import mixins, viewsets
from rest_framework.permissions import DjangoModelPermissions, IsAuthenticated

from huscy.project_ethics import models, serializer, services


class EthicViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin,
                   viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = services.get_or_create_ethics()
    serializer_class = serializer.EthicSerializer


class EthicBoardViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
                        viewsets.GenericViewSet):
    permission_classes = (DjangoModelPermissions, )
    queryset = services.get_ethic_boards()
    serializer_class = serializer.EthicBoardSerializer


class EthicFileViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin,
                       viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = services.get_ethic_files()
    serializer_class = serializer.EthicFileSerializer


class ProjectViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated, )
    queryset = models.Project.objects.all()
    serializer_class = serializer.ProjectSerializer
