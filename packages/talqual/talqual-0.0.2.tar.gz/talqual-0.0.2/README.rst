talqual
=======

|Test| |Coverage| |Pypi|

.. |Test| image:: https://gitlab.com/timbaler/talqual/badges/master/pipeline.svg
        :target: https://gitlab.com/timbaler/talqual/commits/master
.. |Coverage| image:: https://gitlab.com/timbaler/talqual/badges/master/coverage.svg
        :target: https://gitlab.com/timbaler/talqual/commits/master
..  |Pypi| image:: https://img.shields.io/pypi/v/talqual.svg
    :target: https://pypi.python.org/pypi/talqual


TAL_ Chameleon_ static site generator.

Simple structure: templates + data -> output html


.. _TAL: https://chameleon.readthedocs.io/en/latest/reference.html
.. _Chameleon: https://chameleon.readthedocs.io



Installation
------------
Install from PyPI::

    pip install talqual


Developing
----------

Install requirement and launch tests::

    pip install -r requirements-dev.txt
    pytest tests


Selenium
--------

Launch tests with driver option::

  pytest tests --driver firefox


Maybe you get the error::

 selenium.common.exceptions.WebDriverException: Message: 'geckodriver' executable needs to be in PATH.

Then you need to download the latest `geckodriver` release from https://github.com/mozilla/geckodriver/releases (such as `geckodriver-v0.26.0-linux64.tar.gz`) and extract it to the correspongind directory (such as `/usr/local/bin/`).



Usage
-----

* talqual `templates_dir`
* talqual `templates_dir` `output_html` --data `data.yaml`
* python -m talqual `templates_dir` `output_html` --data `data.yaml`

or from code::

 from talqual.main import run
 run(templates_dir, html_dir, data_yaml_file)


Features
--------

Template elements: Folder, File, TalTemplate/Html, NoView, TalCommand
Data elements: Python objects, yaml files


* Define a `data`.yaml file
* Define a `templates` directory
* A folder in the `templates` is created to the `html` directory
* A file (pdf, image, css, js, etc.) in the `templates` is copied to the `html` directory
* A no view element (file or directory starting by `_`) in the `templates` is not created to the `html` directory
* A TAL template in the `templates` gets rendered to the `html` directory

  - It can reference data from the `data` directory or from python objects
  - It can be:

    - a static .html or .htm (with no templating)
    - a simple template .html .htm or .pt (with TAL templating)
    - a template with macros .html .htm or .pt (with TAL and METAL templating)

* A TAL Command gets executed and rendered  to the `html` directory

  - a template with NAME.tal_repeat_VARIABLE.pt gets repeated by `data[VARIABLE]` (it must be an iterable). Results in `NAME.0.html`, `NAME.1.html`, `NAME.2.html`, etc.

  - a template with NAME.tal_batch_VARIABLE_PAGESIZE.pt gets rendered by a Batch of PAGESIZE for `data[VARIABLE]` (it must be an iterable). Results in `NAME.html`, `NAME.2.html`, `NAME.3.html`, etc.

  - a template with NAME.tal_replace_talqual_scripts.js gets rendered to a javascript file NAME.js with the faceted module.


* A template can include the faceted javascript module. See the `portfolio` example.


License
-------

``talqual`` is offered under the GPLv3 license.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
