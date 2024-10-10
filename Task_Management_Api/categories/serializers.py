from rest_framework import serializers

from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    """
    CategorySerializer is a ModelSerializer for the Category model.

    Fields:
        - id: Integer, read-only
        - name: String
    """

    class Meta:
        model = Category
        fields = ["id", "name"]
        read_only_fields = ["id"]