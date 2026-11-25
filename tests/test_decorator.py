from flake8_plugin_utils import assert_error, assert_not_error

from flake8_vedro.errors import DecoratorVedroOnly
from flake8_vedro.visitors import ScenarioVisitor
from flake8_vedro.visitors.scenario_checkers import VedroOnlyChecker


def test_vedro_decorator_only():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(VedroOnlyChecker)
    code = """
    @vedro.only
    class Scenario: pass
    """
    assert_error(ScenarioVisitor, code, DecoratorVedroOnly)


def test_decorator_only():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(VedroOnlyChecker)
    code = """
    from vedro import only
    @only
    class Scenario: pass
    """
    assert_error(ScenarioVisitor, code, DecoratorVedroOnly)


def test_vedro_decorator_skip():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(VedroOnlyChecker)
    code = """
    @vedro.skip
    class Scenario: pass
    """
    assert_not_error(ScenarioVisitor, code)


def test_decorator_skip():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(VedroOnlyChecker)
    code = """
    from vedro import skip
    @skip
    class Scenario: pass
    """
    assert_not_error(ScenarioVisitor, code)


def test_aliased_decorator_only():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(VedroOnlyChecker)
    code = """
    from vedro import only as o
    @o
    class Scenario: pass
    """
    assert_error(ScenarioVisitor, code, DecoratorVedroOnly)


def test_decorator_only_not_from_vedro():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(VedroOnlyChecker)
    code = """
    from helpers import only
    @only
    class Scenario: pass
    """
    assert_not_error(ScenarioVisitor, code)


def test_nested_attribute_decorator_only():
    ScenarioVisitor.deregister_all()
    ScenarioVisitor.register_scenario_checker(VedroOnlyChecker)
    code = """
    @helpers.decorators.only
    class Scenario: pass
    """
    assert_not_error(ScenarioVisitor, code)
