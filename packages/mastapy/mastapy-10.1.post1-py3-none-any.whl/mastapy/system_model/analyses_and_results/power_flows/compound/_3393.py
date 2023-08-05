'''_3393.py

GearMeshCompoundPowerFlow
'''


from mastapy.gears.rating import _168
from mastapy._internal import constructor
from mastapy.gears.rating.worm import _180
from mastapy._internal.cast_exception import CastException
from mastapy.gears.rating.face import _249
from mastapy.gears.rating.cylindrical import _267
from mastapy.gears.rating.conical import _330
from mastapy.gears.rating.concept import _335
from mastapy.system_model.analyses_and_results.power_flows.compound import _3400
from mastapy._internal.python_net import python_net_import

_GEAR_MESH_COMPOUND_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows.Compound', 'GearMeshCompoundPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMeshCompoundPowerFlow',)


class GearMeshCompoundPowerFlow(_3400.InterMountableComponentConnectionCompoundPowerFlow):
    '''GearMeshCompoundPowerFlow

    This is a mastapy class.
    '''

    TYPE = _GEAR_MESH_COMPOUND_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearMeshCompoundPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def gear_mesh_duty_cycle_rating(self) -> '_168.MeshDutyCycleRating':
        '''MeshDutyCycleRating: 'GearMeshDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_168.MeshDutyCycleRating)(self.wrapped.GearMeshDutyCycleRating) if self.wrapped.GearMeshDutyCycleRating else None

    @property
    def gear_mesh_duty_cycle_rating_of_type_worm_mesh_duty_cycle_rating(self) -> '_180.WormMeshDutyCycleRating':
        '''WormMeshDutyCycleRating: 'GearMeshDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _180.WormMeshDutyCycleRating.TYPE not in self.wrapped.GearMeshDutyCycleRating.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh_duty_cycle_rating to WormMeshDutyCycleRating. Expected: {}.'.format(self.wrapped.GearMeshDutyCycleRating.__class__.__qualname__))

        return constructor.new(_180.WormMeshDutyCycleRating)(self.wrapped.GearMeshDutyCycleRating) if self.wrapped.GearMeshDutyCycleRating else None

    @property
    def gear_mesh_duty_cycle_rating_of_type_face_gear_mesh_duty_cycle_rating(self) -> '_249.FaceGearMeshDutyCycleRating':
        '''FaceGearMeshDutyCycleRating: 'GearMeshDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _249.FaceGearMeshDutyCycleRating.TYPE not in self.wrapped.GearMeshDutyCycleRating.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh_duty_cycle_rating to FaceGearMeshDutyCycleRating. Expected: {}.'.format(self.wrapped.GearMeshDutyCycleRating.__class__.__qualname__))

        return constructor.new(_249.FaceGearMeshDutyCycleRating)(self.wrapped.GearMeshDutyCycleRating) if self.wrapped.GearMeshDutyCycleRating else None

    @property
    def gear_mesh_duty_cycle_rating_of_type_cylindrical_mesh_duty_cycle_rating(self) -> '_267.CylindricalMeshDutyCycleRating':
        '''CylindricalMeshDutyCycleRating: 'GearMeshDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _267.CylindricalMeshDutyCycleRating.TYPE not in self.wrapped.GearMeshDutyCycleRating.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh_duty_cycle_rating to CylindricalMeshDutyCycleRating. Expected: {}.'.format(self.wrapped.GearMeshDutyCycleRating.__class__.__qualname__))

        return constructor.new(_267.CylindricalMeshDutyCycleRating)(self.wrapped.GearMeshDutyCycleRating) if self.wrapped.GearMeshDutyCycleRating else None

    @property
    def gear_mesh_duty_cycle_rating_of_type_conical_mesh_duty_cycle_rating(self) -> '_330.ConicalMeshDutyCycleRating':
        '''ConicalMeshDutyCycleRating: 'GearMeshDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _330.ConicalMeshDutyCycleRating.TYPE not in self.wrapped.GearMeshDutyCycleRating.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh_duty_cycle_rating to ConicalMeshDutyCycleRating. Expected: {}.'.format(self.wrapped.GearMeshDutyCycleRating.__class__.__qualname__))

        return constructor.new(_330.ConicalMeshDutyCycleRating)(self.wrapped.GearMeshDutyCycleRating) if self.wrapped.GearMeshDutyCycleRating else None

    @property
    def gear_mesh_duty_cycle_rating_of_type_concept_gear_mesh_duty_cycle_rating(self) -> '_335.ConceptGearMeshDutyCycleRating':
        '''ConceptGearMeshDutyCycleRating: 'GearMeshDutyCycleRating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _335.ConceptGearMeshDutyCycleRating.TYPE not in self.wrapped.GearMeshDutyCycleRating.__class__.__mro__:
            raise CastException('Failed to cast gear_mesh_duty_cycle_rating to ConceptGearMeshDutyCycleRating. Expected: {}.'.format(self.wrapped.GearMeshDutyCycleRating.__class__.__qualname__))

        return constructor.new(_335.ConceptGearMeshDutyCycleRating)(self.wrapped.GearMeshDutyCycleRating) if self.wrapped.GearMeshDutyCycleRating else None
