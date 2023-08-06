import pytest

from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_403_FORBIDDEN


def test_admin_user_can_retrieve_project(admin_client, project):
    response = retrieve_project(admin_client, project)

    assert response.status_code == HTTP_200_OK


def test_user_without_permission_can_retrieve_project(client, project):
    response = retrieve_project(client, project)

    assert response.status_code == HTTP_200_OK


@pytest.mark.django_db
def test_anonymous_user_cannot_retrieve_project(anonymous_client, project):
    response = retrieve_project(anonymous_client, project)

    assert response.status_code == HTTP_403_FORBIDDEN


def retrieve_project(client, project):
    return client.get(reverse('project-detail', kwargs=dict(pk=project.pk)))
