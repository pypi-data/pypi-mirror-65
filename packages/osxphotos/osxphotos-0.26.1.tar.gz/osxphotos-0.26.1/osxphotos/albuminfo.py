"""
AlbumInfo class
Represents a single Album in the Photos library and provides access to the album's attributes
PhotosDB.albums() returns a list of AlbumInfo objects
"""


class AlbumInfo:
    """
    Info about a specific Album, contains all the details about the album
    including folders, photos, etc.
    """

    def __init__(self, db=None, uuid=None):
        self._uuid = uuid
        self._db = db
        self._name = self._db._dbalbum_details[uuid]["title"]

    @property
    def name(self):
        return self._name

    @property
    def uuid(self):
        return self._uuid

    @property
    def photos(self):
        uuid = self._db._dbalbums_album[self._uuid]
        print(f"uuid = {uuid}")
        return self._db.photos(uuid=uuid)
