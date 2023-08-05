'''_6217.py

AssemblyAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _1957
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6030
from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
    _6218, _6220, _6223, _6229,
    _6230, _6231, _6236, _6241,
    _6250, _6255, _6262, _6263,
    _6270, _6271, _6278, _6281,
    _6283, _6284, _6286, _6288,
    _6293, _6294, _6295, _6302,
    _6298, _6301, _6307, _6308,
    _6313, _6316, _6319, _6323,
    _6328, _6333, _6336, _6209
)
from mastapy.system_model.analyses_and_results.system_deflections import _2189
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'AssemblyAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyAdvancedSystemDeflection',)


class AssemblyAdvancedSystemDeflection(_6209.AbstractAssemblyAdvancedSystemDeflection):
    '''AssemblyAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyAdvancedSystemDeflection.TYPE'):
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
    def bearings(self) -> 'List[_6218.BearingAdvancedSystemDeflection]':
        '''List[BearingAdvancedSystemDeflection]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_6218.BearingAdvancedSystemDeflection))
        return value

    @property
    def belt_drives(self) -> 'List[_6220.BeltDriveAdvancedSystemDeflection]':
        '''List[BeltDriveAdvancedSystemDeflection]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_6220.BeltDriveAdvancedSystemDeflection))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_6223.BevelDifferentialGearSetAdvancedSystemDeflection]':
        '''List[BevelDifferentialGearSetAdvancedSystemDeflection]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_6223.BevelDifferentialGearSetAdvancedSystemDeflection))
        return value

    @property
    def bolts(self) -> 'List[_6229.BoltAdvancedSystemDeflection]':
        '''List[BoltAdvancedSystemDeflection]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_6229.BoltAdvancedSystemDeflection))
        return value

    @property
    def bolted_joints(self) -> 'List[_6230.BoltedJointAdvancedSystemDeflection]':
        '''List[BoltedJointAdvancedSystemDeflection]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_6230.BoltedJointAdvancedSystemDeflection))
        return value

    @property
    def clutches(self) -> 'List[_6231.ClutchAdvancedSystemDeflection]':
        '''List[ClutchAdvancedSystemDeflection]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_6231.ClutchAdvancedSystemDeflection))
        return value

    @property
    def concept_couplings(self) -> 'List[_6236.ConceptCouplingAdvancedSystemDeflection]':
        '''List[ConceptCouplingAdvancedSystemDeflection]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_6236.ConceptCouplingAdvancedSystemDeflection))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_6241.ConceptGearSetAdvancedSystemDeflection]':
        '''List[ConceptGearSetAdvancedSystemDeflection]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_6241.ConceptGearSetAdvancedSystemDeflection))
        return value

    @property
    def cv_ts(self) -> 'List[_6250.CVTAdvancedSystemDeflection]':
        '''List[CVTAdvancedSystemDeflection]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_6250.CVTAdvancedSystemDeflection))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_6255.CylindricalGearSetAdvancedSystemDeflection]':
        '''List[CylindricalGearSetAdvancedSystemDeflection]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_6255.CylindricalGearSetAdvancedSystemDeflection))
        return value

    @property
    def face_gear_sets(self) -> 'List[_6262.FaceGearSetAdvancedSystemDeflection]':
        '''List[FaceGearSetAdvancedSystemDeflection]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_6262.FaceGearSetAdvancedSystemDeflection))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_6263.FlexiblePinAssemblyAdvancedSystemDeflection]':
        '''List[FlexiblePinAssemblyAdvancedSystemDeflection]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_6263.FlexiblePinAssemblyAdvancedSystemDeflection))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_6270.HypoidGearSetAdvancedSystemDeflection]':
        '''List[HypoidGearSetAdvancedSystemDeflection]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_6270.HypoidGearSetAdvancedSystemDeflection))
        return value

    @property
    def imported_fe_components(self) -> 'List[_6271.ImportedFEComponentAdvancedSystemDeflection]':
        '''List[ImportedFEComponentAdvancedSystemDeflection]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_6271.ImportedFEComponentAdvancedSystemDeflection))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_6278.KlingelnbergCycloPalloidHypoidGearSetAdvancedSystemDeflection]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetAdvancedSystemDeflection]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_6278.KlingelnbergCycloPalloidHypoidGearSetAdvancedSystemDeflection))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_6281.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_6281.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection))
        return value

    @property
    def mass_discs(self) -> 'List[_6283.MassDiscAdvancedSystemDeflection]':
        '''List[MassDiscAdvancedSystemDeflection]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_6283.MassDiscAdvancedSystemDeflection))
        return value

    @property
    def measurement_components(self) -> 'List[_6284.MeasurementComponentAdvancedSystemDeflection]':
        '''List[MeasurementComponentAdvancedSystemDeflection]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_6284.MeasurementComponentAdvancedSystemDeflection))
        return value

    @property
    def oil_seals(self) -> 'List[_6286.OilSealAdvancedSystemDeflection]':
        '''List[OilSealAdvancedSystemDeflection]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_6286.OilSealAdvancedSystemDeflection))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_6288.PartToPartShearCouplingAdvancedSystemDeflection]':
        '''List[PartToPartShearCouplingAdvancedSystemDeflection]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_6288.PartToPartShearCouplingAdvancedSystemDeflection))
        return value

    @property
    def planet_carriers(self) -> 'List[_6293.PlanetCarrierAdvancedSystemDeflection]':
        '''List[PlanetCarrierAdvancedSystemDeflection]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_6293.PlanetCarrierAdvancedSystemDeflection))
        return value

    @property
    def point_loads(self) -> 'List[_6294.PointLoadAdvancedSystemDeflection]':
        '''List[PointLoadAdvancedSystemDeflection]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_6294.PointLoadAdvancedSystemDeflection))
        return value

    @property
    def power_loads(self) -> 'List[_6295.PowerLoadAdvancedSystemDeflection]':
        '''List[PowerLoadAdvancedSystemDeflection]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_6295.PowerLoadAdvancedSystemDeflection))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_6302.ShaftHubConnectionAdvancedSystemDeflection]':
        '''List[ShaftHubConnectionAdvancedSystemDeflection]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_6302.ShaftHubConnectionAdvancedSystemDeflection))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_6298.RollingRingAssemblyAdvancedSystemDeflection]':
        '''List[RollingRingAssemblyAdvancedSystemDeflection]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_6298.RollingRingAssemblyAdvancedSystemDeflection))
        return value

    @property
    def shafts(self) -> 'List[_6301.ShaftAdvancedSystemDeflection]':
        '''List[ShaftAdvancedSystemDeflection]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_6301.ShaftAdvancedSystemDeflection))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_6307.SpiralBevelGearSetAdvancedSystemDeflection]':
        '''List[SpiralBevelGearSetAdvancedSystemDeflection]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_6307.SpiralBevelGearSetAdvancedSystemDeflection))
        return value

    @property
    def spring_dampers(self) -> 'List[_6308.SpringDamperAdvancedSystemDeflection]':
        '''List[SpringDamperAdvancedSystemDeflection]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_6308.SpringDamperAdvancedSystemDeflection))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_6313.StraightBevelDiffGearSetAdvancedSystemDeflection]':
        '''List[StraightBevelDiffGearSetAdvancedSystemDeflection]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_6313.StraightBevelDiffGearSetAdvancedSystemDeflection))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_6316.StraightBevelGearSetAdvancedSystemDeflection]':
        '''List[StraightBevelGearSetAdvancedSystemDeflection]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_6316.StraightBevelGearSetAdvancedSystemDeflection))
        return value

    @property
    def synchronisers(self) -> 'List[_6319.SynchroniserAdvancedSystemDeflection]':
        '''List[SynchroniserAdvancedSystemDeflection]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_6319.SynchroniserAdvancedSystemDeflection))
        return value

    @property
    def torque_converters(self) -> 'List[_6323.TorqueConverterAdvancedSystemDeflection]':
        '''List[TorqueConverterAdvancedSystemDeflection]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_6323.TorqueConverterAdvancedSystemDeflection))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_6328.UnbalancedMassAdvancedSystemDeflection]':
        '''List[UnbalancedMassAdvancedSystemDeflection]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_6328.UnbalancedMassAdvancedSystemDeflection))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_6333.WormGearSetAdvancedSystemDeflection]':
        '''List[WormGearSetAdvancedSystemDeflection]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_6333.WormGearSetAdvancedSystemDeflection))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_6336.ZerolBevelGearSetAdvancedSystemDeflection]':
        '''List[ZerolBevelGearSetAdvancedSystemDeflection]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_6336.ZerolBevelGearSetAdvancedSystemDeflection))
        return value

    @property
    def assembly_system_deflection_results(self) -> 'List[_2189.AssemblySystemDeflection]':
        '''List[AssemblySystemDeflection]: 'AssemblySystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionResults, constructor.new(_2189.AssemblySystemDeflection))
        return value
