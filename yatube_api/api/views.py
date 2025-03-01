from posts import models
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.exceptions import PermissionDenied
from . import serializers

# Create your views here.


class PostViewSet(ModelViewSet):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_update(self, serializer):
        post = (
            self.get_object()
        )
        if self.request.user != post.author:
            raise PermissionDenied(
                "You do not have permission to edit this post."
            )

        serializer.save(instance=post)

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        if self.request.user != post.author:
            raise PermissionDenied(
                "You do not have permission to edit this post."
            )

        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupViewSet(ReadOnlyModelViewSet):
    queryset = models.Group.objects.all()
    serializer_class = serializers.GroupSerializer


class CommentViewSet(ModelViewSet):
    queryset = models.Comment.objects.all()
    serializer_class = serializers.CommentSerializer

    def retrieve(self, request, *args, **kwargs):
        comment = self.get_object()
        post = get_object_or_404(
            models.Post,
            pk=self.kwargs.get("post_id")
        )
        if post is not None:
            serializer = self.get_serializer(comment)
            return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            post=models.Post.objects.get(
                pk=self.kwargs.get("post_id")
            ),
        )

    def perform_update(self, serializer):
        comment = self.get_object()
        if comment.author != self.request.user:
            raise PermissionDenied(
                "You do not have permission to edit this post."
            )
        serializer.save(instance=comment)

    def destroy(self, request, *args, **kwargs):
        comment = self.get_object()
        if comment.author != self.request.user:
            raise PermissionDenied(
                "You do not have permission to edit this post."
            )
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
