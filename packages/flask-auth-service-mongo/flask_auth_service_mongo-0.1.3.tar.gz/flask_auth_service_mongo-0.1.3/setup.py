import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flask_auth_service_mongo",
    version="0.1.3",
    author="Terminus",
    author_email="mateo.chaparro@zinobe.com",
    description="Flask JWT authentication package with mongo.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/terminus-zinobe/flask-auth-service-mongo",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'bcrypt>=3,<4',
        'Cerberus>=1.3,<2',
        'flask>=1,<2',
        'PyJWT>=1.7,<2',
        'mongoengine>=0.18,<0.19',
        'radon>=4,<5',
        'graphene>=2.1,<3',
        'graphene-mongo>=0.2,<0.3',
    ]
)
