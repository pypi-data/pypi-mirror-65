from model_bakery import baker

from rest_framework.reverse import reverse

from huscy.project_ethics.serializer import EthicSerializer


def test_projects_with_existing_ethics(client, project):
    ethics = baker.make('project_ethics.Ethic', project=project, _quantity=1)

    response = retrieve_project(client, project)

    result = response.json()
    assert result['ethics'] == EthicSerializer(ethics, many=True).data


def test_projects_with_not_existing_ethics(client, project):
    response = retrieve_project(client, project)

    result = response.json()
    assert len(result['ethics']) == 1
    assert result['ethics'][0]['project'] == project.id


def retrieve_project(client, project):
    return client.get(reverse('project-detail', kwargs=dict(pk=project.pk)))
