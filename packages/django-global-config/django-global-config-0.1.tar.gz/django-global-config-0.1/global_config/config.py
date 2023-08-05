import sys


class ProxyConfigClass(type):
    def __getattribute__(self, key):
        if key.startswith('_default_'):
            return super().__getattribute__(key.replace('_default_', ''))

        if key.startswith('_'):
            return super().__getattribute__(key)

        if 'ConfigItem' not in sys.modules:
            from .models import ConfigItem

        try:
            config_item = ConfigItem.objects.get(key=key)
        except ConfigItem.DoesNotExist:
            return super().__getattribute__(key)
        else:
            return config_item.value

    def __setattr__(self, key, value):
        raise Exception('You can only modify the global config by either adding/modifying a ConfigItem in the database'
                        ' or by setting a new default on the GlobalConfig class')


class GlobalConfig(metaclass=ProxyConfigClass):
    """
    This class provides global configuration that can be dynamically updated by inserting or updating rows in the database
    A new configuration "key" must be added here with a default value, after which a new migration must be created and run
    """
    @classmethod
    def _get_subclass(cls):
        subclasses = cls.__subclasses__()
        if len(subclasses) > 1:
            raise NotImplementedError('Global config does not support more than one config subclass')
        elif not subclasses:
            return cls
        return subclasses[0]

    @classmethod
    def _get_default_value(cls, key):
        return getattr(cls, '_default_' + key)

    @classmethod
    def _get_keys_by_type(cls):
        keys_by_type = {}
        config_class = cls._get_subclass()
        for k in dir(config_class):
            if k.startswith('_'):
                continue
            v = config_class._get_default_value(k)
            key_type = type(v).__name__
            if isinstance(v, list):
                key_type += '_' + type(v[0]).__name__
            if key_type not in keys_by_type:
                keys_by_type[key_type] = []
            keys_by_type[key_type].append(k)
        return keys_by_type
