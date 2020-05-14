from django.conf.urls import url,include
from rest_framework.routers import DefaultRouter
from . import views
from mytestproj import settings

def get_media_root():
    return settings.MEDIA_ROOT

routers = DefaultRouter()
routers.APIRootView = views.RootView
routers.register(r'teststep',views.TeststepViewSet)
routers.register(r'testcase',views.TestCaseViewSet)
routers.register(r'testsuite',views.TestSuiteViewSet)
routers.register(r'testreport',views.TestReportViewSet)
routers.register(r'users', views.UserViewSet)

urlpatterns = [
    url(r'^',include(routers.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]