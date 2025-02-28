from django.shortcuts import render
from posts import models
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from . import serializers
# Create your views here.


class PostViewSet(ModelViewSet):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        post = models.Post.objects.get(pk=self.kwargs.get('post_id'))
        if self.request.user != post.author:
            return Response(serializer.data, status=status.HTTP_403_FORBIDDEN)
        serializer.save(data=self.request.data, instance=post)

class GroupViewSet(ReadOnlyModelViewSet):
    queryset = models.Group.objects.all()
    serializer_class = serializers.GroupSerializer




class CommentViewSet(ModelViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer



    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=models.Post.objects.get(pk=self.kwargs.get('post_id')))

    def perform_update(self, serializer):
        serializer.save(author=self.request.user)