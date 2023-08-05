'''_2725.py

AssemblySteadyStateSynchronousResponseAtASpeed
'''


from typing import List

from mastapy.system_model.part_model import _1979
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6052
from mastapy.system_model.analyses_and_results.steady_state_synchronous_responses_at_a_speed import (
    _2726, _2728, _2730, _2738,
    _2737, _2741, _2746, _2748,
    _2760, _2762, _2768, _2770,
    _2776, _2778, _2784, _2787,
    _2789, _2790, _2792, _2796,
    _2799, _2800, _2801, _2807,
    _2803, _2808, _2812, _2816,
    _2819, _2822, _2829, _2832,
    _2834, _2837, _2840, _2720
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SteadyStateSynchronousResponsesAtASpeed', 'AssemblySteadyStateSynchronousResponseAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblySteadyStateSynchronousResponseAtASpeed',)


class AssemblySteadyStateSynchronousResponseAtASpeed(_2720.AbstractAssemblySteadyStateSynchronousResponseAtASpeed):
    '''AssemblySteadyStateSynchronousResponseAtASpeed

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_STEADY_STATE_SYNCHRONOUS_RESPONSE_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblySteadyStateSynchronousResponseAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_1979.Assembly':
        '''Assembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1979.Assembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6052.AssemblyLoadCase':
        '''AssemblyLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6052.AssemblyLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def bearings(self) -> 'List[_2726.BearingSteadyStateSynchronousResponseAtASpeed]':
        '''List[BearingSteadyStateSynchronousResponseAtASpeed]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_2726.BearingSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def belt_drives(self) -> 'List[_2728.BeltDriveSteadyStateSynchronousResponseAtASpeed]':
        '''List[BeltDriveSteadyStateSynchronousResponseAtASpeed]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_2728.BeltDriveSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_2730.BevelDifferentialGearSetSteadyStateSynchronousResponseAtASpeed]':
        '''List[BevelDifferentialGearSetSteadyStateSynchronousResponseAtASpeed]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_2730.BevelDifferentialGearSetSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def bolts(self) -> 'List[_2738.BoltSteadyStateSynchronousResponseAtASpeed]':
        '''List[BoltSteadyStateSynchronousResponseAtASpeed]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_2738.BoltSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def bolted_joints(self) -> 'List[_2737.BoltedJointSteadyStateSynchronousResponseAtASpeed]':
        '''List[BoltedJointSteadyStateSynchronousResponseAtASpeed]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_2737.BoltedJointSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def clutches(self) -> 'List[_2741.ClutchSteadyStateSynchronousResponseAtASpeed]':
        '''List[ClutchSteadyStateSynchronousResponseAtASpeed]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_2741.ClutchSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def concept_couplings(self) -> 'List[_2746.ConceptCouplingSteadyStateSynchronousResponseAtASpeed]':
        '''List[ConceptCouplingSteadyStateSynchronousResponseAtASpeed]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_2746.ConceptCouplingSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_2748.ConceptGearSetSteadyStateSynchronousResponseAtASpeed]':
        '''List[ConceptGearSetSteadyStateSynchronousResponseAtASpeed]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_2748.ConceptGearSetSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def cv_ts(self) -> 'List[_2760.CVTSteadyStateSynchronousResponseAtASpeed]':
        '''List[CVTSteadyStateSynchronousResponseAtASpeed]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_2760.CVTSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_2762.CylindricalGearSetSteadyStateSynchronousResponseAtASpeed]':
        '''List[CylindricalGearSetSteadyStateSynchronousResponseAtASpeed]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_2762.CylindricalGearSetSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def face_gear_sets(self) -> 'List[_2768.FaceGearSetSteadyStateSynchronousResponseAtASpeed]':
        '''List[FaceGearSetSteadyStateSynchronousResponseAtASpeed]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_2768.FaceGearSetSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_2770.FlexiblePinAssemblySteadyStateSynchronousResponseAtASpeed]':
        '''List[FlexiblePinAssemblySteadyStateSynchronousResponseAtASpeed]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_2770.FlexiblePinAssemblySteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_2776.HypoidGearSetSteadyStateSynchronousResponseAtASpeed]':
        '''List[HypoidGearSetSteadyStateSynchronousResponseAtASpeed]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_2776.HypoidGearSetSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def imported_fe_components(self) -> 'List[_2778.ImportedFEComponentSteadyStateSynchronousResponseAtASpeed]':
        '''List[ImportedFEComponentSteadyStateSynchronousResponseAtASpeed]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_2778.ImportedFEComponentSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_2784.KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseAtASpeed]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseAtASpeed]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_2784.KlingelnbergCycloPalloidHypoidGearSetSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_2787.KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_2787.KlingelnbergCycloPalloidSpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def mass_discs(self) -> 'List[_2789.MassDiscSteadyStateSynchronousResponseAtASpeed]':
        '''List[MassDiscSteadyStateSynchronousResponseAtASpeed]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_2789.MassDiscSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def measurement_components(self) -> 'List[_2790.MeasurementComponentSteadyStateSynchronousResponseAtASpeed]':
        '''List[MeasurementComponentSteadyStateSynchronousResponseAtASpeed]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_2790.MeasurementComponentSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def oil_seals(self) -> 'List[_2792.OilSealSteadyStateSynchronousResponseAtASpeed]':
        '''List[OilSealSteadyStateSynchronousResponseAtASpeed]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_2792.OilSealSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_2796.PartToPartShearCouplingSteadyStateSynchronousResponseAtASpeed]':
        '''List[PartToPartShearCouplingSteadyStateSynchronousResponseAtASpeed]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_2796.PartToPartShearCouplingSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def planet_carriers(self) -> 'List[_2799.PlanetCarrierSteadyStateSynchronousResponseAtASpeed]':
        '''List[PlanetCarrierSteadyStateSynchronousResponseAtASpeed]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_2799.PlanetCarrierSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def point_loads(self) -> 'List[_2800.PointLoadSteadyStateSynchronousResponseAtASpeed]':
        '''List[PointLoadSteadyStateSynchronousResponseAtASpeed]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_2800.PointLoadSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def power_loads(self) -> 'List[_2801.PowerLoadSteadyStateSynchronousResponseAtASpeed]':
        '''List[PowerLoadSteadyStateSynchronousResponseAtASpeed]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_2801.PowerLoadSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_2807.ShaftHubConnectionSteadyStateSynchronousResponseAtASpeed]':
        '''List[ShaftHubConnectionSteadyStateSynchronousResponseAtASpeed]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_2807.ShaftHubConnectionSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_2803.RollingRingAssemblySteadyStateSynchronousResponseAtASpeed]':
        '''List[RollingRingAssemblySteadyStateSynchronousResponseAtASpeed]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_2803.RollingRingAssemblySteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def shafts(self) -> 'List[_2808.ShaftSteadyStateSynchronousResponseAtASpeed]':
        '''List[ShaftSteadyStateSynchronousResponseAtASpeed]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_2808.ShaftSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_2812.SpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed]':
        '''List[SpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_2812.SpiralBevelGearSetSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def spring_dampers(self) -> 'List[_2816.SpringDamperSteadyStateSynchronousResponseAtASpeed]':
        '''List[SpringDamperSteadyStateSynchronousResponseAtASpeed]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_2816.SpringDamperSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_2819.StraightBevelDiffGearSetSteadyStateSynchronousResponseAtASpeed]':
        '''List[StraightBevelDiffGearSetSteadyStateSynchronousResponseAtASpeed]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_2819.StraightBevelDiffGearSetSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_2822.StraightBevelGearSetSteadyStateSynchronousResponseAtASpeed]':
        '''List[StraightBevelGearSetSteadyStateSynchronousResponseAtASpeed]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_2822.StraightBevelGearSetSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def synchronisers(self) -> 'List[_2829.SynchroniserSteadyStateSynchronousResponseAtASpeed]':
        '''List[SynchroniserSteadyStateSynchronousResponseAtASpeed]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_2829.SynchroniserSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def torque_converters(self) -> 'List[_2832.TorqueConverterSteadyStateSynchronousResponseAtASpeed]':
        '''List[TorqueConverterSteadyStateSynchronousResponseAtASpeed]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_2832.TorqueConverterSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_2834.UnbalancedMassSteadyStateSynchronousResponseAtASpeed]':
        '''List[UnbalancedMassSteadyStateSynchronousResponseAtASpeed]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_2834.UnbalancedMassSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_2837.WormGearSetSteadyStateSynchronousResponseAtASpeed]':
        '''List[WormGearSetSteadyStateSynchronousResponseAtASpeed]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_2837.WormGearSetSteadyStateSynchronousResponseAtASpeed))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_2840.ZerolBevelGearSetSteadyStateSynchronousResponseAtASpeed]':
        '''List[ZerolBevelGearSetSteadyStateSynchronousResponseAtASpeed]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_2840.ZerolBevelGearSetSteadyStateSynchronousResponseAtASpeed))
        return value
