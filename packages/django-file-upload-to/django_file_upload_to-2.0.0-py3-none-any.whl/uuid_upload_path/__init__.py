"""
Generate short UUIDs and use them as paths
for uploaded media files in Django.
"""


__version__ = (2, 0, 0)


from uuid_upload_path.uuid import uuid
from uuid_upload_path.storage import upload_to_factory, upload_to
