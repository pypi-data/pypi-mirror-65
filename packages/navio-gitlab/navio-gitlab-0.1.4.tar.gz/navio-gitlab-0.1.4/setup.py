from setuptools import setup
import navio.meta_gitlab
setup(
    name='navio-gitlab',
    version=navio.meta_gitlab.__version__,
    author='Navio Online OpenSource projects',
    author_email='oss@navio.online',
    url=navio.meta_gitlab.__website__,
    packages=['navio', 'navio.gitlab'],
    install_requires=['python-gitlab'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    license='Apache 2.0 license',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3'
    ],
    keywords=['framework'],
    description='Gitlab Pipelines helper libs',
    long_description="{}\n{}".format(
        open("README.md", 'rb').read().decode('utf-8'),
        open("CHANGES.md", 'rb').read().decode('utf-8')
    ),
    long_description_content_type='text/markdown'
)
