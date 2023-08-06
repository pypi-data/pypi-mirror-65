# pytest-modifyscope
pytest pluging to modify fixture scope

You can use this plugin if you want to change the scope of a fixture for a specific test only.

Install with:
```text
pip install pytest-modifyscope
```

For example, this:
```python
import pytest
import logging

logger = logging.getLogger(__name__)


@pytest.fixture(scope='class')
def class_fixture():
    logger.info('class setup')
    yield
    logger.info('class teardown')


@pytest.fixture(scope='function')
def function_fixture():
    logger.info('function setup')
    yield
    logger.info('function teardown')


@pytest.mark.modifyscope(class_fixture='function')
def test_modifyscope(function_fixture, class_fixture):
    logger.info('call')
```

Yields this output:
```text
pytest test_plugin.py
============================= test session starts =============================
platform win32 -- Python 3.6.8, pytest-5.4.1, py-1.8.1, pluggy-0.13.1
plugins: modifyscope-0.2.0
collected 1 item

----------------------------- live log collection -----------------------------
INFO     pytest_modifyscope:__init__.py:19 Modify fixture scope
INFO     pytest_modifyscope:__init__.py:21 Set "class_fixture" scope to function

------------------------------- live log setup --------------------------------
INFO     tests.test_plugin:test_plugin.py:16 function setup
INFO     tests.test_plugin:test_plugin.py:9 class setup
-------------------------------- live log call --------------------------------
INFO     tests.test_plugin:test_plugin.py:23 call
PASSED                                                                   [100%]
------------------------------ live log teardown ------------------------------
INFO     tests.test_plugin:test_plugin.py:11 class teardown
INFO     tests.test_plugin:test_plugin.py:18 function teardown


============================== 1 passed in 0.05s ==============================
```


