from rest_framework import serializers

from .models import Rating, Favourite, Song, Like, Genre


class SongListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'


class SongListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['likes'] = instance.likes.count()
        return rep





class SongDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Song
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['like'] = instance.likes.count()
        return rep


class CreateSongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        exclude = ('user', )

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        if request.user.is_anonymous:
            raise serializers.ValidationError('Can create only authorized user')
        return super().create(validated_data)





class SongDetailSerializer(serializers.ModelSerializer):
    song = SongListSerializer(many=True, read_only=True)

    class Meta:
        model = Song
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    """Like analitic"""

    class Meta:
        model = Like
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    song = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Song.objects.all())
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Rating
        fields = ('id', 'rate', 'song', 'user', )

    def validate(self, attrs):
        song = attrs.get('song')
        request = self.context.get('request')
        user = request.user
        if Rating.objects.filter(song=song, user=user).exists():
            raise serializers.ValidationError('Impossible to rate twice')
        return attrs

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['user'] = request.user
        return super().create(validated_data)


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

    def get_genre(self, obj):
        if obj.genre:
            return obj.genre
        return ''

class FavouriteMusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        fields = '__all__'

        def get_favourite(self, obj):
            if obj.favourite:
                return obj.favourite
            return ''

        def to_representation(self, instance):
            rep = super().to_representation(instance)
            rep['favourite'] = self.get_favourite(instance)
            return rep