from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN, HTTP_405_METHOD_NOT_ALLOWED


def test_retrieve_is_not_allowed(client, ethic_file):
    response = retrieve_ethic_file(client, ethic_file)

    assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED


def test_admin_user_can_list_ethic_files(admin_client):
    response = list_ethic_files(admin_client)

    assert response.status_code == HTTP_200_OK


def test_user_without_permission_can_list_ethic_file(client):
    response = list_ethic_files(client)

    assert response.status_code == HTTP_200_OK


def test_anonymous_user_cannot_list_ethic_files(anonymous_client):
    response = list_ethic_files(anonymous_client)

    assert response.status_code == HTTP_403_FORBIDDEN


def list_ethic_files(client):
    return client.get(reverse('ethicfile-list'))


def retrieve_ethic_file(client, ethic_file):
    return client.get(reverse('ethicfile-detail', kwargs=dict(pk=ethic_file.id)))
