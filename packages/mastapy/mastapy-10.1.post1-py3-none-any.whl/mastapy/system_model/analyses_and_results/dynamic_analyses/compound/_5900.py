'''_5900.py

AssemblyCompoundDynamicAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _1957
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.dynamic_analyses import _5777
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import (
    _5901, _5903, _5906, _5912,
    _5913, _5914, _5919, _5924,
    _5934, _5938, _5944, _5945,
    _5952, _5953, _5960, _5963,
    _5964, _5965, _5967, _5969,
    _5974, _5975, _5976, _5983,
    _5978, _5982, _5988, _5989,
    _5994, _5997, _6000, _6004,
    _6008, _6012, _6015, _5895
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_DYNAMIC_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.DynamicAnalyses.Compound', 'AssemblyCompoundDynamicAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundDynamicAnalysis',)


class AssemblyCompoundDynamicAnalysis(_5895.AbstractAssemblyCompoundDynamicAnalysis):
    '''AssemblyCompoundDynamicAnalysis

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_DYNAMIC_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundDynamicAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1957.Assembly':
        '''Assembly: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1957.Assembly)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_1957.Assembly':
        '''Assembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1957.Assembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5777.AssemblyDynamicAnalysis]':
        '''List[AssemblyDynamicAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5777.AssemblyDynamicAnalysis))
        return value

    @property
    def assembly_dynamic_analysis_load_cases(self) -> 'List[_5777.AssemblyDynamicAnalysis]':
        '''List[AssemblyDynamicAnalysis]: 'AssemblyDynamicAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyDynamicAnalysisLoadCases, constructor.new(_5777.AssemblyDynamicAnalysis))
        return value

    @property
    def bearings(self) -> 'List[_5901.BearingCompoundDynamicAnalysis]':
        '''List[BearingCompoundDynamicAnalysis]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_5901.BearingCompoundDynamicAnalysis))
        return value

    @property
    def belt_drives(self) -> 'List[_5903.BeltDriveCompoundDynamicAnalysis]':
        '''List[BeltDriveCompoundDynamicAnalysis]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_5903.BeltDriveCompoundDynamicAnalysis))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_5906.BevelDifferentialGearSetCompoundDynamicAnalysis]':
        '''List[BevelDifferentialGearSetCompoundDynamicAnalysis]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_5906.BevelDifferentialGearSetCompoundDynamicAnalysis))
        return value

    @property
    def bolts(self) -> 'List[_5912.BoltCompoundDynamicAnalysis]':
        '''List[BoltCompoundDynamicAnalysis]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_5912.BoltCompoundDynamicAnalysis))
        return value

    @property
    def bolted_joints(self) -> 'List[_5913.BoltedJointCompoundDynamicAnalysis]':
        '''List[BoltedJointCompoundDynamicAnalysis]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_5913.BoltedJointCompoundDynamicAnalysis))
        return value

    @property
    def clutches(self) -> 'List[_5914.ClutchCompoundDynamicAnalysis]':
        '''List[ClutchCompoundDynamicAnalysis]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_5914.ClutchCompoundDynamicAnalysis))
        return value

    @property
    def concept_couplings(self) -> 'List[_5919.ConceptCouplingCompoundDynamicAnalysis]':
        '''List[ConceptCouplingCompoundDynamicAnalysis]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_5919.ConceptCouplingCompoundDynamicAnalysis))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_5924.ConceptGearSetCompoundDynamicAnalysis]':
        '''List[ConceptGearSetCompoundDynamicAnalysis]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_5924.ConceptGearSetCompoundDynamicAnalysis))
        return value

    @property
    def cv_ts(self) -> 'List[_5934.CVTCompoundDynamicAnalysis]':
        '''List[CVTCompoundDynamicAnalysis]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_5934.CVTCompoundDynamicAnalysis))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_5938.CylindricalGearSetCompoundDynamicAnalysis]':
        '''List[CylindricalGearSetCompoundDynamicAnalysis]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_5938.CylindricalGearSetCompoundDynamicAnalysis))
        return value

    @property
    def face_gear_sets(self) -> 'List[_5944.FaceGearSetCompoundDynamicAnalysis]':
        '''List[FaceGearSetCompoundDynamicAnalysis]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_5944.FaceGearSetCompoundDynamicAnalysis))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_5945.FlexiblePinAssemblyCompoundDynamicAnalysis]':
        '''List[FlexiblePinAssemblyCompoundDynamicAnalysis]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_5945.FlexiblePinAssemblyCompoundDynamicAnalysis))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_5952.HypoidGearSetCompoundDynamicAnalysis]':
        '''List[HypoidGearSetCompoundDynamicAnalysis]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_5952.HypoidGearSetCompoundDynamicAnalysis))
        return value

    @property
    def imported_fe_components(self) -> 'List[_5953.ImportedFEComponentCompoundDynamicAnalysis]':
        '''List[ImportedFEComponentCompoundDynamicAnalysis]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_5953.ImportedFEComponentCompoundDynamicAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_5960.KlingelnbergCycloPalloidHypoidGearSetCompoundDynamicAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundDynamicAnalysis]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_5960.KlingelnbergCycloPalloidHypoidGearSetCompoundDynamicAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_5963.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundDynamicAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundDynamicAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_5963.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundDynamicAnalysis))
        return value

    @property
    def mass_discs(self) -> 'List[_5964.MassDiscCompoundDynamicAnalysis]':
        '''List[MassDiscCompoundDynamicAnalysis]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_5964.MassDiscCompoundDynamicAnalysis))
        return value

    @property
    def measurement_components(self) -> 'List[_5965.MeasurementComponentCompoundDynamicAnalysis]':
        '''List[MeasurementComponentCompoundDynamicAnalysis]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_5965.MeasurementComponentCompoundDynamicAnalysis))
        return value

    @property
    def oil_seals(self) -> 'List[_5967.OilSealCompoundDynamicAnalysis]':
        '''List[OilSealCompoundDynamicAnalysis]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_5967.OilSealCompoundDynamicAnalysis))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_5969.PartToPartShearCouplingCompoundDynamicAnalysis]':
        '''List[PartToPartShearCouplingCompoundDynamicAnalysis]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_5969.PartToPartShearCouplingCompoundDynamicAnalysis))
        return value

    @property
    def planet_carriers(self) -> 'List[_5974.PlanetCarrierCompoundDynamicAnalysis]':
        '''List[PlanetCarrierCompoundDynamicAnalysis]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_5974.PlanetCarrierCompoundDynamicAnalysis))
        return value

    @property
    def point_loads(self) -> 'List[_5975.PointLoadCompoundDynamicAnalysis]':
        '''List[PointLoadCompoundDynamicAnalysis]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_5975.PointLoadCompoundDynamicAnalysis))
        return value

    @property
    def power_loads(self) -> 'List[_5976.PowerLoadCompoundDynamicAnalysis]':
        '''List[PowerLoadCompoundDynamicAnalysis]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_5976.PowerLoadCompoundDynamicAnalysis))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_5983.ShaftHubConnectionCompoundDynamicAnalysis]':
        '''List[ShaftHubConnectionCompoundDynamicAnalysis]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_5983.ShaftHubConnectionCompoundDynamicAnalysis))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_5978.RollingRingAssemblyCompoundDynamicAnalysis]':
        '''List[RollingRingAssemblyCompoundDynamicAnalysis]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_5978.RollingRingAssemblyCompoundDynamicAnalysis))
        return value

    @property
    def shafts(self) -> 'List[_5982.ShaftCompoundDynamicAnalysis]':
        '''List[ShaftCompoundDynamicAnalysis]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_5982.ShaftCompoundDynamicAnalysis))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_5988.SpiralBevelGearSetCompoundDynamicAnalysis]':
        '''List[SpiralBevelGearSetCompoundDynamicAnalysis]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_5988.SpiralBevelGearSetCompoundDynamicAnalysis))
        return value

    @property
    def spring_dampers(self) -> 'List[_5989.SpringDamperCompoundDynamicAnalysis]':
        '''List[SpringDamperCompoundDynamicAnalysis]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_5989.SpringDamperCompoundDynamicAnalysis))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_5994.StraightBevelDiffGearSetCompoundDynamicAnalysis]':
        '''List[StraightBevelDiffGearSetCompoundDynamicAnalysis]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_5994.StraightBevelDiffGearSetCompoundDynamicAnalysis))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_5997.StraightBevelGearSetCompoundDynamicAnalysis]':
        '''List[StraightBevelGearSetCompoundDynamicAnalysis]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_5997.StraightBevelGearSetCompoundDynamicAnalysis))
        return value

    @property
    def synchronisers(self) -> 'List[_6000.SynchroniserCompoundDynamicAnalysis]':
        '''List[SynchroniserCompoundDynamicAnalysis]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_6000.SynchroniserCompoundDynamicAnalysis))
        return value

    @property
    def torque_converters(self) -> 'List[_6004.TorqueConverterCompoundDynamicAnalysis]':
        '''List[TorqueConverterCompoundDynamicAnalysis]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_6004.TorqueConverterCompoundDynamicAnalysis))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_6008.UnbalancedMassCompoundDynamicAnalysis]':
        '''List[UnbalancedMassCompoundDynamicAnalysis]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_6008.UnbalancedMassCompoundDynamicAnalysis))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_6012.WormGearSetCompoundDynamicAnalysis]':
        '''List[WormGearSetCompoundDynamicAnalysis]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_6012.WormGearSetCompoundDynamicAnalysis))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_6015.ZerolBevelGearSetCompoundDynamicAnalysis]':
        '''List[ZerolBevelGearSetCompoundDynamicAnalysis]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_6015.ZerolBevelGearSetCompoundDynamicAnalysis))
        return value
