from rest_framework.reverse import reverse
from rest_framework.status import HTTP_405_METHOD_NOT_ALLOWED


def test_update_not_allowed(client, ethic_file):
    response = client.put(reverse('ethicfile-detail', kwargs=dict(pk=ethic_file.pk)), data={})

    assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED
