from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
#OKR
router.register(r'log', views.LogViewSet, basename='log')
router.register(r'source', views.SourceViewSet, basename='source')
router.register(r'formula', views.FormulaViewSet, basename='formula')
router.register(r'objective', views.ObjectiveViewSet, basename='objective')
router.register(r'okr', views.OkrViewSet, basename='okr')
#Employee
router.register(r'employee', views.EmployeeViewSet, basename='employee')
router.register(r'team', views.TeamViewSet, basename='team')
router.register(r'department', views.DepartmentViewSet, basename='department')




urlpatterns = [
    #path('okr/get', views.get_okr, name='get-okr'),
    path('', include(router.urls)),
    # path('', views.home.as_view),
    # path('update', views.create_okr)
]