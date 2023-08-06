class ConfigMeta(type):

    def __new__(cls, typename, bases, ns):

        if ns.get('_root', False):
            return super().__new__(cls, typename, bases, ns)

        fields_spec = build_fields_spec(ns)

        def build_cfg(data):
            config = load_config(fields_spec, data)
            return ConfigObject(config)

        return build_cfg


class Config(metaclass=ConfigMeta):
    _root = True

    def __new__(*args, **kwargs):
        raise NotImplementedError()


class ConfigObject:
    """Container for loaded configuration"""

    def __init__(self, data):
        self._data = data

    def __getattr__(self, name):
        try:
            return self._data[name]
        except KeyError:
            raise AttributeError(name)

    def __repr__(self):
        return 'Config({})'.format(', '.join(
            '{}={}'.format(key, repr(value))
            for key, value in self._data.items()
        ))


def is_valid_key(key):
    return (not key.startswith('_')) and key.isupper()


def build_fields_spec(ns):
    types = ns.get('__annotations__', {})
    all_keys = set(ns) | set(types)
    fields_spec = {}

    for key in all_keys:
        if not is_valid_key(key):
            continue

        fields_spec[key] = (
            types.get(key, str),
            ns.get(key, None))

    return fields_spec


TRUTHY = {'1', 'true', 'on', 'yes'}
FALSEY = {'', '0', 'false', 'off', 'no'}


def load_value(type_, value):
    if type_ is str:
        return value
    if type_ is bool:
        return value.lower() not in FALSEY
    return type_(value)


def load_config(spec, data):
    config = {}
    for key, fld in spec.items():
        type_, defval = fld
        try:
            value = data[key]
        except KeyError:
            value = defval
        else:
            value = load_value(type_, value)
        config[key] = value
    return config
