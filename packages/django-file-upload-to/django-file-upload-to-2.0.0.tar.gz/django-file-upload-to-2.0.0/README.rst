django-file-upload-to
=======================

**django-file-upload-to** generates short UUIDs to use as paths for uploaded media files in Django.


Features
--------

-  Generate short (22 character), URL-safe base64-encoded UUIDs.
-  Upload media files to short UUID filenames.


Installation
------------

1. Checkout the latest django-file-upload-to release and copy or symlink the
   ``uuid_upload_path`` directory into your ``PYTHONPATH``.  If using pip, run 
   ``pip install django-file-upload-to``.


Generating short UUIDs
----------------------

Generate a short, URL-safe UUID as follows:

::

    from uuid_upload_path import uuid

    uuid()  // -> "hCdLEjlQQJW25-sXB3T_Gw"



Generating upload paths
-----------------------

To upload media files to short UUID filenames, just set `upload_to` to `uuid_upload_path.upload_to`.

::

    from uuid_upload_path import upload_to

    class YourModel(models.Model):

        file = models.FileField(
            upload_to = upload_to,
        )


Why use UUIDs as upload paths?
------------------------------

Django tries to ensure that all your uploaded files are given unique names on the filesystem. It does this by checking if a file with the same name exists before saving a new one, and adding a suffix if the new file would otherwise conflict with the existing one.

If you're saving files to disk using the built-in ``django.core.files.storage.FileSystemStorage``, this isn't much of a problem. However, if you're using a cloud file storage, such as ``storages.backends.s3boto.S3BotoStorage``, this uniqueness check can have a noticeable effect on the performance of file uploads. Worse, the default configuration of `S3BotoStorage` is to overwrite existing files with the same name when uploading a new file!

By generating a unique filename for each uploaded file, django-file-upload-to removes the need for a costly uniqueness check, and avoids accidentally overwriting existing files on remote cloud storages.


Support and announcements
-------------------------

Downloads and bug tracking can be found at the `main project
website <https://github.com/panttojo/django-file-upload-to>`_.


More information
----------------

The django-uuid-upload-path project was developed by Dave Hall and forked for make a little customizations.
You can get the code from the `django-uuid-upload-path project
site <https://github.com/etianen/django-uuid-upload-path>`_.
