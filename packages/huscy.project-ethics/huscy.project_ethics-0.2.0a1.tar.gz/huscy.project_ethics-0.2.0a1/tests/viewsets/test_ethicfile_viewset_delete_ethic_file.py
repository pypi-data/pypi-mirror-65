import pytest

from rest_framework.reverse import reverse
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN

pytestmark = pytest.mark.django_db


def test_admin_user_can_delete_ethic_files(admin_client, ethic_file):
    response = delete_ethic_file(admin_client, ethic_file)

    assert response.status_code == HTTP_204_NO_CONTENT


def test_user_without_permission_can_delete_ethic_files(client, ethic_file):
    response = delete_ethic_file(client, ethic_file)

    assert response.status_code == HTTP_204_NO_CONTENT


def test_anonymous_user_cannot_delete_ethic_files(anonymous_client, ethic_file):
    response = delete_ethic_file(anonymous_client, ethic_file)

    assert response.status_code == HTTP_403_FORBIDDEN


def delete_ethic_file(client, ethic_file):
    return client.delete(reverse('ethicfile-detail', kwargs=dict(pk=ethic_file.pk)))
