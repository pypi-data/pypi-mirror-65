import logging
from _pytest.fixtures import scope2index

logger = logging.getLogger(__name__)
modified = {}


def _collect_target(pytestmark):
    target = {}
    if isinstance(pytestmark, list):
        for mark in pytestmark:
            if mark.name == 'modifyscope':
                target.update(mark.kwargs)
    else:
        if pytestmark.name == 'modifyscope':
            target.update(pytestmark.kwargs)
    return target


def pytest_runtest_setup(item):
    fi = item._fixtureinfo
    target_fixture = {}
    if hasattr(item.module, 'pytestmark'):
        target_fixture.update(_collect_target(item.module.pytestmark))
    if hasattr(item.cls, 'pytestmark'):
        target_fixture.update(_collect_target(item.cls.pytestmark))
    target_fixture.update(_collect_target(item.own_markers))
    if target_fixture:
        for name, scope in target_fixture.items():
            if name not in item.fixturenames:
                logger.debug(f'"{name}" not collected')
                continue
            if fi.name2fixturedefs.get(name):
                logger.debug(f'Set "{name}" scope to {scope}')
                modified[name] = fi.name2fixturedefs[name][0].scope
                fi.name2fixturedefs[name][0].scopenum = scope2index(scope, f'modifyscope mark argument "{name}"')
                fi.name2fixturedefs[name][0].scope = scope
        if modified:
            closure = item.session._fixturemanager.getfixtureclosure(fi.initialnames, item.parent)[1]
            fi.names_closure = closure
            item.fixturenames.clear()
            item.fixturenames.extend(closure)


def pytest_runtest_makereport(item, call):
    if call.when == 'teardown':
        for name, scope in modified.items():
            logger.debug(f'Reset "{name}" scope to {scope}')
            item._fixtureinfo.name2fixturedefs[name][0].scopenum = scope2index(scope, f'"{name}"')
            item._fixtureinfo.name2fixturedefs[name][0].scope = scope
        modified.clear()
