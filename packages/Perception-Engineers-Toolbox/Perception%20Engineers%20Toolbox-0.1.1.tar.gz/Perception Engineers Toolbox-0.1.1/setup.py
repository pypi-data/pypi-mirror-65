from setuptools import setup
import pathlib
from PerceptionToolkit.Version import version_str

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='Perception Engineers Toolbox',
    version=version_str,
    long_description=README,
    long_description_content_type="text/markdown",
    include_package_data=True,
    packages=['PerceptionToolkit', 'PerceptionToolkit/plugins'],
    url='https://fahren-sie-sicher.de',
    download_url='https://atreus.informatik.uni-tuebingen.de/kuebler/toolbox/-/archive/Release_0.1.1/toolbox-Release_0.1.1.tar.gz',
    license='MIT',
    author='Thomas Kübler',
    author_email='mails@kueblert.de',
    description='A toolbox for eye-tracking data processing and analysis',
    install_requires=["tabel", "yapsy", "numpy", "pyyaml", "pillow", "scipy", "sklearn", "pomegranate", "matplotlib", "pandas", "h5py"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Development Status :: 3 - Alpha",      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ]
)
