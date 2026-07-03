from datetime import date, datetime, time, timedelta
from pathlib import Path
from typing import Any


def normalize(obj: Any) -> Any:
    match obj:
        case Path():
            return {
                '__type__': 'Path',
                'value': str(obj),
            }
        case datetime():
            return {
                '__type__': 'datetime',
                'value': obj.isoformat(timespec='microseconds'),
            }
        case date():
            return {
                '__type__': 'date',
                'value': obj.isoformat(),
            }
        case time():
            return {
                '__type__': 'time',
                'value': obj.isoformat(timespec='microseconds'),
            }
        case timedelta():
            return {
                '__type__': 'timerange',
                'value': obj.total_seconds(),
            }
        case _:
            return obj


def _denormalize_object(obj: Any) -> Any:
    obj_type = obj['__type__']
    value = obj['value']

    match obj_type:
        case 'Path':
            return Path(value)
        case 'datetime':
            return datetime.fromisoformat(value)
        case 'date':
            return date.fromisoformat(value)
        case 'time':
            return time.fromisoformat(value)
        case 'timedelta':
            return timedelta(seconds=value)
    return obj


def denormalize(obj: Any) -> Any:
    """Reconstruct Python objects from normalized dictionaries."""
    if not isinstance(obj, dict):
        return obj

    if '__type__' in obj or 'value' in obj:
        return _denormalize_object(obj)

    return obj


def deep_denormalize(obj: Any) -> Any:
    """Recursively denormalize nested structures."""
    if isinstance(obj, list):
        return [deep_denormalize(i) for i in obj]

    if isinstance(obj, dict):
        restored = denormalize(obj)
        if restored is not obj:
            return restored
        return {k: deep_denormalize(v) for k, v in obj.items()}

    return obj
