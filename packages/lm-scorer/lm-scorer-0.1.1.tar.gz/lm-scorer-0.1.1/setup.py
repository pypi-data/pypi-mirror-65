# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['lm_scorer',
 'lm_scorer.bin',
 'lm_scorer.models',
 'lm_scorer.models.abc',
 'tests',
 'tests.models']

package_data = \
{'': ['*']}

install_requires = \
['pip>=20.0.0,<21.0.0', 'torch>=1.4.0,<2.0.0', 'transformers>=2.7.0,<3.0.0']

entry_points = \
{'console_scripts': ['lm-scorer = lm_scorer.bin.cli:run']}

setup_kwargs = {
    'name': 'lm-scorer',
    'version': '0.1.1',
    'description': 'Language Model based sentences scoring library',
    'long_description': '<h1 align="center">\n  <b>lm-scorer</b>\n</h1>\n<p align="center">\n  <!-- PyPi -->\n  <a href="https://pypi.org/project/lm-scorer">\n    <img src="https://img.shields.io/pypi/v/lm-scorer.svg" alt="PyPi version" />\n  </a>\n  <br />\n  <!-- Lint -->\n  <a href="https://github.com/simonepri/lm-scorer/actions?query=workflow:lint+branch:master">\n    <img src="https://github.com/simonepri/lm-scorer/workflows/lint/badge.svg?branch=master" alt="Lint status" />\n  </a>\n  <!-- Test - macOS -->\n  <a href="https://github.com/simonepri/lm-scorer/actions?query=workflow:test-macos+branch:master">\n    <img src="https://github.com/simonepri/lm-scorer/workflows/test-macos/badge.svg?branch=master" alt="Test macOS status" />\n  </a>\n  <!-- Test - Ubuntu -->\n  <a href="https://github.com/simonepri/lm-scorer/actions?query=workflow:test-ubuntu+branch:master">\n    <img src="https://github.com/simonepri/lm-scorer/workflows/test-ubuntu/badge.svg?branch=master" alt="Test Ubuntu status" />\n  </a>\n  <br />\n  <!-- Code style -->\n  <a href="https://github.com/ambv/black">\n    <img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code style" />\n  </a>\n  <!-- Linter -->\n  <a href="https://github.com/PyCQA/pylint">\n    <img src="https://img.shields.io/badge/linter-pylint-ce963f.svg" alt="Linter" />\n  </a>\n  <!-- Types checker -->\n  <a href="https://github.com/PyCQA/pylint">\n    <img src="https://img.shields.io/badge/types%20checker-mypy-296db2.svg" alt="Types checker" />\n  </a>\n  <!-- Test runner -->\n  <a href="https://github.com/pytest-dev/pytest">\n    <img src="https://img.shields.io/badge/test%20runner-pytest-449bd6.svg" alt="Test runner" />\n  </a>\n  <!-- Task runner -->\n  <a href="https://github.com/illBeRoy/taskipy">\n    <img src="https://img.shields.io/badge/task%20runner-taskipy-abe63e.svg" alt="Task runner" />\n  </a>\n  <!-- Build tool -->\n  <a href="https://github.com/python-poetry/poetry">\n    <img src="https://img.shields.io/badge/build%20system-poetry-4e5dc8.svg" alt="Build tool" />\n  </a>\n  <br />\n  <!-- License -->\n  <a href="https://github.com/simonepri/lm-scorer/tree/master/license">\n    <img src="https://img.shields.io/github/license/simonepri/lm-scorer.svg" alt="Project license" />\n  </a>\n</p>\n<p align="center">\n  📃 Language Model based sentences scoring library\n</p>\n\n## Synopsis\n\nThis package provides a simple programming interface to score sentences using different ML [language models](wiki:language-model).\n\nA simple [CLI](#cli) is also available for quick prototyping.\n\n## Install\n\n```bash\npip install lm-scorer\n```\n\n## Usage\n\n```python\nfrom lm_scorer.models.auto import AutoLMScorer as LMScorer\n\nLMScorer.supported_model_names()\n# => ["gpt2", "gpt2-medium", "gpt2-large", "gpt2-xl", distilgpt2"]\n\nscorer = LMScorer.from_pretrained("gpt2")\n\nscorer.score("I like this package.")\n# => -25.835\nscorer.score("I like this package.", return_tokens=True)\n# => -25.835, {\n#   "I": -3.9997,\n#   "Ġlike": -5.0142,\n#   "Ġthis": -2.5178,\n#   "Ġpackage": -7.4062,\n#   ".": -1.2812,\n#   "<|endoftext|>": -5.6163,\n# }\n\nscorer.score("I like this package.", return_log_prob=False)\n# => 6.0231e-12\nscorer.score("I like this package.", return_log_prob=False, return_tokens=True)\n# => 6.0231e-12, {\n#   "I": 0.018321,\n#   "Ġlike": 0.0066431,\n#   "Ġthis": 0.080633,\n#   "Ġpackage": 0.00060745,\n#   ".": 0.27772,\n#   "<|endoftext|>": 0.0036381,\n# }\n\n```\n\n## CLI\n\n<img src="https://github.com/simonepri/lm-scorer/raw/master/media/cli.gif" alt="lm-scorer cli" width="225" align="right"/>\n\nThe pip package includes a CLI that you can use to score sentences.\n\n```\nusage: lm-scorer [-h] [--model-name MODEL_NAME] [--tokens] [--log-prob]\n                 [--debug]\n                 sentences-file-path\n\nGet sentences probability using a language model.\n\npositional arguments:\n  sentences-file-path   A file containing sentences to score, one per line. If\n                        - is given as filename it reads from stdin instead.\n\noptional arguments:\n  -h, --help            show this help message and exit\n  --model-name MODEL_NAME, -m MODEL_NAME\n                        The pretrained language model to use. Can be one of:\n                        gpt2, gpt2-medium, gpt2-large, gpt2-xl, distilgpt2.\n  --tokens, -t          If provided it provides the probability of each token\n                        of each sentence.\n  --log-prob, -lp       If provided log probabilities are returned instead.\n  --debug               If provided it provides additional logging in case of\n                        errors.\n```\n\n## Authors\n\n- **Simone Primarosa** - [simonepri][github:simonepri]\n\nSee also the list of [contributors][contributors] who participated in this project.\n\n\n## License\n\nThis project is licensed under the MIT License - see the [license][license] file for details.\n\n\n\n<!-- Links -->\n\n[start]: https://github.com/simonepri/lm-scorer#start-of-content\n[license]: https://github.com/simonepri/lm-scorer/tree/master/license\n[contributors]: https://github.com/simonepri/lm-scorer/contributors\n\n[wiki:language-model]: https://en.wikipedia.org/wiki/Language_model\n\n[github:simonepri]: https://github.com/simonepri\n',
    'author': 'Simone Primarosa',
    'author_email': 'simonepri@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/simonepri/lm-scorer#readme',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<3.8',
}


setup(**setup_kwargs)
