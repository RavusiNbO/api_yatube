from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, GroupViewSet
from rest_framework.authtoken import views

router = DefaultRouter()
router.register('posts', PostViewSet)
router.register('groups', GroupViewSet)

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path('', include(router.urls)),
    path('posts/<int:post_id>/comments/', CommentViewSet.as_view({
        'get' : 'list',
        'post' : 'create'
    })),
    path('posts/<int:post_id>/comments/<int:comment_id>/', CommentViewSet.as_view({
        'get' : 'retrieve',
        'put' : 'update',
        'patch' : 'partial_update',
        'delete' : 'destroy'
    }))
]
