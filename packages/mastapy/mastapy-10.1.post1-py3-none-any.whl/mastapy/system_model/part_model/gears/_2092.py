'''_2092.py

ZerolBevelGearSet
'''


from typing import List

from mastapy.gears.gear_designs.zerol_bevel import _719
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.gears import _2091, _2058
from mastapy.system_model.connections_and_sockets.gears import _1891
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ZerolBevelGearSet')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSet',)


class ZerolBevelGearSet(_2058.BevelGearSet):
    '''ZerolBevelGearSet

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSet.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def conical_gear_set_design(self) -> '_719.ZerolBevelGearSetDesign':
        '''ZerolBevelGearSetDesign: 'ConicalGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_719.ZerolBevelGearSetDesign)(self.wrapped.ConicalGearSetDesign) if self.wrapped.ConicalGearSetDesign else None

    @property
    def zerol_bevel_gear_set_design(self) -> '_719.ZerolBevelGearSetDesign':
        '''ZerolBevelGearSetDesign: 'ZerolBevelGearSetDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_719.ZerolBevelGearSetDesign)(self.wrapped.ZerolBevelGearSetDesign) if self.wrapped.ZerolBevelGearSetDesign else None

    @property
    def zerol_bevel_gears(self) -> 'List[_2091.ZerolBevelGear]':
        '''List[ZerolBevelGear]: 'ZerolBevelGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGears, constructor.new(_2091.ZerolBevelGear))
        return value

    @property
    def zerol_bevel_meshes(self) -> 'List[_1891.ZerolBevelGearMesh]':
        '''List[ZerolBevelGearMesh]: 'ZerolBevelMeshes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshes, constructor.new(_1891.ZerolBevelGearMesh))
        return value
