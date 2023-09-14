from setuptools import setup, find_packages

setup(
    name="HPE-Ezmeral-Software-ToolBox",
    version="2.2",
    packages=find_packages(),
    author="Treo Information Technologies",
    author_email="datascience@treo.com.tr",
    description="HPE Ezmeral Software ToolBox is a collection of tools for HPE Ezmeral Data Fabric.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    license="LICENSE",
    url="https://github.com/msaidbilgehan/HPE-Ezmeral-Software-ToolBox",
    entry_points={
        'console_scripts': [
            'flask_app = Flask_App.flask_app:main',
            # You can add other entry points if needed
        ],
    },
    classifiers=[
        # Add any relevant classifiers here
        "Programming Language :: Python",
        "License :: Custom :: Custom License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        # Add any dependencies here, for example:
        # 'flask',
        'flask',
        'Jinja2',
        'dnspython',
        'paramiko',
    ],
    include_package_data=True,
)
