

from django_filters import rest_framework as rest_filter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import views, filters, mixins, viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.viewsets import GenericViewSet


from .models import Like, Rating, Favourite, Song, Genre
from .serializers import (CreateSongSerializer, SongListSerializer, SongDetailSerializer, RatingSerializer,
                          FavouriteMusicSerializer, LikeSerializer, GenreSerializer)
from .permissions import IsAdminUser, IsAuthor, IsAuthorOrIsAdmin


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return SongListSerializer
        elif self.action == 'retrieve':
            return SongDetailSerializer
        return CreateSongSerializer

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return []
        return [IsAdminUser()]


class SongFilter(rest_filter.FilterSet):
    created_at = rest_filter.DateTimeFromToRangeFilter()

    class Meta:
        model = Song
        fields = ('title', 'artist', 'created_at',)


class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = CreateSongSerializer
    filter_backends = [
        rest_filter.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    search_fields = ['title', 'artist', ]
    ordering_fields = ['description', 'title', ]

    def get_serializer_class(self):
        if self.action == 'list':
            return SongListSerializer
        elif self.action == 'retrieve':
            return SongDetailSerializer
        return CreateSongSerializer

    @action(['POST'], detail=True)
    def like(self, request, pk=None):
        song = self.get_object()
        user = request.user
        try:
            like = Like.objects.get(song=song, user=user)
            like.is_liked = not like.is_liked
            if like.is_liked:
                like.save()
            else:
                like.delete()
            message = 'like' if like.is_liked else 'dislike'
        except Like.DoesNotExist:
            Like.objects.create(song=song, user=user, is_liked=True)
            message = 'liked'
        return Response(message, status=200)

    @action(['POST'], detail=True)
    def favourite(self, request, pk=None):
        song = self.get_object()
        user = request.user
        try:
            favourite = Favourite.objects.get(song=song, user=user)
            favourite.is_favourite = not favourite.is_favourite
            if favourite.is_favourite:
                favourite.save()
            else:
                favourite.delete()
            message = 'added to favourites' if favourite.is_favourite else 'deleted in favourites'
        except Favourite.DoesNotExist:
            Favourite.objects.create(song=song, user=user, is_favourite=True)
            message = 'added to favourites'
        return Response(message, status=200)

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve':
            return []
        elif self.action == 'create' or self.action == 'like' or self.action == 'favourite':
            return [IsAuthenticated()]
        return [IsAuthorOrIsAdmin()]


class SongViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    GenericViewSet):
    queryset = Song.objects.all()
    serializer_class = SongListSerializer
    permission_classes = [IsAuthorOrIsAdmin]


class SongViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows songs to be viewed or edited.
    """
    queryset = Song.objects.all()
    serializer_class = SongListSerializer

class SongViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows songs to be viewed or edited.
    """
    queryset = Song.objects.all()
    serializer_class = SongDetailSerializer







class RatingViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    GenericViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        return [IsAuthor()]


class GenreViewSet(mixins.CreateModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   GenericViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return []


class FavouritesListView(ListAPIView):
    permission_classes = [IsAuthor]
    serializer_class = FavouriteMusicSerializer

    def get_queryset(self):
        user = self.request.user
        return Favourite.objects.filter(user=user)


class LikeView(ListAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['song']

class LikeViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    GenericViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated()]
        return [IsAuthor()]

