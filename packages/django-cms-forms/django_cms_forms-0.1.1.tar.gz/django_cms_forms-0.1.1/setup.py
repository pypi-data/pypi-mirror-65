import os

import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

with open("cms_forms/__init__.py", "r") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.strip().split("=")[1].strip(" '\"")
            break
    else:
        version = "0.0.1"

    patch = os.environ.get("PATCH_VERSION")
    if patch:
        version = f"{version}.{patch}"

with open("requirements.txt") as f:
    _requirements = [line.split("#")[0].strip() for line in f]
    install_requires = [req for req in _requirements if req and not req.startswith("-r")]


setuptools.setup(
    name="django_cms_forms",
    version=version,
    author="Szymon Zmilczak",
    author_email="szymon.zmilczak@gmail.com",
    maintainer="Szymon Zmilczak",
    maintainer_email="szymon.zmilczak@gmail.com",
    description="Set of Django CMS plugins for creating forms",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sim1234/cms_forms",
    license="MIT",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    keywords=["django", "django cms", "cms", "forms"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        # "Framework :: Django CMS",
        # "Framework :: Django CMS :: 3.7",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
