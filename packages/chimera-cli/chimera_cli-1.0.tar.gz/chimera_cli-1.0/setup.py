import setuptools
with open('README.md') as fp:
    big_description = fp.read()
setuptools.setup(
    name='chimera_cli',
    version='1.0',
    scripts=['./scripts/chimera'],
    author='Me',
    description='Command line interface for chimera',
    long_description=big_description,
    long_description_content_type='text/markdown',
    packages=['chimera_cli'],
    install_requires=[
        'setuptools',
        'requests',
        'pyyaml',
        'avro-python3',
        'docker',
        'git-python',
        'watchdog'
    ],
    python_requires='>=3.6'
)
