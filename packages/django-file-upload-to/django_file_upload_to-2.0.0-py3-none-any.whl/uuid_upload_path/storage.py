from __future__ import absolute_import, unicode_literals

from pathlib import Path

from uuid_upload_path.uuid import uuid


def upload_to_factory(prefix):
    """
    An upload path generator that uses compact UUIDs for filenames.
    """
    def get_upload_path(instance, filename):
        ext = ''.join(Path(filename).suffixes)
        name_without_ext = filename.replace(ext, '')
        full_name_with_uuid = ''.join([name_without_ext, '_', uuid(), ext])
        return str(Path(prefix, full_name_with_uuid))
    return get_upload_path


def upload_to(instance, filename):
    """
    An upload path generator that generates an upload prefix based
    on the instance model name, and uses a compact UUID for the filename.
    """
    opts = instance._meta
    instance_path = Path(opts.app_label, instance.__class__.__name__.lower())
    return upload_to_factory(instance_path)(instance, filename)
