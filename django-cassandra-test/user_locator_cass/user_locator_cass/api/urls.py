from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from user_locator_cass.api.views import AccountViewSet, AdminTokenViewSet, UserLocatorViewSet

urlpatterns = [
    url(r'^login/', obtain_jwt_token),
    url(r'^token-refresh/', refresh_jwt_token),
    url(r'^token-verify/', verify_jwt_token),
    url(r'token/$', AdminTokenViewSet.as_view()),
    #url(r'chung/(?P<pk>[0-9]+)/$', UserLocatorViewSet.as_view()),
    url(r'user/(?P<pk>[0-9]+)/$', UserLocatorViewSet.as_view()),
]

router = DefaultRouter()
router.register(r'account', AccountViewSet, base_name='account')
urlpatterns += router.urls

