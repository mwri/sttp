"""NOX config."""

import importlib
import glob
import nox


pkg_meta_spec = importlib.util.spec_from_file_location(
    'pkg_meta',
    'sttp/pkg_meta.py',
)
pkg_meta = importlib.util.module_from_spec(pkg_meta_spec)
pkg_meta_spec.loader.exec_module(pkg_meta)


default_pyvsn = '3'
test_pyvsns = ['3.6', '3.7', '3.8', '3.9', '3.10']


@nox.session(python=[default_pyvsn])
def build(session):
    session.install(*pkg_meta.install_requires)
    session.install('setuptools', 'wheel')
    session.run('python3', 'setup.py', 'sdist', 'bdist_wheel')


@nox.session(python=[default_pyvsn])
def docs(session):
    session.install(*pkg_meta.install_requires)
    session.install('sphinx', 'sphinx-rtd-theme')
    session.cd('docs')
    session.run('sphinx-build', '-M', 'clean', 'source', 'build')
    session.run('sphinx-build', '-M', 'html', 'source', 'build')


@nox.session(python=[default_pyvsn])
def lint(session):
    session.install('black')
    session.run('black', '--check', '--line-length', '120', '--skip-string-normalization', 'sttp', 'test')


@nox.session(python=[default_pyvsn])
def coverage(session):
    session.install(*pkg_meta.install_requires)
    session.install('coverage', 'pytest')
    session.run('coverage', 'run', '--branch', '--source=sttp', '-m', 'pytest', 'test')
    session.run('coverage', 'report')
    session.run('coverage', 'html')
    session.run('coverage', 'xml')


@nox.session(python=test_pyvsns)
def test(session):
    session.install(*pkg_meta.install_requires)
    session.install('pytest')
    session.run('pytest')
    session.run('python', '-m', 'doctest', '-f', *glob.glob("docs/source/**/*.rst", recursive=True))
