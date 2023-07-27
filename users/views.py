from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer

    def get_object(self) -> User:
        return get_user_model().objects.get(id=self.request.user.id)
