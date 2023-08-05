from setuptools import setup, find_packages

setup(
    name='oapi',
    version="0.0.63",
    description=(
        'An SDK for parsing OpenAPI (Swagger) 2.0 - 3.0 specifications'
    ),
    url='https://bitbucket.com/davebelais/oapi.git',
    author='David Belais',
    author_email='david@belais.me',
    license='MIT',
    python_requires='>=3.6, <4',
    keywords='openapi swagger json rest',
    packages=[
        'oapi',
        'oapi.oas'
    ],
    install_requires=[
        "pyyaml>=5.3",
        "iso8601>=0.1.12",
        "sob>=0.2.13",
        "jsonpointer>=2.0"
    ],
    extras_require={
        "dev": [
            "pytest>=5.4.1",
            "tox>=3.14.5",
            "flake8>=3.7.9"
        ],
        "test": [
            "pytest>=5.4.1",
            "tox>=3.14.5",
            "flake8>=3.7.9"
        ]
    }
)
