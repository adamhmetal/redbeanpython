class RedBeanError(Exception):
    ...


class InitializationError(RedBeanError):
    ...


class NotInitializedError(RedBeanError):
    ...


class TypeChangeError(RedBeanError):
    ...


class NotExistsError(RedBeanError):
    ...


class FrozenError(RedBeanError):
    ...


class IncorrectNameError(RedBeanError):
    ...


class IncorrectValueError(RedBeanError):
    ...


class ConfigurationError(RedBeanError):
    ...
