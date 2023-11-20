from django.utils.text import slugify
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from boards.models import Board

class BoardSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(allow_blank=True)
    
    class Meta:
        model = Board
        fields = ("id", "name", 'description', 'slug')
        validators = [
            UniqueTogetherValidator(
                queryset=Board.objects.all(),
                fields=("name",)
            )
        ]
        







            