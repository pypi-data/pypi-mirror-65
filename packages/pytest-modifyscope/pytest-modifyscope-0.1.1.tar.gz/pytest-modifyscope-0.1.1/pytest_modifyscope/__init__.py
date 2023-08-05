import logging

logger = logging.getLogger(__name__)
modified = {}
scopes = "session package module class function".split()


def pytest_runtest_setup(item):
    mark = item.get_closest_marker('modifyscope')
    if not mark:
        return
    logger.info('Modify fixture scope')
    for name, scope in mark.kwargs.items():
        logger.info(f'Set "{name}" scope to {scope}')
        if not item._fixtureinfo.name2fixturedefs.get(name):
            logger.info(f'{name} is not collected')
            return
        modified[name] = item._fixtureinfo.name2fixturedefs[name][0].scope
        item._fixtureinfo.name2fixturedefs[name][0].scope = scope
        item._fixtureinfo.name2fixturedefs[name][0].scopenum = scopes.index(scope)

    fm = item.session._fixturemanager
    closure = fm.getfixtureclosure(item._fixtureinfo.initialnames, item.parent)[1]

    item._fixtureinfo.names_closure = closure
    item.fixturenames.clear()
    item.fixturenames.extend(closure)


def pytest_runtest_teardown(item, nextitem):
    for name, scope in modified.items():
        item._fixtureinfo.name2fixturedefs[name][0].scope = scope
        item._fixtureinfo.name2fixturedefs[name][0].scopenum = scopes.index(scope)
    modified.clear()
