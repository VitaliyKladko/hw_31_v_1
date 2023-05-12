from rest_framework import serializers

from users.models import Location, User


class UserListViewSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = User
        exclude = ['password']


class UserRetrieveViewSerializer(serializers.ModelSerializer):
    locations = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = User
        exclude = ['password']


class UserCreateAPIViewSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    locations = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Location.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = User
        fields = '__all__'

    def is_valid(self, *, raise_exception=False):
        self._location = self.initial_data.pop('locations')
        return super().is_valid(raise_exception=raise_exception)

    def create(self, validated_data):
        user = User.objects.create(**validated_data)

        for loc_name in self._location:
            loc, _ = Location.objects.get_or_create(name=loc_name)
            user.locations.add(loc)
        user.save()
        return user


class UserUpdateAPIViewSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    locations = serializers.SlugRelatedField(
        required=False,
        many=True,
        queryset=Location.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = User
        fields = "__all__"

    def is_valid(self, *, raise_exception=False):
        self._location = self.initial_data.pop('locations')
        return super().is_valid(raise_exception=raise_exception)

    def save(self, **kwargs):
        user = super().save()

        for loc_name in self._location:
            loc_obj, _ = Location.objects.get_or_create(name=loc_name)
            user.locations.clear()
            user.locations.add(loc_obj)
        user.save()
        return user


class UserDestroyAPIViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id']


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'
