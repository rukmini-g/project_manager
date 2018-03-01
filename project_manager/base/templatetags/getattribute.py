import re
import inspect
from django import template
from django.conf import settings

numeric_test = re.compile("^\d+$")
register = template.Library()


def getattribute(value, arg):
    """Gets an attribute of an object dynamically from a string name"""
    if re.match(r'\w+\.\w+', arg):
        matches = re.findall(r'(\w+)', arg)
        for match in matches:
            if hasattr(value, match):
                if inspect.ismethod(getattr(value, match)):
                    value = getattr(value, match)()
                else:
                    value = getattr(value, match)
        return value
    if hasattr(value, str(arg)):
        if inspect.ismethod(getattr(value, str(arg))):
            return getattr(value, arg)()
        else:
            return getattr(value, arg)
    elif hasattr(value, 'has_key') and value.has_key(arg):
        return value[arg]
    elif numeric_test.match(str(arg)) and len(value) > int(arg):
        return value[int(arg)]
    else:
        return settings.TEMPLATE_STRING_IF_INVALID

register.filter('getattribute', getattribute)
