'''_4949.py

AssemblyMultiBodyDynamicsAnalysis
'''


from typing import List

from mastapy.system_model.part_model import _1957
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6030
from mastapy.system_model.analyses_and_results.mbd_analyses import (
    _4950, _4953, _4956, _4963,
    _4962, _4966, _4972, _4975,
    _4985, _4989, _4995, _4996,
    _5004, _5005, _5016, _5019,
    _5020, _5024, _5027, _5031,
    _5034, _5035, _5036, _5044,
    _5038, _5045, _5051, _5054,
    _5057, _5060, _5064, _5069,
    _5073, _5078, _5081, _5010,
    _4944, _5000, _4943
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'AssemblyMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyMultiBodyDynamicsAnalysis',)


class AssemblyMultiBodyDynamicsAnalysis(_4943.AbstractAssemblyMultiBodyDynamicsAnalysis):
    '''AssemblyMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyMultiBodyDynamicsAnalysis.TYPE'):
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
    def bearings(self) -> 'List[_4950.BearingMultiBodyDynamicsAnalysis]':
        '''List[BearingMultiBodyDynamicsAnalysis]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_4950.BearingMultiBodyDynamicsAnalysis))
        return value

    @property
    def belt_drives(self) -> 'List[_4953.BeltDriveMultiBodyDynamicsAnalysis]':
        '''List[BeltDriveMultiBodyDynamicsAnalysis]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_4953.BeltDriveMultiBodyDynamicsAnalysis))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_4956.BevelDifferentialGearSetMultiBodyDynamicsAnalysis]':
        '''List[BevelDifferentialGearSetMultiBodyDynamicsAnalysis]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_4956.BevelDifferentialGearSetMultiBodyDynamicsAnalysis))
        return value

    @property
    def bolts(self) -> 'List[_4963.BoltMultiBodyDynamicsAnalysis]':
        '''List[BoltMultiBodyDynamicsAnalysis]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_4963.BoltMultiBodyDynamicsAnalysis))
        return value

    @property
    def bolted_joints(self) -> 'List[_4962.BoltedJointMultiBodyDynamicsAnalysis]':
        '''List[BoltedJointMultiBodyDynamicsAnalysis]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_4962.BoltedJointMultiBodyDynamicsAnalysis))
        return value

    @property
    def clutches(self) -> 'List[_4966.ClutchMultiBodyDynamicsAnalysis]':
        '''List[ClutchMultiBodyDynamicsAnalysis]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_4966.ClutchMultiBodyDynamicsAnalysis))
        return value

    @property
    def concept_couplings(self) -> 'List[_4972.ConceptCouplingMultiBodyDynamicsAnalysis]':
        '''List[ConceptCouplingMultiBodyDynamicsAnalysis]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_4972.ConceptCouplingMultiBodyDynamicsAnalysis))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_4975.ConceptGearSetMultiBodyDynamicsAnalysis]':
        '''List[ConceptGearSetMultiBodyDynamicsAnalysis]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_4975.ConceptGearSetMultiBodyDynamicsAnalysis))
        return value

    @property
    def cv_ts(self) -> 'List[_4985.CVTMultiBodyDynamicsAnalysis]':
        '''List[CVTMultiBodyDynamicsAnalysis]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_4985.CVTMultiBodyDynamicsAnalysis))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_4989.CylindricalGearSetMultiBodyDynamicsAnalysis]':
        '''List[CylindricalGearSetMultiBodyDynamicsAnalysis]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_4989.CylindricalGearSetMultiBodyDynamicsAnalysis))
        return value

    @property
    def face_gear_sets(self) -> 'List[_4995.FaceGearSetMultiBodyDynamicsAnalysis]':
        '''List[FaceGearSetMultiBodyDynamicsAnalysis]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_4995.FaceGearSetMultiBodyDynamicsAnalysis))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_4996.FlexiblePinAssemblyMultiBodyDynamicsAnalysis]':
        '''List[FlexiblePinAssemblyMultiBodyDynamicsAnalysis]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_4996.FlexiblePinAssemblyMultiBodyDynamicsAnalysis))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_5004.HypoidGearSetMultiBodyDynamicsAnalysis]':
        '''List[HypoidGearSetMultiBodyDynamicsAnalysis]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_5004.HypoidGearSetMultiBodyDynamicsAnalysis))
        return value

    @property
    def imported_fe_components(self) -> 'List[_5005.ImportedFEComponentMultiBodyDynamicsAnalysis]':
        '''List[ImportedFEComponentMultiBodyDynamicsAnalysis]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_5005.ImportedFEComponentMultiBodyDynamicsAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_5016.KlingelnbergCycloPalloidHypoidGearSetMultiBodyDynamicsAnalysis]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetMultiBodyDynamicsAnalysis]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_5016.KlingelnbergCycloPalloidHypoidGearSetMultiBodyDynamicsAnalysis))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_5019.KlingelnbergCycloPalloidSpiralBevelGearSetMultiBodyDynamicsAnalysis]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetMultiBodyDynamicsAnalysis]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_5019.KlingelnbergCycloPalloidSpiralBevelGearSetMultiBodyDynamicsAnalysis))
        return value

    @property
    def mass_discs(self) -> 'List[_5020.MassDiscMultiBodyDynamicsAnalysis]':
        '''List[MassDiscMultiBodyDynamicsAnalysis]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_5020.MassDiscMultiBodyDynamicsAnalysis))
        return value

    @property
    def measurement_components(self) -> 'List[_5024.MeasurementComponentMultiBodyDynamicsAnalysis]':
        '''List[MeasurementComponentMultiBodyDynamicsAnalysis]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_5024.MeasurementComponentMultiBodyDynamicsAnalysis))
        return value

    @property
    def oil_seals(self) -> 'List[_5027.OilSealMultiBodyDynamicsAnalysis]':
        '''List[OilSealMultiBodyDynamicsAnalysis]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_5027.OilSealMultiBodyDynamicsAnalysis))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_5031.PartToPartShearCouplingMultiBodyDynamicsAnalysis]':
        '''List[PartToPartShearCouplingMultiBodyDynamicsAnalysis]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_5031.PartToPartShearCouplingMultiBodyDynamicsAnalysis))
        return value

    @property
    def planet_carriers(self) -> 'List[_5034.PlanetCarrierMultiBodyDynamicsAnalysis]':
        '''List[PlanetCarrierMultiBodyDynamicsAnalysis]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_5034.PlanetCarrierMultiBodyDynamicsAnalysis))
        return value

    @property
    def point_loads(self) -> 'List[_5035.PointLoadMultiBodyDynamicsAnalysis]':
        '''List[PointLoadMultiBodyDynamicsAnalysis]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_5035.PointLoadMultiBodyDynamicsAnalysis))
        return value

    @property
    def power_loads(self) -> 'List[_5036.PowerLoadMultiBodyDynamicsAnalysis]':
        '''List[PowerLoadMultiBodyDynamicsAnalysis]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_5036.PowerLoadMultiBodyDynamicsAnalysis))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_5044.ShaftHubConnectionMultiBodyDynamicsAnalysis]':
        '''List[ShaftHubConnectionMultiBodyDynamicsAnalysis]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_5044.ShaftHubConnectionMultiBodyDynamicsAnalysis))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_5038.RollingRingAssemblyMultiBodyDynamicsAnalysis]':
        '''List[RollingRingAssemblyMultiBodyDynamicsAnalysis]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_5038.RollingRingAssemblyMultiBodyDynamicsAnalysis))
        return value

    @property
    def shafts(self) -> 'List[_5045.ShaftMultiBodyDynamicsAnalysis]':
        '''List[ShaftMultiBodyDynamicsAnalysis]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_5045.ShaftMultiBodyDynamicsAnalysis))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_5051.SpiralBevelGearSetMultiBodyDynamicsAnalysis]':
        '''List[SpiralBevelGearSetMultiBodyDynamicsAnalysis]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_5051.SpiralBevelGearSetMultiBodyDynamicsAnalysis))
        return value

    @property
    def spring_dampers(self) -> 'List[_5054.SpringDamperMultiBodyDynamicsAnalysis]':
        '''List[SpringDamperMultiBodyDynamicsAnalysis]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_5054.SpringDamperMultiBodyDynamicsAnalysis))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_5057.StraightBevelDiffGearSetMultiBodyDynamicsAnalysis]':
        '''List[StraightBevelDiffGearSetMultiBodyDynamicsAnalysis]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_5057.StraightBevelDiffGearSetMultiBodyDynamicsAnalysis))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_5060.StraightBevelGearSetMultiBodyDynamicsAnalysis]':
        '''List[StraightBevelGearSetMultiBodyDynamicsAnalysis]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_5060.StraightBevelGearSetMultiBodyDynamicsAnalysis))
        return value

    @property
    def synchronisers(self) -> 'List[_5064.SynchroniserMultiBodyDynamicsAnalysis]':
        '''List[SynchroniserMultiBodyDynamicsAnalysis]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_5064.SynchroniserMultiBodyDynamicsAnalysis))
        return value

    @property
    def torque_converters(self) -> 'List[_5069.TorqueConverterMultiBodyDynamicsAnalysis]':
        '''List[TorqueConverterMultiBodyDynamicsAnalysis]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_5069.TorqueConverterMultiBodyDynamicsAnalysis))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_5073.UnbalancedMassMultiBodyDynamicsAnalysis]':
        '''List[UnbalancedMassMultiBodyDynamicsAnalysis]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_5073.UnbalancedMassMultiBodyDynamicsAnalysis))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_5078.WormGearSetMultiBodyDynamicsAnalysis]':
        '''List[WormGearSetMultiBodyDynamicsAnalysis]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_5078.WormGearSetMultiBodyDynamicsAnalysis))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_5081.ZerolBevelGearSetMultiBodyDynamicsAnalysis]':
        '''List[ZerolBevelGearSetMultiBodyDynamicsAnalysis]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_5081.ZerolBevelGearSetMultiBodyDynamicsAnalysis))
        return value

    @property
    def connections(self) -> 'List[_5010.InterMountableComponentConnectionMultiBodyDynamicsAnalysis]':
        '''List[InterMountableComponentConnectionMultiBodyDynamicsAnalysis]: 'Connections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Connections, constructor.new(_5010.InterMountableComponentConnectionMultiBodyDynamicsAnalysis))
        return value

    @property
    def shafts_and_housings(self) -> 'List[_4944.AbstractShaftOrHousingMultiBodyDynamicsAnalysis]':
        '''List[AbstractShaftOrHousingMultiBodyDynamicsAnalysis]: 'ShaftsAndHousings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftsAndHousings, constructor.new(_4944.AbstractShaftOrHousingMultiBodyDynamicsAnalysis))
        return value

    @property
    def gear_sets(self) -> 'List[_5000.GearSetMultiBodyDynamicsAnalysis]':
        '''List[GearSetMultiBodyDynamicsAnalysis]: 'GearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearSets, constructor.new(_5000.GearSetMultiBodyDynamicsAnalysis))
        return value
