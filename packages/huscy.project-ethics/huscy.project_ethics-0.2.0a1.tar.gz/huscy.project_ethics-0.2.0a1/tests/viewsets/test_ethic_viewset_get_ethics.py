from rest_framework.reverse import reverse
from rest_framework.status import HTTP_405_METHOD_NOT_ALLOWED


def test_retrieve_ethics_is_not_provided(client, ethic):
    response = client.get(reverse('ethic-detail', kwargs=dict(pk=ethic.pk)))

    assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED


def test_list_ethics_is_not_provided(client):
    response = client.get(reverse('ethic-list'))

    assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED
