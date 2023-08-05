'''_264.py

CylindricalGearSetDutyCycleRating
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy.gears.gear_designs.cylindrical import _787
from mastapy.gears.rating.cylindrical.optimisation import _296
from mastapy.gears.rating.cylindrical import _267
from mastapy.gears.rating import _165
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_DUTY_CYCLE_RATING = python_net_import('SMT.MastaAPI.Gears.Rating.Cylindrical', 'CylindricalGearSetDutyCycleRating')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetDutyCycleRating',)


class CylindricalGearSetDutyCycleRating(_165.GearSetDutyCycleRating):
    '''CylindricalGearSetDutyCycleRating

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_DUTY_CYCLE_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetDutyCycleRating.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def set_profile_shift_to_maximum_safety_factor_fatigue_and_static(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'SetProfileShiftToMaximumSafetyFactorFatigueAndStatic' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SetProfileShiftToMaximumSafetyFactorFatigueAndStatic

    @property
    def cylindrical_gear_set(self) -> '_787.CylindricalGearSetDesign':
        '''CylindricalGearSetDesign: 'CylindricalGearSet' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_787.CylindricalGearSetDesign)(self.wrapped.CylindricalGearSet) if self.wrapped.CylindricalGearSet else None

    @property
    def optimisations(self) -> '_296.CylindricalGearSetRatingOptimisationHelper':
        '''CylindricalGearSetRatingOptimisationHelper: 'Optimisations' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_296.CylindricalGearSetRatingOptimisationHelper)(self.wrapped.Optimisations) if self.wrapped.Optimisations else None

    @property
    def gear_mesh_duty_cycle_ratings(self) -> 'List[_267.CylindricalMeshDutyCycleRating]':
        '''List[CylindricalMeshDutyCycleRating]: 'GearMeshDutyCycleRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearMeshDutyCycleRatings, constructor.new(_267.CylindricalMeshDutyCycleRating))
        return value

    @property
    def cylindrical_mesh_duty_cycle_ratings(self) -> 'List[_267.CylindricalMeshDutyCycleRating]':
        '''List[CylindricalMeshDutyCycleRating]: 'CylindricalMeshDutyCycleRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalMeshDutyCycleRatings, constructor.new(_267.CylindricalMeshDutyCycleRating))
        return value
