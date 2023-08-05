'''_5412.py

AssemblySingleMeshWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _1979
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6052
from mastapy.system_model.analyses_and_results.gear_whine_analyses.single_mesh_whine_analyses import (
    _5413, _5415, _5417, _5425,
    _5424, _5428, _5433, _5435,
    _5447, _5449, _5455, _5457,
    _5463, _5465, _5471, _5474,
    _5476, _5477, _5480, _5484,
    _5487, _5488, _5489, _5495,
    _5491, _5496, _5501, _5505,
    _5507, _5510, _5516, _5520,
    _5522, _5525, _5528, _5407
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_SINGLE_MESH_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.SingleMeshWhineAnalyses', 'AssemblySingleMeshWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblySingleMeshWhineAnalysis',)


class AssemblySingleMeshWhineAnalysis(_5407.AbstractAssemblySingleMeshWhineAnalysis):
    '''AssemblySingleMeshWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_SINGLE_MESH_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblySingleMeshWhineAnalysis.TYPE'):
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
    def bearings(self) -> 'List[_5413.BearingSingleMeshWhineAnalysis]':
        '''List[BearingSingleMeshWhineAnalysis]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_5413.BearingSingleMeshWhineAnalysis))
        return value

    @property
    def belt_drives(self) -> 'List[_5415.BeltDriveSingleMeshWhineAnalysis]':
        '''List[BeltDriveSingleMeshWhineAnalysis]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_5415.BeltDriveSingleMeshWhineAnalysis))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_5417.BevelDifferentialGearSetSingleMeshWhineAnalysis]':
        '''List[BevelDifferentialGearSetSingleMeshWhineAnalysis]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_5417.BevelDifferentialGearSetSingleMeshWhineAnalysis))
        return value

    @property
    def bolts(self) -> 'List[_5425.BoltSingleMeshWhineAnalysis]':
        '''List[BoltSingleMeshWhineAnalysis]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_5425.BoltSingleMeshWhineAnalysis))
        return value

    @property
    def bolted_joints(self) -> 'List[_5424.BoltedJointSingleMeshWhineAnalysis]':
        '''List[BoltedJointSingleMeshWhineAnalysis]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_5424.BoltedJointSingleMeshWhineAnalysis))
        return value

    @property
    def clutches(self) -> 'List[_5428.ClutchSingleMeshWhineAnalysis]':
        '''List[ClutchSingleMeshWhineAnalysis]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_5428.ClutchSingleMeshWhineAnalysis))
        return value

    @property
    def concept_couplings(self) -> 'List[_5433.ConceptCouplingSingleMeshWhineAnalysis]':
        '''List[ConceptCouplingSingleMeshWhineAnalysis]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_5433.ConceptCouplingSingleMeshWhineAnalysis))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_5435.ConceptGearSetSingleMeshWhineAnalysis]':
        '''List[ConceptGearSetSingleMeshWhineAnalysis]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_5435.ConceptGearSetSingleMeshWhineAnalysis))
        return value

    @property
    def cv_ts(self) -> 'List[_5447.CVTSingleMeshWhineAnalysis]':
        '''List[CVTSingleMeshWhineAnalysis]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_5447.CVTSingleMeshWhineAnalysis))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_5449.CylindricalGearSetSingleMeshWhineAnalysis]':
        '''List[CylindricalGearSetSingleMeshWhineAnalysis]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_5449.CylindricalGearSetSingleMeshWhineAnalysis))
        return value

    @property
    def face_gear_sets(self) -> 'List[_5455.FaceGearSetSingleMeshWhineAnalysis]':
        '''List[FaceGearSetSingleMeshWhineAnalysis]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_5455.FaceGearSetSingleMeshWhineAnalysis))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_5457.FlexiblePinAssemblySingleMeshWhineAnalysis]':
        '''List[FlexiblePinAssemblySingleMeshWhineAnalysis]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_5457.FlexiblePinAssemblySingleMeshWhineAnalysis))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_5463.HypoidGearSetSingleMeshWhineAnalysis]':
        '''List[HypoidGearSetSingleMeshWhineAnalysis]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_5463.HypoidGearSetSingleMeshWhineAnalysis))
        return value

    @property
    def imported_fe_components(self) -> 'List[_5465.ImportedFEComponentSingleMeshWhineAnalysis]':
        '''List[ImportedFEComponentSingleMeshWhineAnalysis]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_5465.ImportedFEComponentSingleMeshWhineAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_5471.KlingelnbergCycloPalloidHypoidGearSetSingleMeshWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetSingleMeshWhineAnalysis]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_5471.KlingelnbergCycloPalloidHypoidGearSetSingleMeshWhineAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_5474.KlingelnbergCycloPalloidSpiralBevelGearSetSingleMeshWhineAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetSingleMeshWhineAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_5474.KlingelnbergCycloPalloidSpiralBevelGearSetSingleMeshWhineAnalysis))
        return value

    @property
    def mass_discs(self) -> 'List[_5476.MassDiscSingleMeshWhineAnalysis]':
        '''List[MassDiscSingleMeshWhineAnalysis]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_5476.MassDiscSingleMeshWhineAnalysis))
        return value

    @property
    def measurement_components(self) -> 'List[_5477.MeasurementComponentSingleMeshWhineAnalysis]':
        '''List[MeasurementComponentSingleMeshWhineAnalysis]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_5477.MeasurementComponentSingleMeshWhineAnalysis))
        return value

    @property
    def oil_seals(self) -> 'List[_5480.OilSealSingleMeshWhineAnalysis]':
        '''List[OilSealSingleMeshWhineAnalysis]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_5480.OilSealSingleMeshWhineAnalysis))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_5484.PartToPartShearCouplingSingleMeshWhineAnalysis]':
        '''List[PartToPartShearCouplingSingleMeshWhineAnalysis]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_5484.PartToPartShearCouplingSingleMeshWhineAnalysis))
        return value

    @property
    def planet_carriers(self) -> 'List[_5487.PlanetCarrierSingleMeshWhineAnalysis]':
        '''List[PlanetCarrierSingleMeshWhineAnalysis]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_5487.PlanetCarrierSingleMeshWhineAnalysis))
        return value

    @property
    def point_loads(self) -> 'List[_5488.PointLoadSingleMeshWhineAnalysis]':
        '''List[PointLoadSingleMeshWhineAnalysis]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_5488.PointLoadSingleMeshWhineAnalysis))
        return value

    @property
    def power_loads(self) -> 'List[_5489.PowerLoadSingleMeshWhineAnalysis]':
        '''List[PowerLoadSingleMeshWhineAnalysis]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_5489.PowerLoadSingleMeshWhineAnalysis))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_5495.ShaftHubConnectionSingleMeshWhineAnalysis]':
        '''List[ShaftHubConnectionSingleMeshWhineAnalysis]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_5495.ShaftHubConnectionSingleMeshWhineAnalysis))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_5491.RollingRingAssemblySingleMeshWhineAnalysis]':
        '''List[RollingRingAssemblySingleMeshWhineAnalysis]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_5491.RollingRingAssemblySingleMeshWhineAnalysis))
        return value

    @property
    def shafts(self) -> 'List[_5496.ShaftSingleMeshWhineAnalysis]':
        '''List[ShaftSingleMeshWhineAnalysis]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_5496.ShaftSingleMeshWhineAnalysis))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_5501.SpiralBevelGearSetSingleMeshWhineAnalysis]':
        '''List[SpiralBevelGearSetSingleMeshWhineAnalysis]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_5501.SpiralBevelGearSetSingleMeshWhineAnalysis))
        return value

    @property
    def spring_dampers(self) -> 'List[_5505.SpringDamperSingleMeshWhineAnalysis]':
        '''List[SpringDamperSingleMeshWhineAnalysis]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_5505.SpringDamperSingleMeshWhineAnalysis))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_5507.StraightBevelDiffGearSetSingleMeshWhineAnalysis]':
        '''List[StraightBevelDiffGearSetSingleMeshWhineAnalysis]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_5507.StraightBevelDiffGearSetSingleMeshWhineAnalysis))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_5510.StraightBevelGearSetSingleMeshWhineAnalysis]':
        '''List[StraightBevelGearSetSingleMeshWhineAnalysis]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_5510.StraightBevelGearSetSingleMeshWhineAnalysis))
        return value

    @property
    def synchronisers(self) -> 'List[_5516.SynchroniserSingleMeshWhineAnalysis]':
        '''List[SynchroniserSingleMeshWhineAnalysis]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_5516.SynchroniserSingleMeshWhineAnalysis))
        return value

    @property
    def torque_converters(self) -> 'List[_5520.TorqueConverterSingleMeshWhineAnalysis]':
        '''List[TorqueConverterSingleMeshWhineAnalysis]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_5520.TorqueConverterSingleMeshWhineAnalysis))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_5522.UnbalancedMassSingleMeshWhineAnalysis]':
        '''List[UnbalancedMassSingleMeshWhineAnalysis]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_5522.UnbalancedMassSingleMeshWhineAnalysis))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_5525.WormGearSetSingleMeshWhineAnalysis]':
        '''List[WormGearSetSingleMeshWhineAnalysis]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_5525.WormGearSetSingleMeshWhineAnalysis))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_5528.ZerolBevelGearSetSingleMeshWhineAnalysis]':
        '''List[ZerolBevelGearSetSingleMeshWhineAnalysis]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_5528.ZerolBevelGearSetSingleMeshWhineAnalysis))
        return value
