import pytest

from tests.factories import UserFactory


@pytest.fixture
@pytest.mark.django_db
def access_token(client, django_user_model):
    username = 'test'
    password = 'qwe123'
    django_user_model.objects.create_user(username=username, password=password)
    response = client.post('/user/token/', data={"username": username, "password": password})
    return response.data.get('access')
