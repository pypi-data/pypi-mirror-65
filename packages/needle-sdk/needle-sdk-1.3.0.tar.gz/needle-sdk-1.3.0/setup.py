import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

packages = ['requests']

setuptools.setup(
    name="needle-sdk",
    version="1.3.0",
    author="Needle.sh team",
    author_email="hello@needle.sh",
    description="Needle.sh SDK for Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://needle.sh",
    install_requires=packages,
    packages= ['needle_sdk'],
    package_data={
        'needle_sdk': ['libinjection2/linux/_libinjection.so', 'libinjection2/linux/libinjection.py',
                        'libinjection2/mac_x86_64/_libinjection.so', 'libinjection2/mac_x86_64/libinjection.py',
                         'js_event_list', 'unix_cmd_list', 'scanners_list']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)