import pytest
from rest_framework import status

from ads.serializers import AdListSerializer, AdRetrieveViewSerializer
from tests.factories import AdFactory


@pytest.mark.django_db
def test_ad_list(client):
    ad_list = AdFactory.create_batch(4)
    response = client.get('/ad/')

    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        "count": 4,
        "next": None,
        "previous": None,
        "results": AdListSerializer(ad_list, many=True).data
    }


@pytest.mark.django_db
def test_ad_retrieve(client, access_token):
    ad = AdFactory.create()
    response = client.get(f'/ad/{ad.pk}/', HTTP_AUTHORIZATION=f"Bearer {access_token}")
    assert response.status_code == status.HTTP_200_OK
    assert response.data == AdRetrieveViewSerializer(ad).data


@pytest.mark.django_db
def test_ad_create(client, user, category):
    data = {
        'author': user.username,
        'category': category.name,
        'name': 'Название из 10 символов',
        'price': 313
    }

    expected_data = {
        "id": 1,
        "category": category.name,
        "author": user.username,
        "is_published": False,
        "name": "Название из 10 символов",
        "price": 313,
        "description": None,
        "image": None
    }

    response = client.post("/ad/create/", data=data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == expected_data
