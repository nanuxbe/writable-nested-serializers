from rest_framework import viewsets

from .models import Human
from .serializers import HumanSerializer


class HumanViewSet(viewsets.ModelViewSet):

    queryset = Human.objects.all()
    serializer_class = HumanSerializer
