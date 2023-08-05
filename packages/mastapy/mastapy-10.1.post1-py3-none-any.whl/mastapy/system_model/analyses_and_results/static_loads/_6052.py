'''_6052.py

AssemblyLoadCase
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model import _1979
from mastapy.system_model.analyses_and_results.static_loads import (
    _6053, _6055, _6058, _6065,
    _6064, _6068, _6073, _6076,
    _6088, _6094, _6114, _6115,
    _6134, _6135, _6143, _6146,
    _6147, _6148, _6152, _6157,
    _6161, _6164, _6165, _6172,
    _6168, _6173, _6179, _6182,
    _6186, _6189, _6193, _6199,
    _6206, _6210, _6213, _6046,
    _6066, _6119, _6045
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_LOAD_CASE = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.StaticLoads', 'AssemblyLoadCase')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyLoadCase',)


class AssemblyLoadCase(_6045.AbstractAssemblyLoadCase):
    '''AssemblyLoadCase

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_LOAD_CASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyLoadCase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def volume_of_oil_in_sump(self) -> 'float':
        '''float: 'VolumeOfOilInSump' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.VolumeOfOilInSump

    @property
    def assembly_design(self) -> '_1979.Assembly':
        '''Assembly: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1979.Assembly)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def bearings(self) -> 'List[_6053.BearingLoadCase]':
        '''List[BearingLoadCase]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_6053.BearingLoadCase))
        return value

    @property
    def belt_drives(self) -> 'List[_6055.BeltDriveLoadCase]':
        '''List[BeltDriveLoadCase]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_6055.BeltDriveLoadCase))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_6058.BevelDifferentialGearSetLoadCase]':
        '''List[BevelDifferentialGearSetLoadCase]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_6058.BevelDifferentialGearSetLoadCase))
        return value

    @property
    def bolts(self) -> 'List[_6065.BoltLoadCase]':
        '''List[BoltLoadCase]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_6065.BoltLoadCase))
        return value

    @property
    def bolted_joints(self) -> 'List[_6064.BoltedJointLoadCase]':
        '''List[BoltedJointLoadCase]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_6064.BoltedJointLoadCase))
        return value

    @property
    def clutches(self) -> 'List[_6068.ClutchLoadCase]':
        '''List[ClutchLoadCase]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_6068.ClutchLoadCase))
        return value

    @property
    def concept_couplings(self) -> 'List[_6073.ConceptCouplingLoadCase]':
        '''List[ConceptCouplingLoadCase]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_6073.ConceptCouplingLoadCase))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_6076.ConceptGearSetLoadCase]':
        '''List[ConceptGearSetLoadCase]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_6076.ConceptGearSetLoadCase))
        return value

    @property
    def cv_ts(self) -> 'List[_6088.CVTLoadCase]':
        '''List[CVTLoadCase]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_6088.CVTLoadCase))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_6094.CylindricalGearSetLoadCase]':
        '''List[CylindricalGearSetLoadCase]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_6094.CylindricalGearSetLoadCase))
        return value

    @property
    def face_gear_sets(self) -> 'List[_6114.FaceGearSetLoadCase]':
        '''List[FaceGearSetLoadCase]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_6114.FaceGearSetLoadCase))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_6115.FlexiblePinAssemblyLoadCase]':
        '''List[FlexiblePinAssemblyLoadCase]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_6115.FlexiblePinAssemblyLoadCase))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_6134.HypoidGearSetLoadCase]':
        '''List[HypoidGearSetLoadCase]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_6134.HypoidGearSetLoadCase))
        return value

    @property
    def imported_fe_components(self) -> 'List[_6135.ImportedFEComponentLoadCase]':
        '''List[ImportedFEComponentLoadCase]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_6135.ImportedFEComponentLoadCase))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_6143.KlingelnbergCycloPalloidHypoidGearSetLoadCase]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetLoadCase]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_6143.KlingelnbergCycloPalloidHypoidGearSetLoadCase))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_6146.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_6146.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase))
        return value

    @property
    def mass_discs(self) -> 'List[_6147.MassDiscLoadCase]':
        '''List[MassDiscLoadCase]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_6147.MassDiscLoadCase))
        return value

    @property
    def measurement_components(self) -> 'List[_6148.MeasurementComponentLoadCase]':
        '''List[MeasurementComponentLoadCase]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_6148.MeasurementComponentLoadCase))
        return value

    @property
    def oil_seals(self) -> 'List[_6152.OilSealLoadCase]':
        '''List[OilSealLoadCase]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_6152.OilSealLoadCase))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_6157.PartToPartShearCouplingLoadCase]':
        '''List[PartToPartShearCouplingLoadCase]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_6157.PartToPartShearCouplingLoadCase))
        return value

    @property
    def planet_carriers(self) -> 'List[_6161.PlanetCarrierLoadCase]':
        '''List[PlanetCarrierLoadCase]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_6161.PlanetCarrierLoadCase))
        return value

    @property
    def point_loads(self) -> 'List[_6164.PointLoadLoadCase]':
        '''List[PointLoadLoadCase]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_6164.PointLoadLoadCase))
        return value

    @property
    def power_loads(self) -> 'List[_6165.PowerLoadLoadCase]':
        '''List[PowerLoadLoadCase]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_6165.PowerLoadLoadCase))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_6172.ShaftHubConnectionLoadCase]':
        '''List[ShaftHubConnectionLoadCase]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_6172.ShaftHubConnectionLoadCase))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_6168.RollingRingAssemblyLoadCase]':
        '''List[RollingRingAssemblyLoadCase]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_6168.RollingRingAssemblyLoadCase))
        return value

    @property
    def shafts(self) -> 'List[_6173.ShaftLoadCase]':
        '''List[ShaftLoadCase]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_6173.ShaftLoadCase))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_6179.SpiralBevelGearSetLoadCase]':
        '''List[SpiralBevelGearSetLoadCase]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_6179.SpiralBevelGearSetLoadCase))
        return value

    @property
    def spring_dampers(self) -> 'List[_6182.SpringDamperLoadCase]':
        '''List[SpringDamperLoadCase]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_6182.SpringDamperLoadCase))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_6186.StraightBevelDiffGearSetLoadCase]':
        '''List[StraightBevelDiffGearSetLoadCase]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_6186.StraightBevelDiffGearSetLoadCase))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_6189.StraightBevelGearSetLoadCase]':
        '''List[StraightBevelGearSetLoadCase]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_6189.StraightBevelGearSetLoadCase))
        return value

    @property
    def synchronisers(self) -> 'List[_6193.SynchroniserLoadCase]':
        '''List[SynchroniserLoadCase]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_6193.SynchroniserLoadCase))
        return value

    @property
    def torque_converters(self) -> 'List[_6199.TorqueConverterLoadCase]':
        '''List[TorqueConverterLoadCase]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_6199.TorqueConverterLoadCase))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_6206.UnbalancedMassLoadCase]':
        '''List[UnbalancedMassLoadCase]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_6206.UnbalancedMassLoadCase))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_6210.WormGearSetLoadCase]':
        '''List[WormGearSetLoadCase]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_6210.WormGearSetLoadCase))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_6213.ZerolBevelGearSetLoadCase]':
        '''List[ZerolBevelGearSetLoadCase]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_6213.ZerolBevelGearSetLoadCase))
        return value

    @property
    def shafts_and_housings(self) -> 'List[_6046.AbstractShaftOrHousingLoadCase]':
        '''List[AbstractShaftOrHousingLoadCase]: 'ShaftsAndHousings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftsAndHousings, constructor.new(_6046.AbstractShaftOrHousingLoadCase))
        return value

    @property
    def clutch_connections(self) -> 'List[_6066.ClutchConnectionLoadCase]':
        '''List[ClutchConnectionLoadCase]: 'ClutchConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ClutchConnections, constructor.new(_6066.ClutchConnectionLoadCase))
        return value

    @property
    def gear_meshes(self) -> 'List[_6119.GearMeshLoadCase]':
        '''List[GearMeshLoadCase]: 'GearMeshes' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearMeshes, constructor.new(_6119.GearMeshLoadCase))
        return value
