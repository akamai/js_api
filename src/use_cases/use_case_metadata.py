from src.metadata.metadata_vt import MetadataVT
from src.metadata.metadata_publicwww import MetadataPublicWWW

METADATA = [MetadataVT, MetadataPublicWWW]


class UseCaseMetadata(object):
    """
    Use case for metadata. Modify this file if you want to add a new metadata component
    """

    @staticmethod
    def get_metadata_list():
        return [metadata.NAME for metadata in METADATA]

    @staticmethod
    def get_metadata(name):
        """
        Add your metadata here to "plug it"
        Args:
            name: metadata name

        Returns: metadata object

        """
        name = name.lower()
        if name == MetadataVT.NAME.lower():
            return MetadataVT
        elif name == MetadataPublicWWW.NAME.lower():
            return MetadataPublicWWW
        return None
