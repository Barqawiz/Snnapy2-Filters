from setuptools import setup, find_packages
import os

with open("PIPREADME.md", "r") as fh:
    long_description = fh.read()

def get_resources():
    resources = []
    for root, dirs, files in os.walk('snappy2/resource'):
        resources.extend([os.path.join(root, f) for f in files])
    return resources

resources = get_resources()
# print(resources)

setup(
    name='snappy2',
    version='0.3',
    author='Albarqawi',
    packages=find_packages(),
    include_package_data=True,
    url='https://snappy2.ahmadai.com/',
    description="Detect faces and draw overlay images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[ 'opencv-python==3.4.18.65', 'Pillow==9.4.0', 'tensorflow==2.9.0', 'keras==2.9.0', 'numpy==1.24.1', 'Markdown==3.4.1', 'absl-py==1.4.0', 'Werkzeug==2.2.2', 'h5py==3.1.0'    ],
    data_files=[('snappy2/resource', resources)]
)
