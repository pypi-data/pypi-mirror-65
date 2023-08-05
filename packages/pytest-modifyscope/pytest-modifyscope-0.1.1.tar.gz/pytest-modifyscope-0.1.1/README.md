# pytest-modifyscope

## Usage
```python
import pytest
import logging

logger = logging.getLogger(__name__)


@pytest.fixture(scope='class')
def c():
    logger.info('class setup')
    yield
    logger.info('class teardown')


@pytest.fixture(scope='function')
def f():
    logger.info('function setup')
    yield
    logger.info('function teardown')


@pytest.mark.modifyscope(c='function')
def test_modifyscope(f, c):
    logger.info('call')
```

```text
tests/test_plugin.py::test_modifyscope 
------------------------------- live log setup --------------------------------
INFO     pytest_modifyscope:__init__.py:12 Modify fixture scope
INFO     pytest_modifyscope:__init__.py:14 Set "c" scope to function
INFO     tests.test_plugin:test_plugin.py:16 function setup
INFO     tests.test_plugin:test_plugin.py:9 class setup
-------------------------------- live log call --------------------------------
INFO     tests.test_plugin:test_plugin.py:23 call
PASSED                                                                   [100%]
------------------------------ live log teardown ------------------------------
INFO     tests.test_plugin:test_plugin.py:11 class teardown
INFO     tests.test_plugin:test_plugin.py:18 function teardown


============================== 1 passed in 0.03s ==============================
```