'''_6364.py

AssemblyCompoundAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.part_model import _1979
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6239
from mastapy.system_model.analyses_and_results.advanced_system_deflections.compound import (
    _6365, _6367, _6370, _6376,
    _6377, _6378, _6383, _6388,
    _6398, _6402, _6408, _6409,
    _6416, _6417, _6424, _6427,
    _6428, _6429, _6431, _6433,
    _6438, _6439, _6440, _6447,
    _6442, _6446, _6452, _6453,
    _6458, _6461, _6464, _6468,
    _6472, _6476, _6479, _6359
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections.Compound', 'AssemblyCompoundAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundAdvancedSystemDeflection',)


class AssemblyCompoundAdvancedSystemDeflection(_6359.AbstractAssemblyCompoundAdvancedSystemDeflection):
    '''AssemblyCompoundAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundAdvancedSystemDeflection.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_6239.AssemblyAdvancedSystemDeflection]':
        '''List[AssemblyAdvancedSystemDeflection]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_6239.AssemblyAdvancedSystemDeflection))
        return value

    @property
    def assembly_advanced_system_deflection_load_cases(self) -> 'List[_6239.AssemblyAdvancedSystemDeflection]':
        '''List[AssemblyAdvancedSystemDeflection]: 'AssemblyAdvancedSystemDeflectionLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyAdvancedSystemDeflectionLoadCases, constructor.new(_6239.AssemblyAdvancedSystemDeflection))
        return value

    @property
    def bearings(self) -> 'List[_6365.BearingCompoundAdvancedSystemDeflection]':
        '''List[BearingCompoundAdvancedSystemDeflection]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_6365.BearingCompoundAdvancedSystemDeflection))
        return value

    @property
    def belt_drives(self) -> 'List[_6367.BeltDriveCompoundAdvancedSystemDeflection]':
        '''List[BeltDriveCompoundAdvancedSystemDeflection]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_6367.BeltDriveCompoundAdvancedSystemDeflection))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_6370.BevelDifferentialGearSetCompoundAdvancedSystemDeflection]':
        '''List[BevelDifferentialGearSetCompoundAdvancedSystemDeflection]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_6370.BevelDifferentialGearSetCompoundAdvancedSystemDeflection))
        return value

    @property
    def bolts(self) -> 'List[_6376.BoltCompoundAdvancedSystemDeflection]':
        '''List[BoltCompoundAdvancedSystemDeflection]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_6376.BoltCompoundAdvancedSystemDeflection))
        return value

    @property
    def bolted_joints(self) -> 'List[_6377.BoltedJointCompoundAdvancedSystemDeflection]':
        '''List[BoltedJointCompoundAdvancedSystemDeflection]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_6377.BoltedJointCompoundAdvancedSystemDeflection))
        return value

    @property
    def clutches(self) -> 'List[_6378.ClutchCompoundAdvancedSystemDeflection]':
        '''List[ClutchCompoundAdvancedSystemDeflection]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_6378.ClutchCompoundAdvancedSystemDeflection))
        return value

    @property
    def concept_couplings(self) -> 'List[_6383.ConceptCouplingCompoundAdvancedSystemDeflection]':
        '''List[ConceptCouplingCompoundAdvancedSystemDeflection]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_6383.ConceptCouplingCompoundAdvancedSystemDeflection))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_6388.ConceptGearSetCompoundAdvancedSystemDeflection]':
        '''List[ConceptGearSetCompoundAdvancedSystemDeflection]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_6388.ConceptGearSetCompoundAdvancedSystemDeflection))
        return value

    @property
    def cv_ts(self) -> 'List[_6398.CVTCompoundAdvancedSystemDeflection]':
        '''List[CVTCompoundAdvancedSystemDeflection]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_6398.CVTCompoundAdvancedSystemDeflection))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_6402.CylindricalGearSetCompoundAdvancedSystemDeflection]':
        '''List[CylindricalGearSetCompoundAdvancedSystemDeflection]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_6402.CylindricalGearSetCompoundAdvancedSystemDeflection))
        return value

    @property
    def face_gear_sets(self) -> 'List[_6408.FaceGearSetCompoundAdvancedSystemDeflection]':
        '''List[FaceGearSetCompoundAdvancedSystemDeflection]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_6408.FaceGearSetCompoundAdvancedSystemDeflection))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_6409.FlexiblePinAssemblyCompoundAdvancedSystemDeflection]':
        '''List[FlexiblePinAssemblyCompoundAdvancedSystemDeflection]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_6409.FlexiblePinAssemblyCompoundAdvancedSystemDeflection))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_6416.HypoidGearSetCompoundAdvancedSystemDeflection]':
        '''List[HypoidGearSetCompoundAdvancedSystemDeflection]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_6416.HypoidGearSetCompoundAdvancedSystemDeflection))
        return value

    @property
    def imported_fe_components(self) -> 'List[_6417.ImportedFEComponentCompoundAdvancedSystemDeflection]':
        '''List[ImportedFEComponentCompoundAdvancedSystemDeflection]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_6417.ImportedFEComponentCompoundAdvancedSystemDeflection))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_6424.KlingelnbergCycloPalloidHypoidGearSetCompoundAdvancedSystemDeflection]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundAdvancedSystemDeflection]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_6424.KlingelnbergCycloPalloidHypoidGearSetCompoundAdvancedSystemDeflection))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_6427.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedSystemDeflection]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedSystemDeflection]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_6427.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundAdvancedSystemDeflection))
        return value

    @property
    def mass_discs(self) -> 'List[_6428.MassDiscCompoundAdvancedSystemDeflection]':
        '''List[MassDiscCompoundAdvancedSystemDeflection]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_6428.MassDiscCompoundAdvancedSystemDeflection))
        return value

    @property
    def measurement_components(self) -> 'List[_6429.MeasurementComponentCompoundAdvancedSystemDeflection]':
        '''List[MeasurementComponentCompoundAdvancedSystemDeflection]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_6429.MeasurementComponentCompoundAdvancedSystemDeflection))
        return value

    @property
    def oil_seals(self) -> 'List[_6431.OilSealCompoundAdvancedSystemDeflection]':
        '''List[OilSealCompoundAdvancedSystemDeflection]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_6431.OilSealCompoundAdvancedSystemDeflection))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_6433.PartToPartShearCouplingCompoundAdvancedSystemDeflection]':
        '''List[PartToPartShearCouplingCompoundAdvancedSystemDeflection]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_6433.PartToPartShearCouplingCompoundAdvancedSystemDeflection))
        return value

    @property
    def planet_carriers(self) -> 'List[_6438.PlanetCarrierCompoundAdvancedSystemDeflection]':
        '''List[PlanetCarrierCompoundAdvancedSystemDeflection]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_6438.PlanetCarrierCompoundAdvancedSystemDeflection))
        return value

    @property
    def point_loads(self) -> 'List[_6439.PointLoadCompoundAdvancedSystemDeflection]':
        '''List[PointLoadCompoundAdvancedSystemDeflection]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_6439.PointLoadCompoundAdvancedSystemDeflection))
        return value

    @property
    def power_loads(self) -> 'List[_6440.PowerLoadCompoundAdvancedSystemDeflection]':
        '''List[PowerLoadCompoundAdvancedSystemDeflection]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_6440.PowerLoadCompoundAdvancedSystemDeflection))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_6447.ShaftHubConnectionCompoundAdvancedSystemDeflection]':
        '''List[ShaftHubConnectionCompoundAdvancedSystemDeflection]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_6447.ShaftHubConnectionCompoundAdvancedSystemDeflection))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_6442.RollingRingAssemblyCompoundAdvancedSystemDeflection]':
        '''List[RollingRingAssemblyCompoundAdvancedSystemDeflection]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_6442.RollingRingAssemblyCompoundAdvancedSystemDeflection))
        return value

    @property
    def shafts(self) -> 'List[_6446.ShaftCompoundAdvancedSystemDeflection]':
        '''List[ShaftCompoundAdvancedSystemDeflection]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_6446.ShaftCompoundAdvancedSystemDeflection))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_6452.SpiralBevelGearSetCompoundAdvancedSystemDeflection]':
        '''List[SpiralBevelGearSetCompoundAdvancedSystemDeflection]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_6452.SpiralBevelGearSetCompoundAdvancedSystemDeflection))
        return value

    @property
    def spring_dampers(self) -> 'List[_6453.SpringDamperCompoundAdvancedSystemDeflection]':
        '''List[SpringDamperCompoundAdvancedSystemDeflection]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_6453.SpringDamperCompoundAdvancedSystemDeflection))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_6458.StraightBevelDiffGearSetCompoundAdvancedSystemDeflection]':
        '''List[StraightBevelDiffGearSetCompoundAdvancedSystemDeflection]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_6458.StraightBevelDiffGearSetCompoundAdvancedSystemDeflection))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_6461.StraightBevelGearSetCompoundAdvancedSystemDeflection]':
        '''List[StraightBevelGearSetCompoundAdvancedSystemDeflection]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_6461.StraightBevelGearSetCompoundAdvancedSystemDeflection))
        return value

    @property
    def synchronisers(self) -> 'List[_6464.SynchroniserCompoundAdvancedSystemDeflection]':
        '''List[SynchroniserCompoundAdvancedSystemDeflection]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_6464.SynchroniserCompoundAdvancedSystemDeflection))
        return value

    @property
    def torque_converters(self) -> 'List[_6468.TorqueConverterCompoundAdvancedSystemDeflection]':
        '''List[TorqueConverterCompoundAdvancedSystemDeflection]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_6468.TorqueConverterCompoundAdvancedSystemDeflection))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_6472.UnbalancedMassCompoundAdvancedSystemDeflection]':
        '''List[UnbalancedMassCompoundAdvancedSystemDeflection]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_6472.UnbalancedMassCompoundAdvancedSystemDeflection))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_6476.WormGearSetCompoundAdvancedSystemDeflection]':
        '''List[WormGearSetCompoundAdvancedSystemDeflection]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_6476.WormGearSetCompoundAdvancedSystemDeflection))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_6479.ZerolBevelGearSetCompoundAdvancedSystemDeflection]':
        '''List[ZerolBevelGearSetCompoundAdvancedSystemDeflection]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_6479.ZerolBevelGearSetCompoundAdvancedSystemDeflection))
        return value
