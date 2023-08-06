from rest_framework.metadata import BaseMetadata


class ScrudMetadata(BaseMetadata):

    def determine_metadata(self, request, view):
        ...
