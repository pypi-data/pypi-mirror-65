'''_3703.py

AssemblyModalAnalysesAtStiffnesses
'''


from typing import List

from mastapy.system_model.part_model import _1957
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6030
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import (
    _3704, _3706, _3709, _3716,
    _3715, _3719, _3724, _3727,
    _3738, _3742, _3748, _3749,
    _3756, _3757, _3764, _3767,
    _3768, _3769, _3773, _3777,
    _3780, _3781, _3782, _3788,
    _3784, _3789, _3794, _3797,
    _3800, _3803, _3807, _3811,
    _3814, _3818, _3821, _3698
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'AssemblyModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyModalAnalysesAtStiffnesses',)


class AssemblyModalAnalysesAtStiffnesses(_3698.AbstractAssemblyModalAnalysesAtStiffnesses):
    '''AssemblyModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1957.Assembly':
        '''Assembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1957.Assembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6030.AssemblyLoadCase':
        '''AssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6030.AssemblyLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def bearings(self) -> 'List[_3704.BearingModalAnalysesAtStiffnesses]':
        '''List[BearingModalAnalysesAtStiffnesses]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_3704.BearingModalAnalysesAtStiffnesses))
        return value

    @property
    def belt_drives(self) -> 'List[_3706.BeltDriveModalAnalysesAtStiffnesses]':
        '''List[BeltDriveModalAnalysesAtStiffnesses]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_3706.BeltDriveModalAnalysesAtStiffnesses))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_3709.BevelDifferentialGearSetModalAnalysesAtStiffnesses]':
        '''List[BevelDifferentialGearSetModalAnalysesAtStiffnesses]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_3709.BevelDifferentialGearSetModalAnalysesAtStiffnesses))
        return value

    @property
    def bolts(self) -> 'List[_3716.BoltModalAnalysesAtStiffnesses]':
        '''List[BoltModalAnalysesAtStiffnesses]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_3716.BoltModalAnalysesAtStiffnesses))
        return value

    @property
    def bolted_joints(self) -> 'List[_3715.BoltedJointModalAnalysesAtStiffnesses]':
        '''List[BoltedJointModalAnalysesAtStiffnesses]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_3715.BoltedJointModalAnalysesAtStiffnesses))
        return value

    @property
    def clutches(self) -> 'List[_3719.ClutchModalAnalysesAtStiffnesses]':
        '''List[ClutchModalAnalysesAtStiffnesses]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_3719.ClutchModalAnalysesAtStiffnesses))
        return value

    @property
    def concept_couplings(self) -> 'List[_3724.ConceptCouplingModalAnalysesAtStiffnesses]':
        '''List[ConceptCouplingModalAnalysesAtStiffnesses]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_3724.ConceptCouplingModalAnalysesAtStiffnesses))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_3727.ConceptGearSetModalAnalysesAtStiffnesses]':
        '''List[ConceptGearSetModalAnalysesAtStiffnesses]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_3727.ConceptGearSetModalAnalysesAtStiffnesses))
        return value

    @property
    def cv_ts(self) -> 'List[_3738.CVTModalAnalysesAtStiffnesses]':
        '''List[CVTModalAnalysesAtStiffnesses]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_3738.CVTModalAnalysesAtStiffnesses))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_3742.CylindricalGearSetModalAnalysesAtStiffnesses]':
        '''List[CylindricalGearSetModalAnalysesAtStiffnesses]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_3742.CylindricalGearSetModalAnalysesAtStiffnesses))
        return value

    @property
    def face_gear_sets(self) -> 'List[_3748.FaceGearSetModalAnalysesAtStiffnesses]':
        '''List[FaceGearSetModalAnalysesAtStiffnesses]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_3748.FaceGearSetModalAnalysesAtStiffnesses))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_3749.FlexiblePinAssemblyModalAnalysesAtStiffnesses]':
        '''List[FlexiblePinAssemblyModalAnalysesAtStiffnesses]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_3749.FlexiblePinAssemblyModalAnalysesAtStiffnesses))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_3756.HypoidGearSetModalAnalysesAtStiffnesses]':
        '''List[HypoidGearSetModalAnalysesAtStiffnesses]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_3756.HypoidGearSetModalAnalysesAtStiffnesses))
        return value

    @property
    def imported_fe_components(self) -> 'List[_3757.ImportedFEComponentModalAnalysesAtStiffnesses]':
        '''List[ImportedFEComponentModalAnalysesAtStiffnesses]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_3757.ImportedFEComponentModalAnalysesAtStiffnesses))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_3764.KlingelnbergCycloPalloidHypoidGearSetModalAnalysesAtStiffnesses]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetModalAnalysesAtStiffnesses]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_3764.KlingelnbergCycloPalloidHypoidGearSetModalAnalysesAtStiffnesses))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_3767.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysesAtStiffnesses]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysesAtStiffnesses]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_3767.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysesAtStiffnesses))
        return value

    @property
    def mass_discs(self) -> 'List[_3768.MassDiscModalAnalysesAtStiffnesses]':
        '''List[MassDiscModalAnalysesAtStiffnesses]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_3768.MassDiscModalAnalysesAtStiffnesses))
        return value

    @property
    def measurement_components(self) -> 'List[_3769.MeasurementComponentModalAnalysesAtStiffnesses]':
        '''List[MeasurementComponentModalAnalysesAtStiffnesses]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_3769.MeasurementComponentModalAnalysesAtStiffnesses))
        return value

    @property
    def oil_seals(self) -> 'List[_3773.OilSealModalAnalysesAtStiffnesses]':
        '''List[OilSealModalAnalysesAtStiffnesses]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_3773.OilSealModalAnalysesAtStiffnesses))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_3777.PartToPartShearCouplingModalAnalysesAtStiffnesses]':
        '''List[PartToPartShearCouplingModalAnalysesAtStiffnesses]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_3777.PartToPartShearCouplingModalAnalysesAtStiffnesses))
        return value

    @property
    def planet_carriers(self) -> 'List[_3780.PlanetCarrierModalAnalysesAtStiffnesses]':
        '''List[PlanetCarrierModalAnalysesAtStiffnesses]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_3780.PlanetCarrierModalAnalysesAtStiffnesses))
        return value

    @property
    def point_loads(self) -> 'List[_3781.PointLoadModalAnalysesAtStiffnesses]':
        '''List[PointLoadModalAnalysesAtStiffnesses]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_3781.PointLoadModalAnalysesAtStiffnesses))
        return value

    @property
    def power_loads(self) -> 'List[_3782.PowerLoadModalAnalysesAtStiffnesses]':
        '''List[PowerLoadModalAnalysesAtStiffnesses]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_3782.PowerLoadModalAnalysesAtStiffnesses))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_3788.ShaftHubConnectionModalAnalysesAtStiffnesses]':
        '''List[ShaftHubConnectionModalAnalysesAtStiffnesses]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_3788.ShaftHubConnectionModalAnalysesAtStiffnesses))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_3784.RollingRingAssemblyModalAnalysesAtStiffnesses]':
        '''List[RollingRingAssemblyModalAnalysesAtStiffnesses]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_3784.RollingRingAssemblyModalAnalysesAtStiffnesses))
        return value

    @property
    def shafts(self) -> 'List[_3789.ShaftModalAnalysesAtStiffnesses]':
        '''List[ShaftModalAnalysesAtStiffnesses]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_3789.ShaftModalAnalysesAtStiffnesses))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_3794.SpiralBevelGearSetModalAnalysesAtStiffnesses]':
        '''List[SpiralBevelGearSetModalAnalysesAtStiffnesses]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_3794.SpiralBevelGearSetModalAnalysesAtStiffnesses))
        return value

    @property
    def spring_dampers(self) -> 'List[_3797.SpringDamperModalAnalysesAtStiffnesses]':
        '''List[SpringDamperModalAnalysesAtStiffnesses]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_3797.SpringDamperModalAnalysesAtStiffnesses))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_3800.StraightBevelDiffGearSetModalAnalysesAtStiffnesses]':
        '''List[StraightBevelDiffGearSetModalAnalysesAtStiffnesses]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_3800.StraightBevelDiffGearSetModalAnalysesAtStiffnesses))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_3803.StraightBevelGearSetModalAnalysesAtStiffnesses]':
        '''List[StraightBevelGearSetModalAnalysesAtStiffnesses]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_3803.StraightBevelGearSetModalAnalysesAtStiffnesses))
        return value

    @property
    def synchronisers(self) -> 'List[_3807.SynchroniserModalAnalysesAtStiffnesses]':
        '''List[SynchroniserModalAnalysesAtStiffnesses]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_3807.SynchroniserModalAnalysesAtStiffnesses))
        return value

    @property
    def torque_converters(self) -> 'List[_3811.TorqueConverterModalAnalysesAtStiffnesses]':
        '''List[TorqueConverterModalAnalysesAtStiffnesses]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_3811.TorqueConverterModalAnalysesAtStiffnesses))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_3814.UnbalancedMassModalAnalysesAtStiffnesses]':
        '''List[UnbalancedMassModalAnalysesAtStiffnesses]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_3814.UnbalancedMassModalAnalysesAtStiffnesses))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_3818.WormGearSetModalAnalysesAtStiffnesses]':
        '''List[WormGearSetModalAnalysesAtStiffnesses]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_3818.WormGearSetModalAnalysesAtStiffnesses))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_3821.ZerolBevelGearSetModalAnalysesAtStiffnesses]':
        '''List[ZerolBevelGearSetModalAnalysesAtStiffnesses]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_3821.ZerolBevelGearSetModalAnalysesAtStiffnesses))
        return value
