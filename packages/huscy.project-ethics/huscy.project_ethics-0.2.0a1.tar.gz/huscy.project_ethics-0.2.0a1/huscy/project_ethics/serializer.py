from rest_framework import serializers

from huscy.project_ethics import models, services


class EthicBoardSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EthicBoard
        fields = (
            'id',
            'name',
        )


class EthicSerializer(serializers.ModelSerializer):
    ethic_board_name = serializers.SerializerMethodField()
    ethic_files = serializers.SerializerMethodField()

    class Meta:
        model = models.Ethic
        fields = (
            'code',
            'ethic_board',
            'ethic_board_name',
            'ethic_files',
            'id',
            'project',
        )

    def get_ethic_board_name(self, ethic):
        return ethic.ethic_board and ethic.ethic_board.name

    def get_ethic_files(self, ethic):
        return EthicFileSerializer(ethic.ethicfile_set.all(), many=True).data


class EthicFileSerializer(serializers.ModelSerializer):
    filetype_name = serializers.SerializerMethodField()

    class Meta:
        model = models.EthicFile
        fields = (
            'ethic',
            'filehandle',
            'filename',
            'filetype',
            'filetype_name',
            'uploaded_at',
            'uploaded_by',
        )
        read_only_fields = 'filename',

    def get_filetype_name(self, ethic_file):
        return ethic_file.get_filetype_display()

    def create(self, validated_data):
        creator = self.context.get('request').user
        return services.create_ethic_file(**validated_data, creator=creator)


class ProjectSerializer(serializers.ModelSerializer):
    ethics = serializers.SerializerMethodField()

    class Meta:
        model = models.Project
        fields = (
            'id',
            'ethics',
        )

    def get_ethics(self, project):
        ethics = services.get_or_create_ethics(project)
        return EthicSerializer(ethics, many=True).data
