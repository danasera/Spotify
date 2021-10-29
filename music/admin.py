from django.contrib import admin

from django.contrib import admin

from music.models import Song, Rating, Like, Favourite, Genre


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ['title', 'artist', 'album', 'duration', ]
    list_filter = ['title', 'artist']
    search_fields = ['title', 'artist']
    prepopulated_fields = {'artist': ('title',)}

admin.site.register(Rating)
admin.site.register(Like)
admin.site.register(Favourite)
admin.site.register(Genre)
