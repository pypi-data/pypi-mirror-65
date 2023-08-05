import setuptools

class Setup():
    def __init__(self):
        setuptools.setup(
            name=u'Pysun',
            version=u'0.0.1',
            long_description=open(u'README.txt', u'r').read(),
            long_description_content_type=u'text/markdown',
            author=u'visual.ml',
            keywords=u'window designer display',
            install_requires=[u'PySide2'],
            license=u'MIT',
            packages=[u'pysun'],
            include_package_data=True
        )

Setup()
    