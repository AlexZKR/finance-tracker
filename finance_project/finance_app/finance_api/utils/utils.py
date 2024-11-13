from typing import Tuple

import importlib
from django.conf import settings


def get_auth_token_class_objects() -> Tuple[str]:
    """
    Get tuple of token classes that are allowed for authenticating requests
    """
    class_objects = []
    for path in settings.SIMPLE_JWT["AUTH_TOKEN_CLASSES"]:
        module_name, class_name = path.rsplit(".", 1)
        module = importlib.import_module(module_name)
        class_obj = getattr(module, class_name)
        class_objects.append(class_obj)
    return tuple(class_objects)
