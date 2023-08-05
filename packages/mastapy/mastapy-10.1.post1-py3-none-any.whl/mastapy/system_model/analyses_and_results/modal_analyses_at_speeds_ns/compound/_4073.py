'''_4073.py

AssemblyCompoundModalAnalysesAtSpeeds
'''


from typing import List

from mastapy.system_model.part_model import _1957
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _3948
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns.compound import (
    _4074, _4076, _4079, _4085,
    _4086, _4087, _4092, _4097,
    _4107, _4111, _4117, _4118,
    _4125, _4126, _4133, _4136,
    _4137, _4138, _4140, _4142,
    _4147, _4148, _4149, _4156,
    _4151, _4155, _4161, _4162,
    _4167, _4170, _4173, _4177,
    _4181, _4185, _4188, _4068
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS.Compound', 'AssemblyCompoundModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundModalAnalysesAtSpeeds',)


class AssemblyCompoundModalAnalysesAtSpeeds(_4068.AbstractAssemblyCompoundModalAnalysesAtSpeeds):
    '''AssemblyCompoundModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundModalAnalysesAtSpeeds.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_3948.AssemblyModalAnalysesAtSpeeds]':
        '''List[AssemblyModalAnalysesAtSpeeds]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3948.AssemblyModalAnalysesAtSpeeds))
        return value

    @property
    def assembly_modal_analyses_at_speeds_load_cases(self) -> 'List[_3948.AssemblyModalAnalysesAtSpeeds]':
        '''List[AssemblyModalAnalysesAtSpeeds]: 'AssemblyModalAnalysesAtSpeedsLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysesAtSpeedsLoadCases, constructor.new(_3948.AssemblyModalAnalysesAtSpeeds))
        return value

    @property
    def bearings(self) -> 'List[_4074.BearingCompoundModalAnalysesAtSpeeds]':
        '''List[BearingCompoundModalAnalysesAtSpeeds]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_4074.BearingCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def belt_drives(self) -> 'List[_4076.BeltDriveCompoundModalAnalysesAtSpeeds]':
        '''List[BeltDriveCompoundModalAnalysesAtSpeeds]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_4076.BeltDriveCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_4079.BevelDifferentialGearSetCompoundModalAnalysesAtSpeeds]':
        '''List[BevelDifferentialGearSetCompoundModalAnalysesAtSpeeds]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_4079.BevelDifferentialGearSetCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def bolts(self) -> 'List[_4085.BoltCompoundModalAnalysesAtSpeeds]':
        '''List[BoltCompoundModalAnalysesAtSpeeds]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_4085.BoltCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def bolted_joints(self) -> 'List[_4086.BoltedJointCompoundModalAnalysesAtSpeeds]':
        '''List[BoltedJointCompoundModalAnalysesAtSpeeds]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_4086.BoltedJointCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def clutches(self) -> 'List[_4087.ClutchCompoundModalAnalysesAtSpeeds]':
        '''List[ClutchCompoundModalAnalysesAtSpeeds]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_4087.ClutchCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def concept_couplings(self) -> 'List[_4092.ConceptCouplingCompoundModalAnalysesAtSpeeds]':
        '''List[ConceptCouplingCompoundModalAnalysesAtSpeeds]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_4092.ConceptCouplingCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_4097.ConceptGearSetCompoundModalAnalysesAtSpeeds]':
        '''List[ConceptGearSetCompoundModalAnalysesAtSpeeds]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_4097.ConceptGearSetCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def cv_ts(self) -> 'List[_4107.CVTCompoundModalAnalysesAtSpeeds]':
        '''List[CVTCompoundModalAnalysesAtSpeeds]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_4107.CVTCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_4111.CylindricalGearSetCompoundModalAnalysesAtSpeeds]':
        '''List[CylindricalGearSetCompoundModalAnalysesAtSpeeds]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_4111.CylindricalGearSetCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def face_gear_sets(self) -> 'List[_4117.FaceGearSetCompoundModalAnalysesAtSpeeds]':
        '''List[FaceGearSetCompoundModalAnalysesAtSpeeds]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_4117.FaceGearSetCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_4118.FlexiblePinAssemblyCompoundModalAnalysesAtSpeeds]':
        '''List[FlexiblePinAssemblyCompoundModalAnalysesAtSpeeds]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_4118.FlexiblePinAssemblyCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_4125.HypoidGearSetCompoundModalAnalysesAtSpeeds]':
        '''List[HypoidGearSetCompoundModalAnalysesAtSpeeds]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_4125.HypoidGearSetCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def imported_fe_components(self) -> 'List[_4126.ImportedFEComponentCompoundModalAnalysesAtSpeeds]':
        '''List[ImportedFEComponentCompoundModalAnalysesAtSpeeds]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_4126.ImportedFEComponentCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_4133.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysesAtSpeeds]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysesAtSpeeds]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_4133.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_4136.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysesAtSpeeds]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysesAtSpeeds]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_4136.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def mass_discs(self) -> 'List[_4137.MassDiscCompoundModalAnalysesAtSpeeds]':
        '''List[MassDiscCompoundModalAnalysesAtSpeeds]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_4137.MassDiscCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def measurement_components(self) -> 'List[_4138.MeasurementComponentCompoundModalAnalysesAtSpeeds]':
        '''List[MeasurementComponentCompoundModalAnalysesAtSpeeds]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_4138.MeasurementComponentCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def oil_seals(self) -> 'List[_4140.OilSealCompoundModalAnalysesAtSpeeds]':
        '''List[OilSealCompoundModalAnalysesAtSpeeds]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_4140.OilSealCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_4142.PartToPartShearCouplingCompoundModalAnalysesAtSpeeds]':
        '''List[PartToPartShearCouplingCompoundModalAnalysesAtSpeeds]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_4142.PartToPartShearCouplingCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def planet_carriers(self) -> 'List[_4147.PlanetCarrierCompoundModalAnalysesAtSpeeds]':
        '''List[PlanetCarrierCompoundModalAnalysesAtSpeeds]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_4147.PlanetCarrierCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def point_loads(self) -> 'List[_4148.PointLoadCompoundModalAnalysesAtSpeeds]':
        '''List[PointLoadCompoundModalAnalysesAtSpeeds]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_4148.PointLoadCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def power_loads(self) -> 'List[_4149.PowerLoadCompoundModalAnalysesAtSpeeds]':
        '''List[PowerLoadCompoundModalAnalysesAtSpeeds]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_4149.PowerLoadCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_4156.ShaftHubConnectionCompoundModalAnalysesAtSpeeds]':
        '''List[ShaftHubConnectionCompoundModalAnalysesAtSpeeds]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_4156.ShaftHubConnectionCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_4151.RollingRingAssemblyCompoundModalAnalysesAtSpeeds]':
        '''List[RollingRingAssemblyCompoundModalAnalysesAtSpeeds]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_4151.RollingRingAssemblyCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def shafts(self) -> 'List[_4155.ShaftCompoundModalAnalysesAtSpeeds]':
        '''List[ShaftCompoundModalAnalysesAtSpeeds]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_4155.ShaftCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_4161.SpiralBevelGearSetCompoundModalAnalysesAtSpeeds]':
        '''List[SpiralBevelGearSetCompoundModalAnalysesAtSpeeds]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_4161.SpiralBevelGearSetCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def spring_dampers(self) -> 'List[_4162.SpringDamperCompoundModalAnalysesAtSpeeds]':
        '''List[SpringDamperCompoundModalAnalysesAtSpeeds]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_4162.SpringDamperCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_4167.StraightBevelDiffGearSetCompoundModalAnalysesAtSpeeds]':
        '''List[StraightBevelDiffGearSetCompoundModalAnalysesAtSpeeds]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_4167.StraightBevelDiffGearSetCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_4170.StraightBevelGearSetCompoundModalAnalysesAtSpeeds]':
        '''List[StraightBevelGearSetCompoundModalAnalysesAtSpeeds]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_4170.StraightBevelGearSetCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def synchronisers(self) -> 'List[_4173.SynchroniserCompoundModalAnalysesAtSpeeds]':
        '''List[SynchroniserCompoundModalAnalysesAtSpeeds]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_4173.SynchroniserCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def torque_converters(self) -> 'List[_4177.TorqueConverterCompoundModalAnalysesAtSpeeds]':
        '''List[TorqueConverterCompoundModalAnalysesAtSpeeds]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_4177.TorqueConverterCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_4181.UnbalancedMassCompoundModalAnalysesAtSpeeds]':
        '''List[UnbalancedMassCompoundModalAnalysesAtSpeeds]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_4181.UnbalancedMassCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_4185.WormGearSetCompoundModalAnalysesAtSpeeds]':
        '''List[WormGearSetCompoundModalAnalysesAtSpeeds]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_4185.WormGearSetCompoundModalAnalysesAtSpeeds))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_4188.ZerolBevelGearSetCompoundModalAnalysesAtSpeeds]':
        '''List[ZerolBevelGearSetCompoundModalAnalysesAtSpeeds]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_4188.ZerolBevelGearSetCompoundModalAnalysesAtSpeeds))
        return value
