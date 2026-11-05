from __future__ import annotations

import json
from pathlib import Path
from typing import Dict, List, Optional

from dil.core.models import RoleDefinition


class RoleManager:
    """Manages predefined banking roles and custom developer-defined roles."""

    def __init__(self, predefined_dir: Optional[Path | str] = None):
        self._roles: Dict[str, RoleDefinition] = {}
        if predefined_dir:
            self._scan_dir(Path(predefined_dir))
        else:
            default_dir = Path(__file__).resolve().parent / "predefined"
            if default_dir.is_dir():
                self._scan_dir(default_dir)

    def _scan_dir(self, directory: Path) -> None:
        for json_file in directory.glob("*.json"):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    role = RoleDefinition(**data)
                    self.register_role(role)
            except Exception:
                pass

    def register_role(self, role: RoleDefinition) -> None:
        self._roles[role.role_id.lower()] = role

    def get_role(self, role_id: str) -> RoleDefinition:
        role_key = role_id.lower()
        if role_key not in self._roles:
            raise KeyError(f"Role '{role_id}' is not defined. Available roles: {list(self._roles.keys())}")
        return self._roles[role_key]

    def create_custom_role(
        self,
        role_id: str,
        name: str,
        objective: str,
        rules: List[str],
        system_instructions: str,
        tone: str = "professional",
        disclaimers: Optional[List[str]] = None,
        description: str = "",
    ) -> RoleDefinition:
        role = RoleDefinition(
            role_id=role_id,
            name=name,
            description=description,
            objective=objective,
            tone=tone,
            system_instructions=system_instructions,
            rules=rules,
            disclaimers=disclaimers or [],
        )
        self.register_role(role)
        return role

    def list_roles(self) -> List[str]:
        return list(self._roles.keys())

