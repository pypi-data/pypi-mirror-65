'''_204.py

StraightBevelGearSetRating
'''


from typing import List

from mastapy.gears.gear_designs.straight_bevel import _732
from mastapy._internal import constructor, conversion
from mastapy.gears.rating.straight_bevel import _202, _203
from mastapy.gears.rating.bevel import _342
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_SET_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.StraightBevel', 'StraightBevelGearSetRating')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearSetRating',)


class StraightBevelGearSetRating(_342.BevelGearSetRating):
    '''StraightBevelGearSetRating

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_SET_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearSetRating.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def straight_bevel_gear_set(self) -> '_732.StraightBevelGearSetDesign':
        '''StraightBevelGearSetDesign: 'StraightBevelGearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_732.StraightBevelGearSetDesign)(self.wrapped.StraightBevelGearSet) if self.wrapped.StraightBevelGearSet else None

    @property
    def straight_bevel_mesh_ratings(self) -> 'List[_202.StraightBevelGearMeshRating]':
        '''List[StraightBevelGearMeshRating]: 'StraightBevelMeshRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelMeshRatings, constructor.new(_202.StraightBevelGearMeshRating))
        return value

    @property
    def straight_bevel_gear_ratings(self) -> 'List[_203.StraightBevelGearRating]':
        '''List[StraightBevelGearRating]: 'StraightBevelGearRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearRatings, constructor.new(_203.StraightBevelGearRating))
        return value
