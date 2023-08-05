'''_2460.py

AssemblySteadyStateSynchronousResponseOnAShaft
'''


from typing import List

from mastapy.system_model.part_model import _1957
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6030
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_on_a_shaft import (
    _2461, _2463, _2465, _2473,
    _2472, _2476, _2481, _2483,
    _2495, _2497, _2503, _2505,
    _2511, _2513, _2519, _2522,
    _2524, _2525, _2527, _2531,
    _2534, _2535, _2536, _2542,
    _2538, _2543, _2547, _2551,
    _2554, _2557, _2564, _2567,
    _2569, _2572, _2575, _2455
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesOnAShaft', 'AssemblySteadyStateSynchronousResponseOnAShaft')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblySteadyStateSynchronousResponseOnAShaft',)


class AssemblySteadyStateSynchronousResponseOnAShaft(_2455.AbstractAssemblySteadyStateSynchronousResponseOnAShaft):
    '''AssemblySteadyStateSynchronousResponseOnAShaft

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_STEADY_STATE_SYNCHRONOUS_RESPONSE_ON_A_SHAFT

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblySteadyStateSynchronousResponseOnAShaft.TYPE'):
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
    def bearings(self) -> 'List[_2461.BearingSteadyStateSynchronousResponseOnAShaft]':
        '''List[BearingSteadyStateSynchronousResponseOnAShaft]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_2461.BearingSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def belt_drives(self) -> 'List[_2463.BeltDriveSteadyStateSynchronousResponseOnAShaft]':
        '''List[BeltDriveSteadyStateSynchronousResponseOnAShaft]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_2463.BeltDriveSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_2465.BevelDifferentialGearSetSteadyStateSynchronousResponseOnAShaft]':
        '''List[BevelDifferentialGearSetSteadyStateSynchronousResponseOnAShaft]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_2465.BevelDifferentialGearSetSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def bolts(self) -> 'List[_2473.BoltSteadyStateSynchronousResponseOnAShaft]':
        '''List[BoltSteadyStateSynchronousResponseOnAShaft]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_2473.BoltSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def bolted_joints(self) -> 'List[_2472.BoltedJointSteadyStateSynchronousResponseOnAShaft]':
        '''List[BoltedJointSteadyStateSynchronousResponseOnAShaft]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_2472.BoltedJointSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def clutches(self) -> 'List[_2476.ClutchSteadyStateSynchronousResponseOnAShaft]':
        '''List[ClutchSteadyStateSynchronousResponseOnAShaft]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_2476.ClutchSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def concept_couplings(self) -> 'List[_2481.ConceptCouplingSteadyStateSynchronousResponseOnAShaft]':
        '''List[ConceptCouplingSteadyStateSynchronousResponseOnAShaft]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_2481.ConceptCouplingSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_2483.ConceptGearSetSteadyStateSynchronousResponseOnAShaft]':
        '''List[ConceptGearSetSteadyStateSynchronousResponseOnAShaft]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_2483.ConceptGearSetSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def cv_ts(self) -> 'List[_2495.CVTSteadyStateSynchronousResponseOnAShaft]':
        '''List[CVTSteadyStateSynchronousResponseOnAShaft]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_2495.CVTSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_2497.CylindricalGearSetSteadyStateSynchronousResponseOnAShaft]':
        '''List[CylindricalGearSetSteadyStateSynchronousResponseOnAShaft]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_2497.CylindricalGearSetSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def face_gear_sets(self) -> 'List[_2503.FaceGearSetSteadyStateSynchronousResponseOnAShaft]':
        '''List[FaceGearSetSteadyStateSynchronousResponseOnAShaft]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_2503.FaceGearSetSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_2505.FlexiblePinAssemblySteadyStateSynchronousResponseOnAShaft]':
        '''List[FlexiblePinAssemblySteadyStateSynchronousResponseOnAShaft]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_2505.FlexiblePinAssemblySteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_2511.HypoidGearSetSteadyStateSynchronousResponseOnAShaft]':
        '''List[HypoidGearSetSteadyStateSynchronousResponseOnAShaft]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_2511.HypoidGearSetSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def imported_fe_components(self) -> 'List[_2513.ImportedFEComponentSteadyStateSynchronousResponseOnAShaft]':
        '''List[ImportedFEComponentSteadyStateSynchronousResponseOnAShaft]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_2513.ImportedFEComponentSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_2519.KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseOnAShaft]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseOnAShaft]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_2519.KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_2522.KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponseOnAShaft]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponseOnAShaft]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_2522.KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def mass_discs(self) -> 'List[_2524.MassDiscSteadyStateSynchronousResponseOnAShaft]':
        '''List[MassDiscSteadyStateSynchronousResponseOnAShaft]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_2524.MassDiscSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def measurement_components(self) -> 'List[_2525.MeasurementComponentSteadyStateSynchronousResponseOnAShaft]':
        '''List[MeasurementComponentSteadyStateSynchronousResponseOnAShaft]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_2525.MeasurementComponentSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def oil_seals(self) -> 'List[_2527.OilSealSteadyStateSynchronousResponseOnAShaft]':
        '''List[OilSealSteadyStateSynchronousResponseOnAShaft]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_2527.OilSealSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_2531.PartToPartShearCouplingSteadyStateSynchronousResponseOnAShaft]':
        '''List[PartToPartShearCouplingSteadyStateSynchronousResponseOnAShaft]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_2531.PartToPartShearCouplingSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def planet_carriers(self) -> 'List[_2534.PlanetCarrierSteadyStateSynchronousResponseOnAShaft]':
        '''List[PlanetCarrierSteadyStateSynchronousResponseOnAShaft]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_2534.PlanetCarrierSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def point_loads(self) -> 'List[_2535.PointLoadSteadyStateSynchronousResponseOnAShaft]':
        '''List[PointLoadSteadyStateSynchronousResponseOnAShaft]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_2535.PointLoadSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def power_loads(self) -> 'List[_2536.PowerLoadSteadyStateSynchronousResponseOnAShaft]':
        '''List[PowerLoadSteadyStateSynchronousResponseOnAShaft]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_2536.PowerLoadSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_2542.ShaftHubConnectionSteadyStateSynchronousResponseOnAShaft]':
        '''List[ShaftHubConnectionSteadyStateSynchronousResponseOnAShaft]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_2542.ShaftHubConnectionSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_2538.RollingRingAssemblySteadyStateSynchronousResponseOnAShaft]':
        '''List[RollingRingAssemblySteadyStateSynchronousResponseOnAShaft]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_2538.RollingRingAssemblySteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def shafts(self) -> 'List[_2543.ShaftSteadyStateSynchronousResponseOnAShaft]':
        '''List[ShaftSteadyStateSynchronousResponseOnAShaft]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_2543.ShaftSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_2547.SpiralBevelGearSetSteadyStateSynchronousResponseOnAShaft]':
        '''List[SpiralBevelGearSetSteadyStateSynchronousResponseOnAShaft]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_2547.SpiralBevelGearSetSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def spring_dampers(self) -> 'List[_2551.SpringDamperSteadyStateSynchronousResponseOnAShaft]':
        '''List[SpringDamperSteadyStateSynchronousResponseOnAShaft]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_2551.SpringDamperSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_2554.StraightBevelDiffGearSetSteadyStateSynchronousResponseOnAShaft]':
        '''List[StraightBevelDiffGearSetSteadyStateSynchronousResponseOnAShaft]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_2554.StraightBevelDiffGearSetSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_2557.StraightBevelGearSetSteadyStateSynchronousResponseOnAShaft]':
        '''List[StraightBevelGearSetSteadyStateSynchronousResponseOnAShaft]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_2557.StraightBevelGearSetSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def synchronisers(self) -> 'List[_2564.SynchroniserSteadyStateSynchronousResponseOnAShaft]':
        '''List[SynchroniserSteadyStateSynchronousResponseOnAShaft]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_2564.SynchroniserSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def torque_converters(self) -> 'List[_2567.TorqueConverterSteadyStateSynchronousResponseOnAShaft]':
        '''List[TorqueConverterSteadyStateSynchronousResponseOnAShaft]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_2567.TorqueConverterSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_2569.UnbalancedMassSteadyStateSynchronousResponseOnAShaft]':
        '''List[UnbalancedMassSteadyStateSynchronousResponseOnAShaft]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_2569.UnbalancedMassSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_2572.WormGearSetSteadyStateSynchronousResponseOnAShaft]':
        '''List[WormGearSetSteadyStateSynchronousResponseOnAShaft]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_2572.WormGearSetSteadyStateSynchronousResponseOnAShaft))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_2575.ZerolBevelGearSetSteadyStateSynchronousResponseOnAShaft]':
        '''List[ZerolBevelGearSetSteadyStateSynchronousResponseOnAShaft]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_2575.ZerolBevelGearSetSteadyStateSynchronousResponseOnAShaft))
        return value
