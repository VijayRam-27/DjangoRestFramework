from rest_framework import serializers
from .models import Posts


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Posts
        fields = ["id", "post_title", "post_description"]