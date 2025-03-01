from rest_framework import serializers
from posts import models


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    image = serializers.ImageField(required=False)
    pub_date = serializers.DateTimeField(read_only=True)

    class Meta:
        model = models.Post
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    created = serializers.DateTimeField(read_only=True)

    class Meta:
        model = models.Comment
        fields = "__all__"


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Group
        fields = "__all__"
