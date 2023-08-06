from __future__ import absolute_import, unicode_literals

from unittest import TestCase

from uuid_upload_path.uuid import uuid
from uuid_upload_path.storage import upload_to_factory, upload_to


class UuidTest(TestCase):

    # It's hard to test random data, but more iterations makes the tests
    # more robust.
    TEST_ITERATIONS = 1000

    def testUuidFormat(self):
        for _ in range(self.TEST_ITERATIONS):
            self.assertRegex(uuid(), r"^[a-zA-Z0-9\-_]{22}$")

    def testUuidUnique(self):
        generated_uuids = set()
        for _ in range(self.TEST_ITERATIONS):
            new_uuid = uuid()
            self.assertNotIn(new_uuid, generated_uuids)
            generated_uuids.add(new_uuid)


class TestModel(object):

    class _meta:
        app_label = "test"


class StorageTest(TestCase):

    def testUploadToFactory(self):
        uploaded_file = upload_to_factory("test")(object(), "test.txt.gzip")
        regex_file = r"^test/test_[a-zA-Z0-9\-_]{22}.txt.gzip$"
        self.assertRegex(uploaded_file, regex_file)

    def testUploadTo(self):
        uploaded_file = upload_to(TestModel(), "test.txt.gzip")
        regex_file = r"^test/testmodel/test_[a-zA-Z0-9\-_]{22}.txt.gzip$"
        self.assertRegex(uploaded_file, regex_file)
