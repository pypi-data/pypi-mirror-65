import pytest
import json

from rest_framework.reverse import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN

pytestmark = pytest.mark.django_db


def test_admin_user_can_create_ethic(admin_client, ethic_board, project):
    response = create_ethic(admin_client, ethic_board, project)

    assert response.status_code == HTTP_201_CREATED


def test_user_without_permission_can_create_ethic(django_db_reset_sequences, client, ethic_board,
                                                  project):
    response = create_ethic(client, project, ethic_board)

    assert response.status_code == HTTP_201_CREATED, json.dumps(response.json(),
                                                                indent=4,
                                                                sort_keys=True)


def test_anonymous_user_cannot_create_ethic(anonymous_client, project, ethic_board):
    response = create_ethic(anonymous_client, project, ethic_board)

    assert response.status_code == HTTP_403_FORBIDDEN


def create_ethic(client, ethic_board, project):
    data = dict(
        code='123/12-ek',
        ethic_board=ethic_board.id,
        project=project.id,
    )
    return client.post(reverse('ethic-list'), data=data)
