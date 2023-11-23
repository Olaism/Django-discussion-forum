from django.utils.text import slugify
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from boards.models import Board

class BoardSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(allow_blank=True, read_only=True)
    
    class Meta:
        model = Board
        fields = ("id", "name", 'description', 'slug')
        validators = [
            UniqueTogetherValidator(
                queryset=Board.objects.all(),
                fields=("name",)
            )
        ]
        
    def update(self, instance, validated_data):
        instance.slug = slugify(validated_data.get('name'))
        return super().update(instance, validated_data)
        







            