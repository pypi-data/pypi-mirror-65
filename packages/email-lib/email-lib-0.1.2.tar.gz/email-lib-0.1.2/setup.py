from setuptools import setup, find_packages

def get_requirements():
    try:
        with open('./requirements.txt') as handle:
            return handle.readlines()
    except:
        pass

setup(
    name="email-lib",
    version="0.1.2",
    author="Pierre Wacrenier",
    author_email="pierre@wacrenier.me",
    description="Simplify email organization",
    url="https://github.com/mota/email-lib",
    install_requires=get_requirements(),
    packages=find_packages(),
    license='MIT',

    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
)
