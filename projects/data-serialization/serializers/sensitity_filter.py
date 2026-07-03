from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Iterable

DEFAULT_EXCLUDED_FIELDS: set[str] = {
    'password',
    'token',
    'apikey',
    'api_key',
    'sessionid',
    'session_id',
    'secret',
}


def filter_sensitive(
    data: dict,
    *,
    exclude_keys: Iterable[str] = DEFAULT_EXCLUDED_FIELDS,
    force_include: Iterable[str] | None = None,
) -> dict:
    """Remove sensitive fields unless explicitly allowed."""
    force_include = set(force_include or [])
    exclude_keys = {k.lower() for k in exclude_keys}
    safe = {}
    for key, value in data.items():
        key_lc = key.lower()
        if key_lc in exclude_keys and key not in force_include:
            continue
        safe[key] = value
    return safe
