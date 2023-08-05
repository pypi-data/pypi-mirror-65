'''_733.py

SpiralBevelGearMeshDesign
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.spiral_bevel import _734, _732, _735
from mastapy.gears.gear_designs.bevel import _913
from mastapy._internal.python_net import python_net_import

_SPIRAL_BEVEL_GEAR_MESH_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns.SpiralBevel', 'SpiralBevelGearMeshDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('SpiralBevelGearMeshDesign',)


class SpiralBevelGearMeshDesign(_913.BevelGearMeshDesign):
    '''SpiralBevelGearMeshDesign

    This is a mastapy class.
    '''

    TYPE = _SPIRAL_BEVEL_GEAR_MESH_DESIGN

    __hash__ = None

    def __init__(self, instance_to_wrap: 'SpiralBevelGearMeshDesign.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def wheel_inner_blade_angle_convex(self) -> 'float':
        '''float: 'WheelInnerBladeAngleConvex' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.WheelInnerBladeAngleConvex

    @property
    def wheel_outer_blade_angle_concave(self) -> 'float':
        '''float: 'WheelOuterBladeAngleConcave' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.WheelOuterBladeAngleConcave

    @property
    def spiral_bevel_gear_set(self) -> '_734.SpiralBevelGearSetDesign':
        '''SpiralBevelGearSetDesign: 'SpiralBevelGearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_734.SpiralBevelGearSetDesign)(self.wrapped.SpiralBevelGearSet) if self.wrapped.SpiralBevelGearSet else None

    @property
    def spiral_bevel_gears(self) -> 'List[_732.SpiralBevelGearDesign]':
        '''List[SpiralBevelGearDesign]: 'SpiralBevelGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGears, constructor.new(_732.SpiralBevelGearDesign))
        return value

    @property
    def spiral_bevel_meshed_gears(self) -> 'List[_735.SpiralBevelMeshedGearDesign]':
        '''List[SpiralBevelMeshedGearDesign]: 'SpiralBevelMeshedGears' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelMeshedGears, constructor.new(_735.SpiralBevelMeshedGearDesign))
        return value
