from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings
from rest_framework.routers import SimpleRouter

from .views import RatingViewSet, FavouritesListView, LikeView, SongViewSet


router = SimpleRouter()
router.register('songs', SongViewSet, 'songs')
router.register('ratings', RatingViewSet, 'ratings')

urlpatterns = [
    path('', include(router.urls)),
    path('favourites/', FavouritesListView.as_view()),
    path('liked/', LikeView.as_view())
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)