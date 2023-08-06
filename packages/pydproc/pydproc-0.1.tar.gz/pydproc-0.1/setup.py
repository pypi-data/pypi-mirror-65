from setuptools import setup, find_packages

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='pydproc',
    version='0.1',
    description='A useful module',
    license="MIT",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Vladimir Oveckin, Robert Burris, Andrew Wu',
    author_email='vladov3000@gmail.com',
    url="https://github.com/vladov3000/pydproc",
    install_requires=['pyyaml', 'click', 'docker'],  # external packages as dependencies
    packages=find_packages(),
    package_data={'pydproc': ['docker_base/*']},
    entry_points='''
        [console_scripts]
        pydproc=pydproc.scripts.cli:pydproc
   '''
)
