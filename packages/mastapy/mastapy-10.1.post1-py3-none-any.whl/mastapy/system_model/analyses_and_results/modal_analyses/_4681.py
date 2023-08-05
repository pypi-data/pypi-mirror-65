'''_4681.py

AssemblyModalAnalysis
'''


from typing import Callable, List

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import _1957
from mastapy.system_model.analyses_and_results.static_loads import _6030
from mastapy.system_model.analyses_and_results.system_deflections import _2189
from mastapy.system_model.analyses_and_results.modal_analyses import (
    _4736, _4682, _4684, _4687,
    _4694, _4693, _4697, _4702,
    _4705, _4716, _4720, _4726,
    _4727, _4735, _4743, _4746,
    _4747, _4748, _4754, _4759,
    _4762, _4763, _4764, _4770,
    _4766, _4771, _4777, _4780,
    _4783, _4786, _4790, _4794,
    _4797, _4806, _4809, _4676
)
from mastapy.system_model.analyses_and_results.modal_analyses.reporting import _4810
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'AssemblyModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyModalAnalysis',)


class AssemblyModalAnalysis(_4676.AbstractAssemblyModalAnalysis):
    '''AssemblyModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def calculate_all_selected_strain_and_kinetic_energies(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'CalculateAllSelectedStrainAndKineticEnergies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CalculateAllSelectedStrainAndKineticEnergies

    @property
    def calculate_all_strain_and_kinetic_energies(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'CalculateAllStrainAndKineticEnergies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CalculateAllStrainAndKineticEnergies

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
    def system_deflection_results(self) -> '_2189.AssemblySystemDeflection':
        '''AssemblySystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2189.AssemblySystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def full_fe_meshes_for_calculating_modes(self) -> 'List[_4736.ImportedFEComponentModalAnalysis]':
        '''List[ImportedFEComponentModalAnalysis]: 'FullFEMeshesForCalculatingModes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FullFEMeshesForCalculatingModes, constructor.new(_4736.ImportedFEComponentModalAnalysis))
        return value

    @property
    def calculate_full_fe_results_by_mode(self) -> 'List[_4810.CalculateFullFEResultsForMode]':
        '''List[CalculateFullFEResultsForMode]: 'CalculateFullFEResultsByMode' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CalculateFullFEResultsByMode, constructor.new(_4810.CalculateFullFEResultsForMode))
        return value

    @property
    def bearings(self) -> 'List[_4682.BearingModalAnalysis]':
        '''List[BearingModalAnalysis]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_4682.BearingModalAnalysis))
        return value

    @property
    def belt_drives(self) -> 'List[_4684.BeltDriveModalAnalysis]':
        '''List[BeltDriveModalAnalysis]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_4684.BeltDriveModalAnalysis))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_4687.BevelDifferentialGearSetModalAnalysis]':
        '''List[BevelDifferentialGearSetModalAnalysis]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_4687.BevelDifferentialGearSetModalAnalysis))
        return value

    @property
    def bolts(self) -> 'List[_4694.BoltModalAnalysis]':
        '''List[BoltModalAnalysis]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_4694.BoltModalAnalysis))
        return value

    @property
    def bolted_joints(self) -> 'List[_4693.BoltedJointModalAnalysis]':
        '''List[BoltedJointModalAnalysis]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_4693.BoltedJointModalAnalysis))
        return value

    @property
    def clutches(self) -> 'List[_4697.ClutchModalAnalysis]':
        '''List[ClutchModalAnalysis]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_4697.ClutchModalAnalysis))
        return value

    @property
    def concept_couplings(self) -> 'List[_4702.ConceptCouplingModalAnalysis]':
        '''List[ConceptCouplingModalAnalysis]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_4702.ConceptCouplingModalAnalysis))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_4705.ConceptGearSetModalAnalysis]':
        '''List[ConceptGearSetModalAnalysis]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_4705.ConceptGearSetModalAnalysis))
        return value

    @property
    def cv_ts(self) -> 'List[_4716.CVTModalAnalysis]':
        '''List[CVTModalAnalysis]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_4716.CVTModalAnalysis))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_4720.CylindricalGearSetModalAnalysis]':
        '''List[CylindricalGearSetModalAnalysis]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_4720.CylindricalGearSetModalAnalysis))
        return value

    @property
    def face_gear_sets(self) -> 'List[_4726.FaceGearSetModalAnalysis]':
        '''List[FaceGearSetModalAnalysis]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_4726.FaceGearSetModalAnalysis))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_4727.FlexiblePinAssemblyModalAnalysis]':
        '''List[FlexiblePinAssemblyModalAnalysis]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_4727.FlexiblePinAssemblyModalAnalysis))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_4735.HypoidGearSetModalAnalysis]':
        '''List[HypoidGearSetModalAnalysis]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_4735.HypoidGearSetModalAnalysis))
        return value

    @property
    def imported_fe_components(self) -> 'List[_4736.ImportedFEComponentModalAnalysis]':
        '''List[ImportedFEComponentModalAnalysis]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_4736.ImportedFEComponentModalAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_4743.KlingelnbergCycloPalloidHypoidGearSetModalAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetModalAnalysis]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_4743.KlingelnbergCycloPalloidHypoidGearSetModalAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_4746.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_4746.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysis))
        return value

    @property
    def mass_discs(self) -> 'List[_4747.MassDiscModalAnalysis]':
        '''List[MassDiscModalAnalysis]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_4747.MassDiscModalAnalysis))
        return value

    @property
    def measurement_components(self) -> 'List[_4748.MeasurementComponentModalAnalysis]':
        '''List[MeasurementComponentModalAnalysis]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_4748.MeasurementComponentModalAnalysis))
        return value

    @property
    def oil_seals(self) -> 'List[_4754.OilSealModalAnalysis]':
        '''List[OilSealModalAnalysis]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_4754.OilSealModalAnalysis))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_4759.PartToPartShearCouplingModalAnalysis]':
        '''List[PartToPartShearCouplingModalAnalysis]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_4759.PartToPartShearCouplingModalAnalysis))
        return value

    @property
    def planet_carriers(self) -> 'List[_4762.PlanetCarrierModalAnalysis]':
        '''List[PlanetCarrierModalAnalysis]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_4762.PlanetCarrierModalAnalysis))
        return value

    @property
    def point_loads(self) -> 'List[_4763.PointLoadModalAnalysis]':
        '''List[PointLoadModalAnalysis]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_4763.PointLoadModalAnalysis))
        return value

    @property
    def power_loads(self) -> 'List[_4764.PowerLoadModalAnalysis]':
        '''List[PowerLoadModalAnalysis]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_4764.PowerLoadModalAnalysis))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_4770.ShaftHubConnectionModalAnalysis]':
        '''List[ShaftHubConnectionModalAnalysis]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_4770.ShaftHubConnectionModalAnalysis))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_4766.RollingRingAssemblyModalAnalysis]':
        '''List[RollingRingAssemblyModalAnalysis]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_4766.RollingRingAssemblyModalAnalysis))
        return value

    @property
    def shafts(self) -> 'List[_4771.ShaftModalAnalysis]':
        '''List[ShaftModalAnalysis]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_4771.ShaftModalAnalysis))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_4777.SpiralBevelGearSetModalAnalysis]':
        '''List[SpiralBevelGearSetModalAnalysis]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_4777.SpiralBevelGearSetModalAnalysis))
        return value

    @property
    def spring_dampers(self) -> 'List[_4780.SpringDamperModalAnalysis]':
        '''List[SpringDamperModalAnalysis]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_4780.SpringDamperModalAnalysis))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_4783.StraightBevelDiffGearSetModalAnalysis]':
        '''List[StraightBevelDiffGearSetModalAnalysis]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_4783.StraightBevelDiffGearSetModalAnalysis))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_4786.StraightBevelGearSetModalAnalysis]':
        '''List[StraightBevelGearSetModalAnalysis]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_4786.StraightBevelGearSetModalAnalysis))
        return value

    @property
    def synchronisers(self) -> 'List[_4790.SynchroniserModalAnalysis]':
        '''List[SynchroniserModalAnalysis]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_4790.SynchroniserModalAnalysis))
        return value

    @property
    def torque_converters(self) -> 'List[_4794.TorqueConverterModalAnalysis]':
        '''List[TorqueConverterModalAnalysis]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_4794.TorqueConverterModalAnalysis))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_4797.UnbalancedMassModalAnalysis]':
        '''List[UnbalancedMassModalAnalysis]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_4797.UnbalancedMassModalAnalysis))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_4806.WormGearSetModalAnalysis]':
        '''List[WormGearSetModalAnalysis]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_4806.WormGearSetModalAnalysis))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_4809.ZerolBevelGearSetModalAnalysis]':
        '''List[ZerolBevelGearSetModalAnalysis]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_4809.ZerolBevelGearSetModalAnalysis))
        return value
