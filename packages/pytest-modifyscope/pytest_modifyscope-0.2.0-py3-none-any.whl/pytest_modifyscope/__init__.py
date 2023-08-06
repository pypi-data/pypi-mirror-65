import logging
from _pytest.fixtures import scope2index

logger = logging.getLogger(__name__)
modified = {}
scopes = "session package module class function".split()


def pytest_runtest_setup(item):
    fi = item._fixtureinfo
    target_scope = {}
    if hasattr(item.cls, 'pytestmark'):
        for mark in item.cls.pytestmark:
            if mark.name == 'modifyscope':
                target_scope.update(mark.kwargs)
    for mark in item.own_markers:
        if mark.name == 'modifyscope':
            target_scope.update(mark.kwargs)
    if target_scope:
        for name, scope in target_scope.items():
            if name not in item.fixturenames:
                logger.debug(f'{name} not collected')
                continue
            if fi.name2fixturedefs.get(name):
                logger.debug(f'Set "{name}" scope to {scope}')
                modified[name] = fi.name2fixturedefs[name][0].scope
                fi.name2fixturedefs[name][0].scopenum = scope2index(scope, f'modifyscope mark argument "{name}"')
                fi.name2fixturedefs[name][0].scope = scope
        if modified:
            fm = item.session._fixturemanager
            closure = fm.getfixtureclosure(fi.initialnames, item.parent)[1]
            fi.names_closure = closure
            item.fixturenames.clear()
            item.fixturenames.extend(closure)


def pytest_runtest_makereport(item, call):
    if call.when == 'teardown':
        for name, scope in modified.items():
            logger.debug(f'Reset "{name}" scope to {scope}')
            item._fixtureinfo.name2fixturedefs[name][0].scopenum = scopes.index(scope)
            item._fixtureinfo.name2fixturedefs[name][0].scope = scope
        modified.clear()
