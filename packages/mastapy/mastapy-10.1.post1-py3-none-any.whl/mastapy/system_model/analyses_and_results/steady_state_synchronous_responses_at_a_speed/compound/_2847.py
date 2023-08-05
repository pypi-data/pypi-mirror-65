'''_2847.py

AssemblyCompoundSteadyStateSynchronousResponseAtASpeed
'''


from typing import List

from mastapy.system_model.part_model import _1979
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import _2725
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed.compound import (
    _2848, _2850, _2853, _2859,
    _2860, _2861, _2866, _2871,
    _2881, _2885, _2891, _2892,
    _2899, _2900, _2907, _2910,
    _2911, _2912, _2914, _2916,
    _2921, _2922, _2923, _2930,
    _2925, _2929, _2935, _2936,
    _2941, _2944, _2947, _2951,
    _2955, _2959, _2962, _2842
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed.Compound', 'AssemblyCompoundSteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundSteadyStateSynchronousResponseAtASpeed',)


class AssemblyCompoundSteadyStateSynchronousResponseAtASpeed(_2842.AbstractAssemblyCompoundSteadyStateSynchronousResponseAtASpeed):
    '''AssemblyCompoundSteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundSteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1979.Assembly':
        '''Assembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1979.Assembly)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1979.Assembly':
        '''Assembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1979.Assembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_2725.AssemblySteadyStateSynchronousResponseAtASpeed]':
        '''List[AssemblySteadyStateSynchronousResponseAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_2725.AssemblySteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def assembly_steady_state_synchronous_response_at_a_speed_load_cases(self) -> 'List[_2725.AssemblySteadyStateSynchronousResponseAtASpeed]':
        '''List[AssemblySteadyStateSynchronousResponseAtASpeed]: 'AssemblySteadyStateSynchronousResponseAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySteadyStateSynchronousResponseAtASpeedLoadCases, constructor.new(_2725.AssemblySteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def bearings(self) -> 'List[_2848.BearingCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[BearingCompoundSteadyStateSynchronousResponseAtASpeed]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_2848.BearingCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def belt_drives(self) -> 'List[_2850.BeltDriveCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[BeltDriveCompoundSteadyStateSynchronousResponseAtASpeed]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_2850.BeltDriveCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_2853.BevelDifferentialGearSetCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[BevelDifferentialGearSetCompoundSteadyStateSynchronousResponseAtASpeed]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_2853.BevelDifferentialGearSetCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def bolts(self) -> 'List[_2859.BoltCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[BoltCompoundSteadyStateSynchronousResponseAtASpeed]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_2859.BoltCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def bolted_joints(self) -> 'List[_2860.BoltedJointCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[BoltedJointCompoundSteadyStateSynchronousResponseAtASpeed]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_2860.BoltedJointCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def clutches(self) -> 'List[_2861.ClutchCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[ClutchCompoundSteadyStateSynchronousResponseAtASpeed]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_2861.ClutchCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def concept_couplings(self) -> 'List[_2866.ConceptCouplingCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[ConceptCouplingCompoundSteadyStateSynchronousResponseAtASpeed]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_2866.ConceptCouplingCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_2871.ConceptGearSetCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[ConceptGearSetCompoundSteadyStateSynchronousResponseAtASpeed]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_2871.ConceptGearSetCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def cv_ts(self) -> 'List[_2881.CVTCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[CVTCompoundSteadyStateSynchronousResponseAtASpeed]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_2881.CVTCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_2885.CylindricalGearSetCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[CylindricalGearSetCompoundSteadyStateSynchronousResponseAtASpeed]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_2885.CylindricalGearSetCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def face_gear_sets(self) -> 'List[_2891.FaceGearSetCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[FaceGearSetCompoundSteadyStateSynchronousResponseAtASpeed]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_2891.FaceGearSetCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_2892.FlexiblePinAssemblyCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[FlexiblePinAssemblyCompoundSteadyStateSynchronousResponseAtASpeed]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_2892.FlexiblePinAssemblyCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_2899.HypoidGearSetCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[HypoidGearSetCompoundSteadyStateSynchronousResponseAtASpeed]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_2899.HypoidGearSetCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def imported_fe_components(self) -> 'List[_2900.ImportedFEComponentCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[ImportedFEComponentCompoundSteadyStateSynchronousResponseAtASpeed]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_2900.ImportedFEComponentCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_2907.KlingelnbergCycloPalloidHypoidGearSetCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundSteadyStateSynchronousResponseAtASpeed]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_2907.KlingelnbergCycloPalloidHypoidGearSetCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_2910.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_2910.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def mass_discs(self) -> 'List[_2911.MassDiscCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[MassDiscCompoundSteadyStateSynchronousResponseAtASpeed]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_2911.MassDiscCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def measurement_components(self) -> 'List[_2912.MeasurementComponentCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[MeasurementComponentCompoundSteadyStateSynchronousResponseAtASpeed]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_2912.MeasurementComponentCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def oil_seals(self) -> 'List[_2914.OilSealCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[OilSealCompoundSteadyStateSynchronousResponseAtASpeed]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_2914.OilSealCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_2916.PartToPartShearCouplingCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[PartToPartShearCouplingCompoundSteadyStateSynchronousResponseAtASpeed]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_2916.PartToPartShearCouplingCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def planet_carriers(self) -> 'List[_2921.PlanetCarrierCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[PlanetCarrierCompoundSteadyStateSynchronousResponseAtASpeed]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_2921.PlanetCarrierCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def point_loads(self) -> 'List[_2922.PointLoadCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[PointLoadCompoundSteadyStateSynchronousResponseAtASpeed]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_2922.PointLoadCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def power_loads(self) -> 'List[_2923.PowerLoadCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[PowerLoadCompoundSteadyStateSynchronousResponseAtASpeed]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_2923.PowerLoadCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_2930.ShaftHubConnectionCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[ShaftHubConnectionCompoundSteadyStateSynchronousResponseAtASpeed]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_2930.ShaftHubConnectionCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_2925.RollingRingAssemblyCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[RollingRingAssemblyCompoundSteadyStateSynchronousResponseAtASpeed]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_2925.RollingRingAssemblyCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def shafts(self) -> 'List[_2929.ShaftCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[ShaftCompoundSteadyStateSynchronousResponseAtASpeed]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_2929.ShaftCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_2935.SpiralBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[SpiralBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_2935.SpiralBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def spring_dampers(self) -> 'List[_2936.SpringDamperCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[SpringDamperCompoundSteadyStateSynchronousResponseAtASpeed]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_2936.SpringDamperCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_2941.StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponseAtASpeed]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_2941.StraightBevelDiffGearSetCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_2944.StraightBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[StraightBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_2944.StraightBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def synchronisers(self) -> 'List[_2947.SynchroniserCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[SynchroniserCompoundSteadyStateSynchronousResponseAtASpeed]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_2947.SynchroniserCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def torque_converters(self) -> 'List[_2951.TorqueConverterCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[TorqueConverterCompoundSteadyStateSynchronousResponseAtASpeed]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_2951.TorqueConverterCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_2955.UnbalancedMassCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[UnbalancedMassCompoundSteadyStateSynchronousResponseAtASpeed]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_2955.UnbalancedMassCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_2959.WormGearSetCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[WormGearSetCompoundSteadyStateSynchronousResponseAtASpeed]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_2959.WormGearSetCompoundSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_2962.ZerolBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed]':
        '''List[ZerolBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_2962.ZerolBevelGearSetCompoundSteadyStateSynchronousResponseAtASpeed))
        return value
