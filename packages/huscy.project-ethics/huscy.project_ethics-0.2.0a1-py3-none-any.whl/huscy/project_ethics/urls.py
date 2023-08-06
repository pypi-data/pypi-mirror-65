from rest_framework.routers import DefaultRouter

from huscy.project_ethics import views


router = DefaultRouter()
router.register('ethicboards', views.EthicBoardViewSet)
router.register('ethicfiles', views.EthicFileViewSet)
router.register('ethics', views.EthicViewSet, basename='ethic')
router.register('projects', views.ProjectViewSet)
