'''_161.py

GearDutyCycleRating
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.gears.rating import (
    _165, _162, _164, _157
)
from mastapy.gears.rating.worm import _178
from mastapy._internal.cast_exception import CastException
from mastapy.gears.rating.face import _252
from mastapy.gears.rating.cylindrical import _264
from mastapy.gears.rating.conical import _327
from mastapy.gears.rating.concept import _338
from mastapy._internal.python_net import python_net_import

_GEAR_DUTY_CYCLE_RATING = python_net_import('SMT.MastaAPI.Gears.Rating', 'GearDutyCycleRating')


__docformat__ = 'restructuredtext en'
__all__ = ('GearDutyCycleRating',)


class GearDutyCycleRating(_157.AbstractGearRating):
    '''GearDutyCycleRating

    This is a mastapy class.
    '''

    TYPE = _GEAR_DUTY_CYCLE_RATING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearDutyCycleRating.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def damage_bending(self) -> 'float':
        '''float: 'DamageBending' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DamageBending

    @property
    def damage_contact(self) -> 'float':
        '''float: 'DamageContact' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.DamageContact

    @property
    def maximum_contact_stress(self) -> 'float':
        '''float: 'MaximumContactStress' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumContactStress

    @property
    def maximum_bending_stress(self) -> 'float':
        '''float: 'MaximumBendingStress' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MaximumBendingStress

    @property
    def gear_set_design_duty_cycle(self) -> '_165.GearSetDutyCycleRating':
        '''GearSetDutyCycleRating: 'GearSetDesignDutyCycle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_165.GearSetDutyCycleRating)(self.wrapped.GearSetDesignDutyCycle) if self.wrapped.GearSetDesignDutyCycle else None

    @property
    def gear_set_design_duty_cycle_of_type_worm_gear_set_duty_cycle_rating(self) -> '_178.WormGearSetDutyCycleRating':
        '''WormGearSetDutyCycleRating: 'GearSetDesignDutyCycle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _178.WormGearSetDutyCycleRating.TYPE not in self.wrapped.GearSetDesignDutyCycle.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design_duty_cycle to WormGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.GearSetDesignDutyCycle.__class__.__qualname__))

        return constructor.new(_178.WormGearSetDutyCycleRating)(self.wrapped.GearSetDesignDutyCycle) if self.wrapped.GearSetDesignDutyCycle else None

    @property
    def gear_set_design_duty_cycle_of_type_face_gear_set_duty_cycle_rating(self) -> '_252.FaceGearSetDutyCycleRating':
        '''FaceGearSetDutyCycleRating: 'GearSetDesignDutyCycle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _252.FaceGearSetDutyCycleRating.TYPE not in self.wrapped.GearSetDesignDutyCycle.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design_duty_cycle to FaceGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.GearSetDesignDutyCycle.__class__.__qualname__))

        return constructor.new(_252.FaceGearSetDutyCycleRating)(self.wrapped.GearSetDesignDutyCycle) if self.wrapped.GearSetDesignDutyCycle else None

    @property
    def gear_set_design_duty_cycle_of_type_cylindrical_gear_set_duty_cycle_rating(self) -> '_264.CylindricalGearSetDutyCycleRating':
        '''CylindricalGearSetDutyCycleRating: 'GearSetDesignDutyCycle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _264.CylindricalGearSetDutyCycleRating.TYPE not in self.wrapped.GearSetDesignDutyCycle.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design_duty_cycle to CylindricalGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.GearSetDesignDutyCycle.__class__.__qualname__))

        return constructor.new(_264.CylindricalGearSetDutyCycleRating)(self.wrapped.GearSetDesignDutyCycle) if self.wrapped.GearSetDesignDutyCycle else None

    @property
    def gear_set_design_duty_cycle_of_type_conical_gear_set_duty_cycle_rating(self) -> '_327.ConicalGearSetDutyCycleRating':
        '''ConicalGearSetDutyCycleRating: 'GearSetDesignDutyCycle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _327.ConicalGearSetDutyCycleRating.TYPE not in self.wrapped.GearSetDesignDutyCycle.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design_duty_cycle to ConicalGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.GearSetDesignDutyCycle.__class__.__qualname__))

        return constructor.new(_327.ConicalGearSetDutyCycleRating)(self.wrapped.GearSetDesignDutyCycle) if self.wrapped.GearSetDesignDutyCycle else None

    @property
    def gear_set_design_duty_cycle_of_type_concept_gear_set_duty_cycle_rating(self) -> '_338.ConceptGearSetDutyCycleRating':
        '''ConceptGearSetDutyCycleRating: 'GearSetDesignDutyCycle' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _338.ConceptGearSetDutyCycleRating.TYPE not in self.wrapped.GearSetDesignDutyCycle.__class__.__mro__:
            raise CastException('Failed to cast gear_set_design_duty_cycle to ConceptGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.GearSetDesignDutyCycle.__class__.__qualname__))

        return constructor.new(_338.ConceptGearSetDutyCycleRating)(self.wrapped.GearSetDesignDutyCycle) if self.wrapped.GearSetDesignDutyCycle else None

    @property
    def left_flank_rating(self) -> '_162.GearFlankRating':
        '''GearFlankRating: 'LeftFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_162.GearFlankRating)(self.wrapped.LeftFlankRating) if self.wrapped.LeftFlankRating else None

    @property
    def right_flank_rating(self) -> '_162.GearFlankRating':
        '''GearFlankRating: 'RightFlankRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_162.GearFlankRating)(self.wrapped.RightFlankRating) if self.wrapped.RightFlankRating else None

    @property
    def gear_ratings(self) -> 'List[_164.GearRating]':
        '''List[GearRating]: 'GearRatings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearRatings, constructor.new(_164.GearRating))
        return value
