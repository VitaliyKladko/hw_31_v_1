import pytest
from rest_framework import status

from tests.factories import AdFactory


@pytest.mark.django_db
def test_selection_create(client, access_token):
    ad_list = AdFactory.create_batch(4)
    data = {
        "name": "Подборка",
        "items": [ad.pk for ad in ad_list]
    }

    expected_data = {
        "id": 1,
        "owner": "test",
        "name": "Подборка",
        "items": [ad.pk for ad in ad_list]
    }

    response = client.post("/selection/", data=data, HTTP_AUTHORIZATION=f"Bearer {access_token}")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data == expected_data
