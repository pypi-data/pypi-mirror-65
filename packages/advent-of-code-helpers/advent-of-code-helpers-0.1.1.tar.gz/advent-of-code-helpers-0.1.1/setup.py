from setuptools import setup
import setuptools_scm


def local_scheme(version):
    print(version)
    if version.branch == 'master' and not version.dirty:
        return ''
    return setuptools_scm.version.get_local_node_and_date(version)


setup(
    use_scm_version={
        'local_scheme': local_scheme,
        'write_to': 'src/aoc/version.py',
        'write_to_template': '__version__ = "{version}"\n',
        'tag_regex': r'^(?P<prefix>v)?(?P<version>[^\+]+)(?P<suffix>.*)?$',
    }
)
