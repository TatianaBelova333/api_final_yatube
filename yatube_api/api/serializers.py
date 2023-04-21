import base64

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.core.files.base import ContentFile


from posts.models import Comment, Follow, Group, Post, User


class Base64ImageField(serializers.ImageField):
    """
    ImageField that takes base64 image as a string,
    saves the image as a file and returns the file path.

    """
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(
                base64.b64decode(imgstr),
                name='images/temp.' + ext,
            )
        return super().to_internal_value(data)


class PostSerializer(serializers.ModelSerializer):
    """Serializer for the Post model."""
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )
    image = Base64ImageField(required=False, allow_null=True)

    class Meta:
        model = Post
        fields = (
            'id',
            'text',
            'pub_date',
            'author',
            'image',
            'group',
        )
        read_only_fields = ('id', 'pub_date')


class GroupSerializer(serializers.ModelSerializer):
    """Serializer for the Group model."""

    class Meta:
        model = Group
        fields = ('id', 'title', 'slug', 'description')


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for the Comment model."""
    author = serializers.StringRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
        read_only_fields = ('id', 'created', 'post')


class FollowSerializer(serializers.ModelSerializer):
    """Serializer for the Follow model."""
    user = serializers.StringRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        required=True,
    )

    class Meta:
        model = Follow
        fields = ('user', 'following')
        validators = [
            UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('user', 'following'),
            )
        ]

    def validate(self, data):
        """
        Raise ValidationError if the user and the following fields
        are the same.

        """
        request = self.context.get("request")
        user = request.user
        following = data.get('following')
        if user == following:
            raise serializers.ValidationError(
                detail={'following': 'Request user cannot follow himself.'}
            )
        return data
