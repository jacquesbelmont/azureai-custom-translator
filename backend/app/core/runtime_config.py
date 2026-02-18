from __future__ import annotations

from typing import Any, Dict, Optional


_runtime_overrides: Dict[str, Any] = {}


def set_overrides(values: Dict[str, Any]) -> None:
    for k, v in values.items():
        if v is None:
            continue
        _runtime_overrides[k] = v


def clear_overrides() -> None:
    _runtime_overrides.clear()


def get_override(key: str) -> Optional[Any]:
    return _runtime_overrides.get(key)


def get_all_overrides() -> Dict[str, Any]:
    return dict(_runtime_overrides)
