from typing import List

from flake8_plugin_utils import Error

from flake8_vedro.abstract_checkers import ScenarioChecker
from flake8_vedro.errors import DecoratorVedroOnly
from flake8_vedro.helpers import is_vedro_decorator
from flake8_vedro.visitors.scenario_visitor import Context, ScenarioVisitor


@ScenarioVisitor.register_scenario_checker
class VedroOnlyChecker(ScenarioChecker):

    def check_scenario(self, context: Context, *args) -> List[Error]:
        for decorator in context.scenario_node.decorator_list:
            if is_vedro_decorator(decorator, context.import_from_nodes, 'only'):
                return [DecoratorVedroOnly(decorator.lineno, decorator.col_offset)]
        return []
