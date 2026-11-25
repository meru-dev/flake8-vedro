import ast
from typing import List


def is_vedro_decorator(decorator: ast.expr, import_from_nodes: List[ast.ImportFrom], name: str) -> bool:
    """
    Check if decorator is vedro.<name> or <name> imported (possibly aliased) from vedro, called or not
    """
    target = decorator.func if isinstance(decorator, ast.Call) else decorator

    if isinstance(target, ast.Attribute):
        return (
            isinstance(target.value, ast.Name)
            and target.value.id == 'vedro'
            and target.attr == name
        )

    if not isinstance(target, ast.Name):
        return False

    return any(
        import_from.module == 'vedro'
        and any(
            alias.name == name and (alias.asname or alias.name) == target.id
            for alias in import_from.names
        )
        for import_from in import_from_nodes
    )
