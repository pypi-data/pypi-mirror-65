'''_1964.py

Bolt
'''


from mastapy.bolts import _1040
from mastapy._internal import constructor
from mastapy.system_model.part_model import _1965, _1966
from mastapy._internal.python_net import python_net_import

_BOLT = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Bolt')


__docformat__ = 'restructuredtext en'
__all__ = ('Bolt',)


class Bolt(_1966.Component):
    '''Bolt

    This is a mastapy class.
    '''

    TYPE = _BOLT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Bolt.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def loaded_bolt(self) -> '_1040.LoadedBolt':
        '''LoadedBolt: 'LoadedBolt' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1040.LoadedBolt)(self.wrapped.LoadedBolt) if self.wrapped.LoadedBolt else None

    @property
    def bolted_joint(self) -> '_1965.BoltedJoint':
        '''BoltedJoint: 'BoltedJoint' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1965.BoltedJoint)(self.wrapped.BoltedJoint) if self.wrapped.BoltedJoint else None
