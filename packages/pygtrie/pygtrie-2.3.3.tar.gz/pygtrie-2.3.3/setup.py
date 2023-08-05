import codecs
import distutils.command.sdist
import distutils.core
import os
import re
import re
import shutil
import subprocess
import sys
import tempfile

import version


class BuildDocCommand(distutils.core.Command):
    description = 'build Sphinx documentation'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        release = self.distribution.get_version()
        version = '.'.join(release.split('.', 2)[0:2])
        outdir = tempfile.mkdtemp() if self.dry_run else 'html'
        try:
            subprocess.check_call(('sphinx-build', '-Drelease=' + release,
                                   '-n', '-Dversion=' + version, '.', outdir))
        finally:
            if self.dry_run:
                shutil.rmtree(outdir)


release = version.get_version()

with codecs.open('README.rst', 'r', 'utf-8') as f:
    readme = f.read()
with codecs.open('version-history.rst', 'r', 'utf-8') as f:
    readme += '\n' + f.read()
readme, _ = re.subn(r':(?:class|func|const):`([^`]*)`', r'``\1``', readme)


kwargs = {
    'name': 'pygtrie',
    'version': release,
    'description': 'Trie data structure implementation.',
    'long_description': readme,
    'author': 'Michal Nazarewicz',
    'author_email': 'mina86@mina86.com',
    'url': 'https://github.com/mina86/pygtrie',
    'py_modules': ['pygtrie'],
    'license': 'Apache-2.0',
    'platforms': 'Platform Independent',
    'keywords': ['trie', 'prefix tree', 'data structure'],
    'classifiers': [
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    'cmdclass': {'build_doc': BuildDocCommand},
}

if re.search(r'(?:\d+\.)*\d+', release):
    kwargs['download_url'] = kwargs['url'] + '/tarball/v' + release

distutils.core.setup(**kwargs)
