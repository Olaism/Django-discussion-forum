from .permissions import IsStaffOrReadOnly

class IsStaffOrReadOnlyMixins():
    serializer_class = [IsStaffOrReadOnly]