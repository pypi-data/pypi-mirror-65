from setuptools import setup

setup(
    name="irma-shared",
    version="3.3.0",
    author="irma-dev",
    author_email="irma-dev@quarkslab.com",
    description="Objects and well-known values used by the IRMA software",
    packages=(
        "irma.shared",
        "irma.shared.schemas",
    ),
    package_dir={
        "irma.shared": "src",
    },
    namespace_packages=(
        "irma",
    ),
    install_requires=(
        'marshmallow==3.3.0',
        'marshmallow_enum==1.5.1',
    ),
    test_suite='nose.collector',
    tests_require=(
        'nose',
    )
)
