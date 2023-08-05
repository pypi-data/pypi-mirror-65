'''_4216.py

AssemblyModalAnalysisAtAStiffness
'''


from typing import List

from mastapy.system_model.part_model import _1979
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6052
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_stiffness import (
    _4217, _4219, _4222, _4229,
    _4228, _4232, _4237, _4240,
    _4250, _4254, _4261, _4262,
    _4269, _4270, _4277, _4280,
    _4281, _4282, _4285, _4289,
    _4292, _4293, _4294, _4300,
    _4296, _4301, _4306, _4309,
    _4312, _4315, _4319, _4323,
    _4326, _4330, _4333, _4211
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_MODAL_ANALYSIS_AT_A_STIFFNESS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtAStiffness', 'AssemblyModalAnalysisAtAStiffness')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyModalAnalysisAtAStiffness',)


class AssemblyModalAnalysisAtAStiffness(_4211.AbstractAssemblyModalAnalysisAtAStiffness):
    '''AssemblyModalAnalysisAtAStiffness

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_MODAL_ANALYSIS_AT_A_STIFFNESS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyModalAnalysisAtAStiffness.TYPE'):
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
    def bearings(self) -> 'List[_4217.BearingModalAnalysisAtAStiffness]':
        '''List[BearingModalAnalysisAtAStiffness]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_4217.BearingModalAnalysisAtAStiffness))
        return value

    @property
    def belt_drives(self) -> 'List[_4219.BeltDriveModalAnalysisAtAStiffness]':
        '''List[BeltDriveModalAnalysisAtAStiffness]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_4219.BeltDriveModalAnalysisAtAStiffness))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_4222.BevelDifferentialGearSetModalAnalysisAtAStiffness]':
        '''List[BevelDifferentialGearSetModalAnalysisAtAStiffness]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_4222.BevelDifferentialGearSetModalAnalysisAtAStiffness))
        return value

    @property
    def bolts(self) -> 'List[_4229.BoltModalAnalysisAtAStiffness]':
        '''List[BoltModalAnalysisAtAStiffness]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_4229.BoltModalAnalysisAtAStiffness))
        return value

    @property
    def bolted_joints(self) -> 'List[_4228.BoltedJointModalAnalysisAtAStiffness]':
        '''List[BoltedJointModalAnalysisAtAStiffness]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_4228.BoltedJointModalAnalysisAtAStiffness))
        return value

    @property
    def clutches(self) -> 'List[_4232.ClutchModalAnalysisAtAStiffness]':
        '''List[ClutchModalAnalysisAtAStiffness]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_4232.ClutchModalAnalysisAtAStiffness))
        return value

    @property
    def concept_couplings(self) -> 'List[_4237.ConceptCouplingModalAnalysisAtAStiffness]':
        '''List[ConceptCouplingModalAnalysisAtAStiffness]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_4237.ConceptCouplingModalAnalysisAtAStiffness))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_4240.ConceptGearSetModalAnalysisAtAStiffness]':
        '''List[ConceptGearSetModalAnalysisAtAStiffness]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_4240.ConceptGearSetModalAnalysisAtAStiffness))
        return value

    @property
    def cv_ts(self) -> 'List[_4250.CVTModalAnalysisAtAStiffness]':
        '''List[CVTModalAnalysisAtAStiffness]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_4250.CVTModalAnalysisAtAStiffness))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_4254.CylindricalGearSetModalAnalysisAtAStiffness]':
        '''List[CylindricalGearSetModalAnalysisAtAStiffness]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_4254.CylindricalGearSetModalAnalysisAtAStiffness))
        return value

    @property
    def face_gear_sets(self) -> 'List[_4261.FaceGearSetModalAnalysisAtAStiffness]':
        '''List[FaceGearSetModalAnalysisAtAStiffness]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_4261.FaceGearSetModalAnalysisAtAStiffness))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_4262.FlexiblePinAssemblyModalAnalysisAtAStiffness]':
        '''List[FlexiblePinAssemblyModalAnalysisAtAStiffness]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_4262.FlexiblePinAssemblyModalAnalysisAtAStiffness))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_4269.HypoidGearSetModalAnalysisAtAStiffness]':
        '''List[HypoidGearSetModalAnalysisAtAStiffness]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_4269.HypoidGearSetModalAnalysisAtAStiffness))
        return value

    @property
    def imported_fe_components(self) -> 'List[_4270.ImportedFEComponentModalAnalysisAtAStiffness]':
        '''List[ImportedFEComponentModalAnalysisAtAStiffness]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_4270.ImportedFEComponentModalAnalysisAtAStiffness))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_4277.KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtAStiffness]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtAStiffness]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_4277.KlingelnbergCycloPalloidHypoidGearSetModalAnalysisAtAStiffness))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_4280.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtAStiffness]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtAStiffness]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_4280.KlingelnbergCycloPalloidSpiralBevelGearSetModalAnalysisAtAStiffness))
        return value

    @property
    def mass_discs(self) -> 'List[_4281.MassDiscModalAnalysisAtAStiffness]':
        '''List[MassDiscModalAnalysisAtAStiffness]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_4281.MassDiscModalAnalysisAtAStiffness))
        return value

    @property
    def measurement_components(self) -> 'List[_4282.MeasurementComponentModalAnalysisAtAStiffness]':
        '''List[MeasurementComponentModalAnalysisAtAStiffness]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_4282.MeasurementComponentModalAnalysisAtAStiffness))
        return value

    @property
    def oil_seals(self) -> 'List[_4285.OilSealModalAnalysisAtAStiffness]':
        '''List[OilSealModalAnalysisAtAStiffness]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_4285.OilSealModalAnalysisAtAStiffness))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_4289.PartToPartShearCouplingModalAnalysisAtAStiffness]':
        '''List[PartToPartShearCouplingModalAnalysisAtAStiffness]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_4289.PartToPartShearCouplingModalAnalysisAtAStiffness))
        return value

    @property
    def planet_carriers(self) -> 'List[_4292.PlanetCarrierModalAnalysisAtAStiffness]':
        '''List[PlanetCarrierModalAnalysisAtAStiffness]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_4292.PlanetCarrierModalAnalysisAtAStiffness))
        return value

    @property
    def point_loads(self) -> 'List[_4293.PointLoadModalAnalysisAtAStiffness]':
        '''List[PointLoadModalAnalysisAtAStiffness]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_4293.PointLoadModalAnalysisAtAStiffness))
        return value

    @property
    def power_loads(self) -> 'List[_4294.PowerLoadModalAnalysisAtAStiffness]':
        '''List[PowerLoadModalAnalysisAtAStiffness]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_4294.PowerLoadModalAnalysisAtAStiffness))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_4300.ShaftHubConnectionModalAnalysisAtAStiffness]':
        '''List[ShaftHubConnectionModalAnalysisAtAStiffness]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_4300.ShaftHubConnectionModalAnalysisAtAStiffness))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_4296.RollingRingAssemblyModalAnalysisAtAStiffness]':
        '''List[RollingRingAssemblyModalAnalysisAtAStiffness]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_4296.RollingRingAssemblyModalAnalysisAtAStiffness))
        return value

    @property
    def shafts(self) -> 'List[_4301.ShaftModalAnalysisAtAStiffness]':
        '''List[ShaftModalAnalysisAtAStiffness]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_4301.ShaftModalAnalysisAtAStiffness))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_4306.SpiralBevelGearSetModalAnalysisAtAStiffness]':
        '''List[SpiralBevelGearSetModalAnalysisAtAStiffness]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_4306.SpiralBevelGearSetModalAnalysisAtAStiffness))
        return value

    @property
    def spring_dampers(self) -> 'List[_4309.SpringDamperModalAnalysisAtAStiffness]':
        '''List[SpringDamperModalAnalysisAtAStiffness]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_4309.SpringDamperModalAnalysisAtAStiffness))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_4312.StraightBevelDiffGearSetModalAnalysisAtAStiffness]':
        '''List[StraightBevelDiffGearSetModalAnalysisAtAStiffness]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_4312.StraightBevelDiffGearSetModalAnalysisAtAStiffness))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_4315.StraightBevelGearSetModalAnalysisAtAStiffness]':
        '''List[StraightBevelGearSetModalAnalysisAtAStiffness]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_4315.StraightBevelGearSetModalAnalysisAtAStiffness))
        return value

    @property
    def synchronisers(self) -> 'List[_4319.SynchroniserModalAnalysisAtAStiffness]':
        '''List[SynchroniserModalAnalysisAtAStiffness]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_4319.SynchroniserModalAnalysisAtAStiffness))
        return value

    @property
    def torque_converters(self) -> 'List[_4323.TorqueConverterModalAnalysisAtAStiffness]':
        '''List[TorqueConverterModalAnalysisAtAStiffness]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_4323.TorqueConverterModalAnalysisAtAStiffness))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_4326.UnbalancedMassModalAnalysisAtAStiffness]':
        '''List[UnbalancedMassModalAnalysisAtAStiffness]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_4326.UnbalancedMassModalAnalysisAtAStiffness))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_4330.WormGearSetModalAnalysisAtAStiffness]':
        '''List[WormGearSetModalAnalysisAtAStiffness]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_4330.WormGearSetModalAnalysisAtAStiffness))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_4333.ZerolBevelGearSetModalAnalysisAtAStiffness]':
        '''List[ZerolBevelGearSetModalAnalysisAtAStiffness]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_4333.ZerolBevelGearSetModalAnalysisAtAStiffness))
        return value
