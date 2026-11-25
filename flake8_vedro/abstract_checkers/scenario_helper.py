import ast
import pathlib
from typing import List, NamedTuple, Optional

from flake8_vedro.helpers import is_vedro_decorator

SCENARIOS_FOLDER = 'scenarios'
SCENARIO_CLASS_NAME = 'Scenario'


class Subject(NamedTuple):
    value: Optional[str]  # None if subject is not a string literal
    lineno: int
    col_offset: int


class ScenarioHelper:

    def get_all_steps(self, class_node: ast.ClassDef) -> List:
        return [
            element for element in class_node.body if (
                isinstance(element, ast.FunctionDef)
                or isinstance(element, ast.AsyncFunctionDef)
            )
        ]

    def get_init_step(self, node: ast.ClassDef) -> Optional[ast.FunctionDef]:
        for element in node.body:
            if isinstance(element, ast.FunctionDef) and element.name == '__init__':
                return element

    def get_subjects(self, node: ast.ClassDef) -> List[Subject]:
        subjects = []
        for element in node.body:
            if not isinstance(element, ast.Assign):
                continue
            target = element.targets[0]
            if not isinstance(target, ast.Name) or target.id != 'subject':
                continue

            value = element.value
            is_literal = isinstance(value, ast.Constant) and isinstance(value.value, str)
            subjects.append(Subject(value=value.value if is_literal else None,
                                    lineno=element.lineno,
                                    col_offset=element.col_offset))
        return subjects

    def get_subject(self, node: ast.ClassDef) -> Optional[Subject]:
        subjects = self.get_subjects(node)
        return subjects[0] if subjects else None

    def get_params_decorators(self, init_node: ast.FunctionDef,
                              import_from_nodes: List[ast.ImportFrom]) -> List[ast.Call]:
        return [
            decorator for decorator in init_node.decorator_list
            if isinstance(decorator, ast.Call) and is_vedro_decorator(decorator, import_from_nodes, 'params')
        ]

    def get_when_steps(self, steps: List) -> List:
        return [
            step for step in steps if step.name.startswith('when')
        ]

    def get_then_steps(self, steps: List) -> List:
        return [
            step for step in steps if step.name.startswith('then')
        ]

    def is_file_in_folder(self, filename: str,
                          folder: str = SCENARIOS_FOLDER) -> bool:
        path = pathlib.Path(filename)

        for parent in path.parents:
            if parent.name == folder:
                return True
        return False
