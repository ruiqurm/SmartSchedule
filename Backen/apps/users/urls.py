from django.urls import path,re_path
from django.conf.urls import url,include
from apps.users.views import OrgViewset
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
#router.register(r'friend',FriendViewset,basename="friend")
router.register(r'org',OrgViewset,basename='organization')
urlpatterns = [
    url(r"^",include(router.urls)),
]