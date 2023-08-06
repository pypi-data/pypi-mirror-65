# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['rand', 'rand.providers', 'rand.providers.contribs', 'rand.providers.en']

package_data = \
{'': ['*']}

install_requires = \
['pytest-cov>=2.0,<3.0']

setup_kwargs = {
    'name': 'rand',
    'version': '0.1.1',
    'description': 'Generate String from regex pattern',
    'long_description': 'rand\n====\n\nRandom generated String from regex pattern.\n\nWARNING\n-------\n\nThe library **rand** is still in working-in-progress. It is subject to high possibility of API changes. Would appreciate for feedbacks, suggestions or helps.\n\nInstall\n-------\n\nUse pip or clone this repository and execute the setup.py file.\n\n```shell script\n$ pip install rand\n```\n\nUsages\n------\n\n```python\n# import module\nfrom rand import Rand\n\n# initialise object\nrand = Rand()\n\n# generate pattern literal\nrand.gen(\'koro\') # [\'koro\']\nrand.gen(\'28\') # [\'28\']\nrand.gen(\'a-z\') # [\'a-z\']\n\n# generate pattern any\nrand.gen(\'.\') # any char in string.printable\n\n# generate pattern branch\nrand.gen(\'ko|ro\') # either [\'ko\'] or [\'ro\']\nrand.gen(\'ko|ro|ro\') # either [\'ko\'] or [\'ro\']\n\n# generate pattern in\nrand.gen(\'[kororo]\') # either [\'k\'] or [\'o\'] or [\'r\']\nrand.gen(\'k[o]r[o]r[o]\') # [\'kororo\']\n\n# generate pattern repeat\nrand.gen(\'r{2,8}\') # char r in length between 2 to 8 times\n\n# generate pattern range\nrand.gen(\'[a-z]\') # char between a to z\n\n# generate pattern subpattern\nrand.gen(\'(ro)\') # [\'ro\']\n\n# use built-in providers\nrand.gen(\'(:en_vocal:)\') # char either a, i, u, e, o\n```\n\nProviders\n---------\n\nThe library **rand** at core only provide random generator based on regex. Providers are built to allow extensions for rand.\nBelow is sample code how to integrate existing class definition (TestProxy) to Rand.\n\n```python\nfrom rand import Rand\nfrom rand.providers.base import RandProxyBaseProvider\n\n# class definition\nclass TestProxy:\n    # simple function definition to return args values\n    def target(self, arg1=\'def1\', arg2=\'def2\'):\n        return \'%s-%s\' % (arg1, arg2)\n\n# init rand class\nrand = Rand()\n\n# create proxy provider helper and register to rand\ntest_proxy = RandProxyBaseProvider(prefix=\'test\', target=TestProxy())\nrand.register_provider(test_proxy)\n\n# test\nprint(rand.gen(\'(:test_target:)\')) # [\'def1-def2\']\nprint(rand.gen(\'(:test_target:)\', [\'ok1\'])) # [\'ok1-def2\']\nprint(rand.gen(\'(:test_target:)\', [\'ok1\', \'ok2\'])) # [\'ok1-def2\']\nprint(rand.gen(\'(:test_target:)\', [[\'ok1\', \'ok2\']])) # [\'ok1-ok2\']\nprint(rand.gen(\'(:test_target:)\', [[\'ok1\', \'ok2\'], \'ok3\'])) # [\'ok1-ok2\']\nprint(rand.gen(\'(:test_target:)\', [{\'arg1\': \'ok1\'}])) # [\'ok1-def2\']\nprint(rand.gen(\'(:test_target:)\', [{\'arg1\': \'ok1\', \'arg2\': \'ok2\'}])) # [\'ok1-ok2\']\n```\n\nThe library *rand* also has integration with existing projects such as Faker. Ensure you have faker library installed.\n\n```python\nfrom rand import Rand\n\n\nrand = Rand()\nrand.gen(\'(:faker_hexify:)\') # abc\n```\n\nTest\n----\n\nRun test by installing packages and run tox\n\n```shell script\n$ pip install poetry tox\n$ tox\n```\n\nFor hot-reload development coding\n```shell script\n$ npm i -g nodemon\n$ nodemon -w rand --exec python -c "from rand import Rand"\n```\n\n',
    'author': 'kororo',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/kororo/rand',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
