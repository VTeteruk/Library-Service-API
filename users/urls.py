from rest_framework import routers
from users.views import UserViewSet

router = routers.DefaultRouter()
router.register("me", UserViewSet)

urlpatterns = router.urls

app_name = "users"
