import contextlib

class ContextualDescriptorSetter(object):
    @classmethod
    def wrap(cls, value, descriptor):
        baseclass = type(value)
        baseclassname = baseclass.__name__
        subclassname = 'ContextualDescriptorSetterWrapped{}'.format(baseclassname)
        return type(subclassname, (baseclass, cls), {
            '_descriptor': descriptor,
        })(value)

    @contextlib.contextmanager
    def __call__(self, value):
        self._descriptor._value = value
        yield
        self._descriptor._value = self

class CustomDescriptor(object):
    def __init__(self, instance, value):
        self._instance = instance
        self._name = None
        self.__set__(instance, value)
    def __set_name__(self, owner, name):
        self._name = name
    def __get__(self, instance, owner):
        if isinstance(instance, ContextualDescriptorSetter):
            # When we are setting the value from within the __call__ method of the
            # dynamically created ContextualDescriptorSetter subclasses we must
            # let them talk to the real us
            return self
        else:
            # Everybody else gets the underlying value
            return self._value
    def __set__(self, instance, value):
        wrapped_value = value
        if not isinstance(wrapped_value, ContextualDescriptorSetter):
            wrapped_value = ContextualDescriptorSetter.wrap(value, self)
        self._value = wrapped_value

def properties(*args, **kwargs):
    class wrapper(object):
        def __init__(self, *args, **kwargs):
            self._contextual_properties = {
                **{arg: None for arg in args},
                **kwargs,
            }
        def __call__(self, klass):
            for (name, value) in self._contextual_properties.items():
                setattr(klass, name, CustomDescriptor(self, value))
            return klass
    return wrapper(*args, **kwargs)
