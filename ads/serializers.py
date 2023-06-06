from rest_framework import serializers

from ads.models import Ad, Selection, Category
from ads.validators import check_not_published
from users.models import User


class AdCreateAPIViewSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='id', queryset=Category.objects.all())
    author = serializers.SlugRelatedField(slug_field='id', queryset=User.objects.all())
    is_published = serializers.BooleanField(validators=[check_not_published], required=False)

    class Meta:
        model = Ad
        fields = "__all__"


class AdRetrieveViewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'

    )
    category = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Ad
        fields = "__all__"


class AdUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        exclude = ['image']


class AdDestroyView(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = ['id']


class SelectionSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    items = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Selection
        fields = '__all__'


class SelectionCreateSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(slug_field='username', read_only=True)

    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['owner'] = request.user
        return super().create(validated_data)

    class Meta:
        model = Selection
        fields = '__all__'
