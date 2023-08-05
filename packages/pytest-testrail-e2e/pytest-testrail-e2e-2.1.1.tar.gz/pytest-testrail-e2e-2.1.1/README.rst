pytest-testrail-e2e
===================

|PyPI version| |Downloads| |MIT license| |pytest|

This is a pytest plugin for creating/editing testplans or testruns based
on pytest markers. The results of the collected tests will be updated
against the testplan/testrun in TestRail.

Installation
------------

::

    pip install pytest-testrail-e2e

Configuration
-------------

Config for Pytest tests
~~~~~~~~~~~~~~~~~~~~~~~

Add a marker to the tests that will be picked up to be added to the run.

.. code:: python

        from pytest_testrail.plugin import testrail

        @testrail('C1234', 'C5678')
        def test_foo():
            # test code goes here

        # OR    

        from pytest_testrail.plugin import pytestrail

        @pytestrail.case("C1234", "C5678")
        def test_bar():
            # test code goes here

Or if you want to add defects to testcase result:

.. code:: python


        from pytest_testrail.plugin import pytestrail

        @pytestrail.defect("PF-524", "BR-543")
        def test_bar():
            # test code goes here

Skip a testcase [**You need create 'Skipped' status in TestRail'**]:

.. code:: python


        from pytest_testrail.plugin import pytestrail

        @pytestrail.case("C1234")
        @pytest.mark.skip("Mark as skipped description") 
        # or @pytest.mark.skip(reason="Mark as skipped description")
        def test_bar():
            # test code goes here

Block a testcase:

.. code:: python


        from pytest_testrail.plugin import pytestrail

        @pytestrail.case("C1234")
        @pytest.mark.skip(reason="Mark as skipped description", block=True)
        def test_bar():
            # test code goes here

Config for TestRail
~~~~~~~~~~~~~~~~~~~

-  Settings file template config:

.. code:: ini

        [API]
        url = https://yoururl.testrail.net/
        email = user@email.com
        password = <api_key>

        [TESTRUN]
        assignedto_id = 1
        project_id = 2
        suite_id = 3
        plan_id = 4
        description = 'This is an example description'

        [TESTCASE]
        custom_comment = 'This is a custom comment'

Or

-  Set command line options (see below)

Usage
-----

Basically, the following command will create a testrun in TestRail, add
all marked tests to run. Once the all tests are finished they will be
updated in TestRail:

.. code:: bash

        py.test --testrail --tr-config=<settings file>.cfg

All available options
~~~~~~~~~~~~~~~~~~~~~

+-----------------+----------------------------------------------------------+
| option          | description                                              |
+=================+==========================================================+
| --testrail      | Create and update testruns with TestRail                 |
+-----------------+----------------------------------------------------------+
| --tr-config     | Path to the config file containing information about the |
|                 | TestRail server (defaults to testrail.cfg)               |
+-----------------+----------------------------------------------------------+
| --tr-url        | TestRail address you use to access TestRail with your    |
|                 | web browser (config file: url in API section)            |
+-----------------+----------------------------------------------------------+
| --tr-email      | Email for the account on the TestRail server (config     |
|                 | file: email in API section)                              |
+-----------------+----------------------------------------------------------+
| --tr-password   | Password for the account on the TestRail server (config  |
|                 | file: password in API section)                           |
+-----------------+----------------------------------------------------------+
| --tr-testrun-as | ID of the user assigned to the test run (config          |
| signedto-id     | file:assignedto\_id in TESTRUN section)                  |
+-----------------+----------------------------------------------------------+
| --tr-testrun-pr | ID of the project the test run is in (config file:       |
| oject-id        | project\_id in TESTRUN section)                          |
+-----------------+----------------------------------------------------------+
| --tr-testrun-su | ID of the test suite containing the test cases (config   |
| ite-id          | file: suite\_id in TESTRUN section)                      |
+-----------------+----------------------------------------------------------+
| --tr-testrun-su | Include all test cases in specified test suite when      |
| ite-include-all | creating test run (config file: include\_all in TESTRUN  |
|                 | section)                                                 |
+-----------------+----------------------------------------------------------+
| --tr-testrun-na | Name given to testrun, that appears in TestRail (config  |
| me              | file: name in TESTRUN section)                           |
+-----------------+----------------------------------------------------------+
| --tr-testrun-de | Description given to testrun, that appears in TestRail   |
| scription       | (config file: description in TESTRUN section)            |
+-----------------+----------------------------------------------------------+
| --tr-run-id     | Identifier of testrun, that appears in TestRail. If      |
|                 | provided, option "--tr-testrun-name" will be ignored     |
+-----------------+----------------------------------------------------------+
| --tr-plan-id    | Identifier of testplan, that appears in TestRail. If     |
|                 | provided, option "--tr-testrun-name" will be ignored     |
+-----------------+----------------------------------------------------------+
| --tr-version    | Indicate a version in Test Case result.                  |
+-----------------+----------------------------------------------------------+
| --tr-no-ssl-cer | Do not check for valid SSL certificate on TestRail host  |
| t-check         |                                                          |
+-----------------+----------------------------------------------------------+
| --tr-close-on-c | Close a test plan or test run on completion.             |
| omplete         |                                                          |
+-----------------+----------------------------------------------------------+
| --tr-dont-publi | Do not publish results of "blocked" testcases in         |
| sh-blocked      | TestRail                                                 |
+-----------------+----------------------------------------------------------+
| --tr-skip-missi | Skip test cases that are not present in testrun          |
| ng              |                                                          |
+-----------------+----------------------------------------------------------+
| --tr-milestone- | Identifier of milestone to be assigned to run            |
| id              |                                                          |
+-----------------+----------------------------------------------------------+
| --tc-custom-com | Custom comment, to be appended to default comment for    |
| ment            | test case (config file: custom\_comment in TESTCASE      |
|                 | section)                                                 |
+-----------------+----------------------------------------------------------+
| --tr-report-sin | Report result immediately for each test case when it     |
| gle-test        | finished                                                 |
+-----------------+----------------------------------------------------------+

TestRail Settings
-----------------

To increase security, the TestRail team suggests using an API key
instead of a password. You can see how to generate an API key
`here <http://docs.gurock.com/testrail-api2/accessing#username_and_api_key>`__.

If you maintain your own TestRail instance on your own server, it is
recommended to `enable HTTPS for your TestRail
installation <http://docs.gurock.com/testrail-admin/admin-securing#using_https>`__.

For TestRail hosted accounts maintained by
`Gurock <http://www.gurock.com/>`__, all accounts will automatically use
HTTPS.

You can read the whole TestRail documentation
`here <http://docs.gurock.com/>`__.

Author
------

NGUYEN Viet - `github <https://github.com/vietnq254>`__

License
-------

This project is licensed under the `MIT license </LICENSE>`__.

Acknowledgments
---------------

-  `allankp <https://github.com/allankp>`__, author of the
   `pytest-testrail <https://github.com/allankp/pytest-testrail>`__
   repository that was cloned.

.. |PyPI version| image:: https://badge.fury.io/py/pytest-testrail-e2e.svg
   :target: https://badge.fury.io/py/pytest-testrail-e2e
.. |Downloads| image:: https://pepy.tech/badge/pytest-testrail-e2e
   :target: https://pepy.tech/project/pytest-testrail-e2e
.. |MIT license| image:: http://img.shields.io/badge/license-MIT-brightgreen.svg
   :target: /LICENSE
.. |pytest| image:: https://img.shields.io/badge/pytest-%3E%3D3.6-blue.svg
   :target: https://img.shields.io/badge/pytest-%3E%3D3.6-blue.svg
