import ast
from typing import List, Optional

from flake8_plugin_utils import Error

from flake8_vedro.abstract_checkers import ScenarioChecker
from flake8_vedro.errors import SkipReasonTicketMissing
from flake8_vedro.helpers import is_vedro_decorator
from flake8_vedro.visitors.scenario_visitor import Context, ScenarioVisitor


@ScenarioVisitor.register_scenario_checker
class SkipTicketChecker(ScenarioChecker):

    @staticmethod
    def _get_reason(decorator: ast.expr) -> Optional[str]:
        """
        Return skip reason: empty string if there is no reason, None if it cannot be checked statically
        """
        if not isinstance(decorator, ast.Call):
            return ''

        keywords = {keyword.arg: keyword.value for keyword in decorator.keywords}
        reason = decorator.args[0] if decorator.args else keywords.get('reason')

        if reason is None:
            return ''
        if isinstance(reason, ast.Constant) and reason.value is None:
            return ''
        if isinstance(reason, ast.Constant) and isinstance(reason.value, str):
            return reason.value
        return None

    def check_scenario(self, context: Context, config) -> List[Error]:
        if config.skip_ticket_pattern is None:
            return []

        errors = []
        for decorator in context.scenario_node.decorator_list:
            if not is_vedro_decorator(decorator, context.import_from_nodes, 'skip'):
                continue

            reason = self._get_reason(decorator)
            if reason is None or config.skip_ticket_pattern.search(reason):
                continue

            errors.append(SkipReasonTicketMissing(decorator.lineno, decorator.col_offset))
        return errors
