# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['braindead']

package_data = \
{'': ['*'],
 'braindead': ['default_template/*', 'default_template/static/styles/*']}

install_requires = \
['jinja2>=2.11.1,<3.0.0',
 'markdown>=3.2.1,<4.0.0',
 'pygments>=2.6.1,<3.0.0',
 'toml>=0.10.0,<0.11.0']

entry_points = \
{'console_scripts': ['braindead = braindead.rendering:render_blog']}

setup_kwargs = {
    'name': 'braindead',
    'version': '0.1.3',
    'description': 'Braindead is a braindead simple static site generator for minimalists, that has support for markdown and code highlighting.',
    'long_description': '# Braindead\nBraindead is a braindead simple static site generator for minimalists, that has support for markdown and code highlighting.\nI created this package simply to have a bit of fun and because I\'m tired of bloated software.\n\nCan\'t we just have [simple software nowadays](https://tonsky.me/blog/disenchantment/) that does what it needs to do and nothing more?\nExisting solutions felt like they are too much for my needs. So I built this thing. It\'s still under active development.\n\nLive example: [grski.pl](https://grski.pl/)\n\nOne of my main ideals here is to create template that is as fast as it gets. Generated pages take around 10-15 KB in total.\nNo JavaScript used here, at least in the base template. Just css/html.\n\nYou are free to change that though by creating your own templates. More on that below.\n\nBenefits of simple approach:\n\n![Google PageSpeed Insights withh 100 score](https://imgur.com/7IwldRE.png)\n![requests made if loading this template](https://imgur.com/GmYcP08.png)\n \nDefault template scores 100/100 on Google PageSpeed Insights and very fast load times.\n\nDefault template design looks like this:\n\n![Default template of braindead](https://imgur.com/oPdgdvW.png)\nIt\'s based on: [Kiss template](https://github.com/ribice), slightly modified - with minimized styles. In the future I\'ll probably slim them down even more.\n\nIt\'s also eco friendly - it uses less power by not being a bloatware. \n\n# Installation\n```\npip install braindead\n```\n[PyPi page](https://pypi.org/project/braindead/)\n\n# Usage\nCreate `index.md` and run `braindead` that\'s it. You\'ll find your generated site in `dist` directory.\nIt can be empty or not - your choice. If you want index  to contain just the posts - leave it empty.\n\nThat\'s the minimal setup you need. That\'ll generate index.html for you, but well, it\'s not enough, right?\nMore robust structure you can use is:\n```bash\npages/\n  page.md\nposts/\n  post.md\nindex.md\nsite.toml\n```\n\n## Example post/page structure:\n\n```markdown\nTitle: Title of the post or of the page \nDate: 2018-03-22\nAuthors: Olaf Górski\nDescription: Description of the post/page. If not provided it\'ll default to first 140 chars of the content. \n\nCONTENT GOES HERE...\n```\n\nAll of the metadata used here will be available during given page rendering. You can add more keys and metadata if you\'d like. \n\n## Config\n\nAll of the variables that are used to generate the page can be overwritten by creating `site.toml` file, but it\'s not required to get started.\n\n```toml\nBASE_URL = "/"  # give full url ending with slash here - eg. if you host your blog on https://grski.pl/ enter it there.\n\n[site]\ntitle = "Site generated with braindead"  # base title of the website\ndescription = "Just a description of site generated in braindead"  # description used in the meta tags\ncontent = ""  # this will display under heading\nname = "braindeadsite" # og tags\nlogo = "logo_url"  # url to the logo for og tags\nheading = "Braindead Example"  # heading at the top of the site\ngithub = "https://github.com/grski"  # link to your github\nlinkedin = "https://linkedin.com/in/olafgorski"  # link to your li\ncopy_text = "Olaf Górski"  # copy text in the footer\ncopy_link = "https://grski.pl"  # and copy link of the footer\n```\n\nNone of these are required. You can overwrite none, one or more. Your choice.\n\n# Code higlighting\nJust do\n<pre>\n```python\nYour code here\n```</pre>\n\n[List of languages supported by pygments can be found here.](https://pygments.org/languages/)\n\n# Creating your own templates\nTODO\n\n# Technology\nThis bases on \n[toml](https://github.com/uiri/toml), \n[markdown](https://github.com/Python-Markdown/markdown) and [jinja2](https://github.com/pallets/jinja).\n\nToml is used for configuration.\nMarkdown to render all the .md and .markdows into proper html.\nLastly jinja2 to add some contexts here and there.\n\nFormatting of the code is done using [black](https://github.com/psf/black), [isort](https://github.com/timothycrosley/isort).\n[flake8](https://gitlab.com/pycqa/flake8), [autoflake](https://github.com/myint/autoflake) and [bandit](https://github.com/PyCQA/bandit/) to check for potential vulns. \n\nVersioning is done with [bumpversion](https://github.com/peritus/bumpversion).\nPatch for merges to develop, minor for merged to master. Merge to master means release to pypi.\n\nAnd wonderful [poetry](https://github.com/python-poetry/poetry) as dependency manager. BTW pipenv should die.\n\nCode highligthing is done with [pygments](https://github.com/pygments/pygments).\n\nI use type hinting where it\'s possible.\n\nTo start developing you need to install poetry\n`pip install poetry==0.1.0` and then just `poetry install`. \n\n# Known make commands\n```bash\nflake\nisort\nisort-inplace\nbandit\nblack\nlinters\nbumpversion\nblack-inplace\nautoflake-inplace\nformat-inplace\n```\nMost important ones are `make linters` and `make format-inplace`. Before each commit it\'s required to run these checks.\n\n# License\nMIT\n\n\n',
    'author': 'Olaf Górski',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://grski.pl/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
