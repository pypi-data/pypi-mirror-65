'''_3392.py

GearCompoundPowerFlow
'''


from mastapy.gears.rating import _161
from mastapy._internal import constructor
from mastapy.gears.rating.worm import _175
from mastapy._internal.cast_exception import CastException
from mastapy.gears.rating.face import _248
from mastapy.gears.rating.cylindrical import _255
from mastapy.gears.rating.conical import _324
from mastapy.gears.rating.concept import _334
from mastapy.system_model.analyses_and_results.power_flows.compound import _3412
from mastapy._internal.python_net import python_net_import

_GEAR_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'GearCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('GearCompoundPowerFlow',)


class GearCompoundPowerFlow(_3412.MountableComponentCompoundPowerFlow):
    '''GearCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _GEAR_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def gear_duty_cycle_rating(self) -> '_161.GearDutyCycleRating':
        '''GearDutyCycleRating: 'GearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_161.GearDutyCycleRating)(self.wrapped.GearDutyCycleRating) if self.wrapped.GearDutyCycleRating else None

    @property
    def gear_duty_cycle_rating_of_type_worm_gear_duty_cycle_rating(self) -> '_175.WormGearDutyCycleRating':
        '''WormGearDutyCycleRating: 'GearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _175.WormGearDutyCycleRating.TYPE not in self.wrapped.GearDutyCycleRating.__class__.__mro__:
            raise CastException('Failed to cast gear_duty_cycle_rating to WormGearDutyCycleRating. Expected: {}.'.format(self.wrapped.GearDutyCycleRating.__class__.__qualname__))

        return constructor.new(_175.WormGearDutyCycleRating)(self.wrapped.GearDutyCycleRating) if self.wrapped.GearDutyCycleRating else None

    @property
    def gear_duty_cycle_rating_of_type_face_gear_duty_cycle_rating(self) -> '_248.FaceGearDutyCycleRating':
        '''FaceGearDutyCycleRating: 'GearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _248.FaceGearDutyCycleRating.TYPE not in self.wrapped.GearDutyCycleRating.__class__.__mro__:
            raise CastException('Failed to cast gear_duty_cycle_rating to FaceGearDutyCycleRating. Expected: {}.'.format(self.wrapped.GearDutyCycleRating.__class__.__qualname__))

        return constructor.new(_248.FaceGearDutyCycleRating)(self.wrapped.GearDutyCycleRating) if self.wrapped.GearDutyCycleRating else None

    @property
    def gear_duty_cycle_rating_of_type_cylindrical_gear_duty_cycle_rating(self) -> '_255.CylindricalGearDutyCycleRating':
        '''CylindricalGearDutyCycleRating: 'GearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _255.CylindricalGearDutyCycleRating.TYPE not in self.wrapped.GearDutyCycleRating.__class__.__mro__:
            raise CastException('Failed to cast gear_duty_cycle_rating to CylindricalGearDutyCycleRating. Expected: {}.'.format(self.wrapped.GearDutyCycleRating.__class__.__qualname__))

        return constructor.new(_255.CylindricalGearDutyCycleRating)(self.wrapped.GearDutyCycleRating) if self.wrapped.GearDutyCycleRating else None

    @property
    def gear_duty_cycle_rating_of_type_conical_gear_duty_cycle_rating(self) -> '_324.ConicalGearDutyCycleRating':
        '''ConicalGearDutyCycleRating: 'GearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _324.ConicalGearDutyCycleRating.TYPE not in self.wrapped.GearDutyCycleRating.__class__.__mro__:
            raise CastException('Failed to cast gear_duty_cycle_rating to ConicalGearDutyCycleRating. Expected: {}.'.format(self.wrapped.GearDutyCycleRating.__class__.__qualname__))

        return constructor.new(_324.ConicalGearDutyCycleRating)(self.wrapped.GearDutyCycleRating) if self.wrapped.GearDutyCycleRating else None

    @property
    def gear_duty_cycle_rating_of_type_concept_gear_duty_cycle_rating(self) -> '_334.ConceptGearDutyCycleRating':
        '''ConceptGearDutyCycleRating: 'GearDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _334.ConceptGearDutyCycleRating.TYPE not in self.wrapped.GearDutyCycleRating.__class__.__mro__:
            raise CastException('Failed to cast gear_duty_cycle_rating to ConceptGearDutyCycleRating. Expected: {}.'.format(self.wrapped.GearDutyCycleRating.__class__.__qualname__))

        return constructor.new(_334.ConceptGearDutyCycleRating)(self.wrapped.GearDutyCycleRating) if self.wrapped.GearDutyCycleRating else None
