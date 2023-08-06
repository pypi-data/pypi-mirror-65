from setuptools import setup
import os, io
from webcheck import __version__

here = os.path.abspath(os.path.dirname(__file__))
README = io.open(os.path.join(here, 'README.md'), encoding='UTF-8').read()
CHANGES = io.open(os.path.join(here, 'CHANGES.md'), encoding='UTF-8').read()
setup(name="webcheck",
      version=__version__,
      keywords=('webcheck', 'HTTP', 'HTTPS', 'SSL'),
      description="A Web Site check tool.",
      long_description=README + '\n\n\n' + CHANGES,
      long_description_content_type="text/markdown",
      url='https://github.com/sintrb/webcheck/',
      author="trb",
      author_email="sintrb@gmail.com",
      packages=['webcheck'],
      install_requires=['pyOpenSSL'],
      zip_safe=False
      )
