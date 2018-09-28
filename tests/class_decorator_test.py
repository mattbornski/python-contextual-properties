import inspect
import os
import sys

test_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
src_dir = os.path.abspath(os.path.join(test_dir, '..', 'contextualproperties'))
sys.path.append(src_dir)

from contextualproperties import properties as properties

@properties(**{
    'integer_contextual_property': 5,
    'string_contextual_property': 'Courier',
})
class ClassUnderTest(object):
    def __init__(self):
        self.direct_property = 'direct'
        self._decorated_property = 'decorated'

    @property
    def decorated_property(self):
        return self._decorated_property
    
    @decorated_property.setter
    def decorated_property(self, value):
        self._decorated_property = value

def test_context():
    obj = ClassUnderTest()

    # Direct and decorated properties are useful
    assert obj.direct_property == 'direct'
    obj.direct_property = obj.direct_property + '_modified'
    assert obj.direct_property == 'direct_modified'
    try:
        with obj.direct_property('this will not work'):
            assert False
    except TypeError:
        pass
    assert obj.direct_property == 'direct_modified'

    assert obj.decorated_property == 'decorated'
    obj.decorated_property = obj.decorated_property + '_modified'
    assert obj.decorated_property == 'decorated_modified'
    try:
        with obj.decorated_property('this will not work'):
            assert False
    except TypeError:
        pass
    assert obj.decorated_property == 'decorated_modified'


    # But contextual properties can be quite nice
    assert obj.integer_contextual_property == 5
    obj.integer_contextual_property = obj.integer_contextual_property * 2
    assert obj.integer_contextual_property == 10
    with obj.integer_contextual_property(999):
        assert obj.integer_contextual_property == 999
    assert obj.integer_contextual_property == 10

    assert obj.string_contextual_property == 'Courier'
    obj.string_contextual_property = obj.string_contextual_property + ' Bold'
    assert obj.string_contextual_property == 'Courier Bold'
    with obj.string_contextual_property('Helvetica'):
        assert obj.string_contextual_property == 'Helvetica'
    assert obj.string_contextual_property == 'Courier Bold'
