from setuptools import setup

from uuid_upload_path import __version__


version_str = ".".join(str(n) for n in __version__)


with open("README.rst", "r") as fh:
    long_description = fh.read()


setup(
    name="django-file-upload-to",
    version=version_str,
    license="BSD",
    description="Generate short UUIDs and use them as paths for uploaded media files in Django.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Daniel Pantoja",
    author_email="panttojo@yandex.com",
    url="https://github.com/panttojo/django-file-upload-to",
    packages=[
        "uuid_upload_path",
    ],
    test_suite="uuid_upload_path.tests",
    zip_safe=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet :: WWW/HTTP",
    ],
    python_requires='>=3.4',
)
