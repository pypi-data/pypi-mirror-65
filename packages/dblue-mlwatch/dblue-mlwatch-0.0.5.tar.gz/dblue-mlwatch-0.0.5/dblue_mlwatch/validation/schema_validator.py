from typing import Dict, Tuple

from cerberus import Validator


def validate_schema(data, schema) -> Tuple[bool, Dict]:
    validator = Validator(schema)
    status = validator.validate(data)

    return status, validator.errors
