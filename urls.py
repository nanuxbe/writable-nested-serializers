from django.conf.urls import include, url
from django.contrib import admin

from rest_framework import routers

from sample.views import HumanViewSet


router = routers.DefaultRouter()
router.register(r'humans', HumanViewSet)

urlpatterns = [
    # Examples:
    # url(r'^$', 'restframework_writable_nested.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/v1/', include(router.urls)),
]
