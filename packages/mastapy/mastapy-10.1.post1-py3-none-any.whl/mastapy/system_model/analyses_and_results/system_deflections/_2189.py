'''_2189.py

AssemblySystemDeflection
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import _1957
from mastapy.system_model.analyses_and_results.static_loads import _6030
from mastapy.system_model.analyses_and_results.power_flows import _3198
from mastapy.nodal_analysis import _1338
from mastapy.shafts import _37
from mastapy.gears.analysis import _948
from mastapy.system_model.analyses_and_results.system_deflections import (
    _2190, _2192, _2194, _2202,
    _2201, _2205, _2211, _2213,
    _2226, _2230, _2241, _2243,
    _2249, _2251, _2257, _2260,
    _2263, _2264, _2268, _2272,
    _2274, _2275, _2276, _2282,
    _2278, _2285, _2289, _2293,
    _2295, _2298, _2305, _2311,
    _2315, _2318, _2321, _2185,
    _2219, _2207, _2266, _2244,
    _2184
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'AssemblySystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblySystemDeflection',)


class AssemblySystemDeflection(_2184.AbstractAssemblySystemDeflection):
    '''AssemblySystemDeflection

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblySystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def overall_bearing_reliability(self) -> 'float':
        '''float: 'OverallBearingReliability' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OverallBearingReliability

    @property
    def overall_shaft_reliability(self) -> 'float':
        '''float: 'OverallShaftReliability' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OverallShaftReliability

    @property
    def overall_gear_reliability(self) -> 'float':
        '''float: 'OverallGearReliability' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OverallGearReliability

    @property
    def overall_oil_seal_reliability(self) -> 'float':
        '''float: 'OverallOilSealReliability' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OverallOilSealReliability

    @property
    def overall_system_reliability(self) -> 'float':
        '''float: 'OverallSystemReliability' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.OverallSystemReliability

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
    def power_flow_results(self) -> '_3198.AssemblyPowerFlow':
        '''AssemblyPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3198.AssemblyPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def analysis_settings(self) -> '_1338.AnalysisSettings':
        '''AnalysisSettings: 'AnalysisSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1338.AnalysisSettings)(self.wrapped.AnalysisSettings) if self.wrapped.AnalysisSettings else None

    @property
    def shaft_settings(self) -> '_37.ShaftSettings':
        '''ShaftSettings: 'ShaftSettings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_37.ShaftSettings)(self.wrapped.ShaftSettings) if self.wrapped.ShaftSettings else None

    @property
    def rating_for_all_gear_sets(self) -> '_948.GearSetGroupDutyCycle':
        '''GearSetGroupDutyCycle: 'RatingForAllGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_948.GearSetGroupDutyCycle)(self.wrapped.RatingForAllGearSets) if self.wrapped.RatingForAllGearSets else None

    @property
    def bearings(self) -> 'List[_2190.BearingSystemDeflection]':
        '''List[BearingSystemDeflection]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_2190.BearingSystemDeflection))
        return value

    @property
    def belt_drives(self) -> 'List[_2192.BeltDriveSystemDeflection]':
        '''List[BeltDriveSystemDeflection]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_2192.BeltDriveSystemDeflection))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_2194.BevelDifferentialGearSetSystemDeflection]':
        '''List[BevelDifferentialGearSetSystemDeflection]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_2194.BevelDifferentialGearSetSystemDeflection))
        return value

    @property
    def bolts(self) -> 'List[_2202.BoltSystemDeflection]':
        '''List[BoltSystemDeflection]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_2202.BoltSystemDeflection))
        return value

    @property
    def bolted_joints(self) -> 'List[_2201.BoltedJointSystemDeflection]':
        '''List[BoltedJointSystemDeflection]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_2201.BoltedJointSystemDeflection))
        return value

    @property
    def clutches(self) -> 'List[_2205.ClutchSystemDeflection]':
        '''List[ClutchSystemDeflection]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_2205.ClutchSystemDeflection))
        return value

    @property
    def concept_couplings(self) -> 'List[_2211.ConceptCouplingSystemDeflection]':
        '''List[ConceptCouplingSystemDeflection]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_2211.ConceptCouplingSystemDeflection))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_2213.ConceptGearSetSystemDeflection]':
        '''List[ConceptGearSetSystemDeflection]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_2213.ConceptGearSetSystemDeflection))
        return value

    @property
    def cv_ts(self) -> 'List[_2226.CVTSystemDeflection]':
        '''List[CVTSystemDeflection]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_2226.CVTSystemDeflection))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_2230.CylindricalGearSetSystemDeflection]':
        '''List[CylindricalGearSetSystemDeflection]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_2230.CylindricalGearSetSystemDeflection))
        return value

    @property
    def face_gear_sets(self) -> 'List[_2241.FaceGearSetSystemDeflection]':
        '''List[FaceGearSetSystemDeflection]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_2241.FaceGearSetSystemDeflection))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_2243.FlexiblePinAssemblySystemDeflection]':
        '''List[FlexiblePinAssemblySystemDeflection]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_2243.FlexiblePinAssemblySystemDeflection))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_2249.HypoidGearSetSystemDeflection]':
        '''List[HypoidGearSetSystemDeflection]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_2249.HypoidGearSetSystemDeflection))
        return value

    @property
    def imported_fe_components(self) -> 'List[_2251.ImportedFEComponentSystemDeflection]':
        '''List[ImportedFEComponentSystemDeflection]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_2251.ImportedFEComponentSystemDeflection))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_2257.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetSystemDeflection]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_2257.KlingelnbergCycloPalloidHypoidGearSetSystemDeflection))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_2260.KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_2260.KlingelnbergCycloPalloidSpiralBevelGearSetSystemDeflection))
        return value

    @property
    def mass_discs(self) -> 'List[_2263.MassDiscSystemDeflection]':
        '''List[MassDiscSystemDeflection]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_2263.MassDiscSystemDeflection))
        return value

    @property
    def measurement_components(self) -> 'List[_2264.MeasurementComponentSystemDeflection]':
        '''List[MeasurementComponentSystemDeflection]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_2264.MeasurementComponentSystemDeflection))
        return value

    @property
    def oil_seals(self) -> 'List[_2268.OilSealSystemDeflection]':
        '''List[OilSealSystemDeflection]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_2268.OilSealSystemDeflection))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_2272.PartToPartShearCouplingSystemDeflection]':
        '''List[PartToPartShearCouplingSystemDeflection]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_2272.PartToPartShearCouplingSystemDeflection))
        return value

    @property
    def planet_carriers(self) -> 'List[_2274.PlanetCarrierSystemDeflection]':
        '''List[PlanetCarrierSystemDeflection]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_2274.PlanetCarrierSystemDeflection))
        return value

    @property
    def point_loads(self) -> 'List[_2275.PointLoadSystemDeflection]':
        '''List[PointLoadSystemDeflection]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_2275.PointLoadSystemDeflection))
        return value

    @property
    def power_loads(self) -> 'List[_2276.PowerLoadSystemDeflection]':
        '''List[PowerLoadSystemDeflection]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_2276.PowerLoadSystemDeflection))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_2282.ShaftHubConnectionSystemDeflection]':
        '''List[ShaftHubConnectionSystemDeflection]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_2282.ShaftHubConnectionSystemDeflection))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_2278.RollingRingAssemblySystemDeflection]':
        '''List[RollingRingAssemblySystemDeflection]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_2278.RollingRingAssemblySystemDeflection))
        return value

    @property
    def shafts(self) -> 'List[_2285.ShaftSystemDeflection]':
        '''List[ShaftSystemDeflection]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_2285.ShaftSystemDeflection))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_2289.SpiralBevelGearSetSystemDeflection]':
        '''List[SpiralBevelGearSetSystemDeflection]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_2289.SpiralBevelGearSetSystemDeflection))
        return value

    @property
    def spring_dampers(self) -> 'List[_2293.SpringDamperSystemDeflection]':
        '''List[SpringDamperSystemDeflection]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_2293.SpringDamperSystemDeflection))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_2295.StraightBevelDiffGearSetSystemDeflection]':
        '''List[StraightBevelDiffGearSetSystemDeflection]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_2295.StraightBevelDiffGearSetSystemDeflection))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_2298.StraightBevelGearSetSystemDeflection]':
        '''List[StraightBevelGearSetSystemDeflection]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_2298.StraightBevelGearSetSystemDeflection))
        return value

    @property
    def synchronisers(self) -> 'List[_2305.SynchroniserSystemDeflection]':
        '''List[SynchroniserSystemDeflection]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_2305.SynchroniserSystemDeflection))
        return value

    @property
    def torque_converters(self) -> 'List[_2311.TorqueConverterSystemDeflection]':
        '''List[TorqueConverterSystemDeflection]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_2311.TorqueConverterSystemDeflection))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_2315.UnbalancedMassSystemDeflection]':
        '''List[UnbalancedMassSystemDeflection]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_2315.UnbalancedMassSystemDeflection))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_2318.WormGearSetSystemDeflection]':
        '''List[WormGearSetSystemDeflection]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_2318.WormGearSetSystemDeflection))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_2321.ZerolBevelGearSetSystemDeflection]':
        '''List[ZerolBevelGearSetSystemDeflection]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_2321.ZerolBevelGearSetSystemDeflection))
        return value

    @property
    def shafts_and_housings(self) -> 'List[_2185.AbstractShaftOrHousingSystemDeflection]':
        '''List[AbstractShaftOrHousingSystemDeflection]: 'ShaftsAndHousings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftsAndHousings, constructor.new(_2185.AbstractShaftOrHousingSystemDeflection))
        return value

    @property
    def supercharger_rotor_sets(self) -> 'List[_2230.CylindricalGearSetSystemDeflection]':
        '''List[CylindricalGearSetSystemDeflection]: 'SuperchargerRotorSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SuperchargerRotorSets, constructor.new(_2230.CylindricalGearSetSystemDeflection))
        return value

    @property
    def rolling_bearings(self) -> 'List[_2190.BearingSystemDeflection]':
        '''List[BearingSystemDeflection]: 'RollingBearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingBearings, constructor.new(_2190.BearingSystemDeflection))
        return value

    @property
    def connection_details(self) -> 'List[_2219.ConnectionSystemDeflection]':
        '''List[ConnectionSystemDeflection]: 'ConnectionDetails' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionDetails, constructor.new(_2219.ConnectionSystemDeflection))
        return value

    @property
    def sorted_converged_connection_details(self) -> 'List[_2219.ConnectionSystemDeflection]':
        '''List[ConnectionSystemDeflection]: 'SortedConvergedConnectionDetails' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SortedConvergedConnectionDetails, constructor.new(_2219.ConnectionSystemDeflection))
        return value

    @property
    def sorted_unconverged_connection_details(self) -> 'List[_2219.ConnectionSystemDeflection]':
        '''List[ConnectionSystemDeflection]: 'SortedUnconvergedConnectionDetails' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SortedUnconvergedConnectionDetails, constructor.new(_2219.ConnectionSystemDeflection))
        return value

    @property
    def component_details(self) -> 'List[_2207.ComponentSystemDeflection]':
        '''List[ComponentSystemDeflection]: 'ComponentDetails' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentDetails, constructor.new(_2207.ComponentSystemDeflection))
        return value

    @property
    def mountable_component_details(self) -> 'List[_2266.MountableComponentSystemDeflection]':
        '''List[MountableComponentSystemDeflection]: 'MountableComponentDetails' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MountableComponentDetails, constructor.new(_2266.MountableComponentSystemDeflection))
        return value

    @property
    def sorted_converged_component_details(self) -> 'List[_2207.ComponentSystemDeflection]':
        '''List[ComponentSystemDeflection]: 'SortedConvergedComponentDetails' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SortedConvergedComponentDetails, constructor.new(_2207.ComponentSystemDeflection))
        return value

    @property
    def sorted_unconverged_component_details(self) -> 'List[_2207.ComponentSystemDeflection]':
        '''List[ComponentSystemDeflection]: 'SortedUnconvergedComponentDetails' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SortedUnconvergedComponentDetails, constructor.new(_2207.ComponentSystemDeflection))
        return value

    @property
    def unconverged_bearings_sorted_by_load(self) -> 'List[_2190.BearingSystemDeflection]':
        '''List[BearingSystemDeflection]: 'UnconvergedBearingsSortedByLoad' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnconvergedBearingsSortedByLoad, constructor.new(_2190.BearingSystemDeflection))
        return value

    @property
    def unconverged_gear_meshes_sorted_by_power(self) -> 'List[_2244.GearMeshSystemDeflection]':
        '''List[GearMeshSystemDeflection]: 'UnconvergedGearMeshesSortedByPower' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnconvergedGearMeshesSortedByPower, constructor.new(_2244.GearMeshSystemDeflection))
        return value
