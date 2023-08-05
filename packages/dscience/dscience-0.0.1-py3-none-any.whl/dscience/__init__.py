
class ProjectInfo:
	"""Information needed by setup.py and/or docs/conf.py."""
	name = 'dscience'
	release = '0.0.1'
	version = '0.0.1'
	status = "Alpha"
	@staticmethod
	def download_url():
		# https://github.com/kokellab/dscience/archive/0.1.2.tar.gz
		return ProjectInfo.url.rstrip('/')+'/archive/'+ProjectInfo.release+'.tar.gz'
	packages = ['dscience', 'dscience.core', 'dscience.tools', 'dscience.support', 'dscience.biochem', 'dscience.analysis', 'dscience.ml']
	description = 'A collection of Python snippets for the Kokel Lab'
	author = "Douglas Myers-Turnbull"
	copyright = "Copyright 2016–2020, Douglas Myers-Turnbull & UCSF"
	credits = ["Douglas Myers-Turnbull", "Chris Ki", "Cole Helsell", "the Kokel Lab @ UCSF", "the Keiser Lab @ UCSF", "UCSF"]
	maintainer = "Douglas Myers-Turnbull"
	url = 'https://github.com/kokellab/dscience'
	project_urls = {
		"package": "https://pypi.org/project/dscience",
		"build": "https://travis-ci.org/kokellab/dscience",
		'docs': 'https://dscience.readthedocs.io',
		'source': 'https://github.com/kokellab/dscience',
		'issues': 'https://github.com/kokellab/dscience/issues',
	}
	classifiers = [
		"Development Status :: 3 - Alpha",
		'Intended Audience :: Developers',
		'Natural Language :: English',
		'License :: OSI Approved :: Apache Software License',
		'Programming Language :: Python :: 3 :: Only',
		'Programming Language :: Python :: 3.7',
		'Programming Language :: Python :: 3.8',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Topic :: Scientific/Engineering :: Bio-Informatics',
		'Topic :: Scientific/Engineering :: Artificial Intelligence',
		'Operating System :: OS Independent',
		'Typing :: Typed'
	]
	keywords = ['utilities', 'data science', 'pandas']

D = ProjectInfo
__version__ = D.version
__status__ = D.status
__author__ = D.author
__copyright__ = D.copyright
__credits__ = D.credits
__maintainer__ = D.maintainer
