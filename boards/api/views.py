from rest_framework import generics

from .mixins import IsStaffOrReadOnlyMixins
from ..models import Board
from .serializers import BoardSerializer


class BoardListCreateAPIView(IsStaffOrReadOnlyMixins, generics.ListCreateAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer

class BoardRetrieveUpdateDestroyAPIView(IsStaffOrReadOnlyMixins, generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardSerializer
    lookup_field = "slug"