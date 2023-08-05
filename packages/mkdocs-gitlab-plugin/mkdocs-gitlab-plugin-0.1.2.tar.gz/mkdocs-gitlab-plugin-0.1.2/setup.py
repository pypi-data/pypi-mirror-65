
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as fh:
    requires = [line.strip() for line in fh]

setuptools.setup(
    name='mkdocs-gitlab-plugin',
    version='0.1.2',
    packages=setuptools.find_packages(),
    url='https://gitlab.inria.fr/vidjil/mkdocs-gitlab-plugin',
    license='MIT',
    author='magiraud',
    keywords='markdown gitlab links',
    description='MkDocs plugin to transform strings such as #1234 into links to a Gitlab repository',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[x for x in requires if x and not x.startswith('#')],
    entry_points={
        'mkdocs.plugins': [
            'gitlab_links = mkdocs_gitlab_plugin.plugin:GitlabLinksPlugin',
        ]
    },
    classifiers=[
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Documentation',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
  ],
)
