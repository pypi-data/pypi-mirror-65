'''_3827.py

AssemblyCompoundModalAnalysesAtStiffnesses
'''


from typing import List

from mastapy.system_model.part_model import _1957
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3703
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns.compound import (
    _3828, _3830, _3833, _3839,
    _3840, _3841, _3846, _3851,
    _3861, _3865, _3871, _3872,
    _3879, _3880, _3887, _3890,
    _3891, _3892, _3894, _3896,
    _3901, _3902, _3903, _3910,
    _3905, _3909, _3915, _3916,
    _3921, _3924, _3927, _3931,
    _3935, _3939, _3942, _3822
)
from mastapy._internal.python_net import python_net_import

_ASSEMBLY_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS.Compound', 'AssemblyCompoundModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('AssemblyCompoundModalAnalysesAtStiffnesses',)


class AssemblyCompoundModalAnalysesAtStiffnesses(_3822.AbstractAssemblyCompoundModalAnalysesAtStiffnesses):
    '''AssemblyCompoundModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _ASSEMBLY_COMPOUND_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AssemblyCompoundModalAnalysesAtStiffnesses.TYPE'):
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
    def load_case_analyses_ready(self) -> 'List[_3703.AssemblyModalAnalysesAtStiffnesses]':
        '''List[AssemblyModalAnalysesAtStiffnesses]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_3703.AssemblyModalAnalysesAtStiffnesses))
        return value

    @property
    def assembly_modal_analyses_at_stiffnesses_load_cases(self) -> 'List[_3703.AssemblyModalAnalysesAtStiffnesses]':
        '''List[AssemblyModalAnalysesAtStiffnesses]: 'AssemblyModalAnalysesAtStiffnessesLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysesAtStiffnessesLoadCases, constructor.new(_3703.AssemblyModalAnalysesAtStiffnesses))
        return value

    @property
    def bearings(self) -> 'List[_3828.BearingCompoundModalAnalysesAtStiffnesses]':
        '''List[BearingCompoundModalAnalysesAtStiffnesses]: 'Bearings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bearings, constructor.new(_3828.BearingCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def belt_drives(self) -> 'List[_3830.BeltDriveCompoundModalAnalysesAtStiffnesses]':
        '''List[BeltDriveCompoundModalAnalysesAtStiffnesses]: 'BeltDrives' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BeltDrives, constructor.new(_3830.BeltDriveCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def bevel_differential_gear_sets(self) -> 'List[_3833.BevelDifferentialGearSetCompoundModalAnalysesAtStiffnesses]':
        '''List[BevelDifferentialGearSetCompoundModalAnalysesAtStiffnesses]: 'BevelDifferentialGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BevelDifferentialGearSets, constructor.new(_3833.BevelDifferentialGearSetCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def bolts(self) -> 'List[_3839.BoltCompoundModalAnalysesAtStiffnesses]':
        '''List[BoltCompoundModalAnalysesAtStiffnesses]: 'Bolts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Bolts, constructor.new(_3839.BoltCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def bolted_joints(self) -> 'List[_3840.BoltedJointCompoundModalAnalysesAtStiffnesses]':
        '''List[BoltedJointCompoundModalAnalysesAtStiffnesses]: 'BoltedJoints' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.BoltedJoints, constructor.new(_3840.BoltedJointCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def clutches(self) -> 'List[_3841.ClutchCompoundModalAnalysesAtStiffnesses]':
        '''List[ClutchCompoundModalAnalysesAtStiffnesses]: 'Clutches' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Clutches, constructor.new(_3841.ClutchCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def concept_couplings(self) -> 'List[_3846.ConceptCouplingCompoundModalAnalysesAtStiffnesses]':
        '''List[ConceptCouplingCompoundModalAnalysesAtStiffnesses]: 'ConceptCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptCouplings, constructor.new(_3846.ConceptCouplingCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def concept_gear_sets(self) -> 'List[_3851.ConceptGearSetCompoundModalAnalysesAtStiffnesses]':
        '''List[ConceptGearSetCompoundModalAnalysesAtStiffnesses]: 'ConceptGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearSets, constructor.new(_3851.ConceptGearSetCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def cv_ts(self) -> 'List[_3861.CVTCompoundModalAnalysesAtStiffnesses]':
        '''List[CVTCompoundModalAnalysesAtStiffnesses]: 'CVTs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CVTs, constructor.new(_3861.CVTCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def cylindrical_gear_sets(self) -> 'List[_3865.CylindricalGearSetCompoundModalAnalysesAtStiffnesses]':
        '''List[CylindricalGearSetCompoundModalAnalysesAtStiffnesses]: 'CylindricalGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearSets, constructor.new(_3865.CylindricalGearSetCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def face_gear_sets(self) -> 'List[_3871.FaceGearSetCompoundModalAnalysesAtStiffnesses]':
        '''List[FaceGearSetCompoundModalAnalysesAtStiffnesses]: 'FaceGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FaceGearSets, constructor.new(_3871.FaceGearSetCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def flexible_pin_assemblies(self) -> 'List[_3872.FlexiblePinAssemblyCompoundModalAnalysesAtStiffnesses]':
        '''List[FlexiblePinAssemblyCompoundModalAnalysesAtStiffnesses]: 'FlexiblePinAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.FlexiblePinAssemblies, constructor.new(_3872.FlexiblePinAssemblyCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def hypoid_gear_sets(self) -> 'List[_3879.HypoidGearSetCompoundModalAnalysesAtStiffnesses]':
        '''List[HypoidGearSetCompoundModalAnalysesAtStiffnesses]: 'HypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.HypoidGearSets, constructor.new(_3879.HypoidGearSetCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def imported_fe_components(self) -> 'List[_3880.ImportedFEComponentCompoundModalAnalysesAtStiffnesses]':
        '''List[ImportedFEComponentCompoundModalAnalysesAtStiffnesses]: 'ImportedFEComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ImportedFEComponents, constructor.new(_3880.ImportedFEComponentCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def klingelnberg_cyclo_palloid_hypoid_gear_sets(self) -> 'List[_3887.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysesAtStiffnesses]':
        '''List[KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysesAtStiffnesses]: 'KlingelnbergCycloPalloidHypoidGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidHypoidGearSets, constructor.new(_3887.KlingelnbergCycloPalloidHypoidGearSetCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def klingelnberg_cyclo_palloid_spiral_bevel_gear_sets(self) -> 'List[_3890.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysesAtStiffnesses]':
        '''List[KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysesAtStiffnesses]: 'KlingelnbergCycloPalloidSpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.KlingelnbergCycloPalloidSpiralBevelGearSets, constructor.new(_3890.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def mass_discs(self) -> 'List[_3891.MassDiscCompoundModalAnalysesAtStiffnesses]':
        '''List[MassDiscCompoundModalAnalysesAtStiffnesses]: 'MassDiscs' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MassDiscs, constructor.new(_3891.MassDiscCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def measurement_components(self) -> 'List[_3892.MeasurementComponentCompoundModalAnalysesAtStiffnesses]':
        '''List[MeasurementComponentCompoundModalAnalysesAtStiffnesses]: 'MeasurementComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeasurementComponents, constructor.new(_3892.MeasurementComponentCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def oil_seals(self) -> 'List[_3894.OilSealCompoundModalAnalysesAtStiffnesses]':
        '''List[OilSealCompoundModalAnalysesAtStiffnesses]: 'OilSeals' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.OilSeals, constructor.new(_3894.OilSealCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def part_to_part_shear_couplings(self) -> 'List[_3896.PartToPartShearCouplingCompoundModalAnalysesAtStiffnesses]':
        '''List[PartToPartShearCouplingCompoundModalAnalysesAtStiffnesses]: 'PartToPartShearCouplings' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PartToPartShearCouplings, constructor.new(_3896.PartToPartShearCouplingCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def planet_carriers(self) -> 'List[_3901.PlanetCarrierCompoundModalAnalysesAtStiffnesses]':
        '''List[PlanetCarrierCompoundModalAnalysesAtStiffnesses]: 'PlanetCarriers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PlanetCarriers, constructor.new(_3901.PlanetCarrierCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def point_loads(self) -> 'List[_3902.PointLoadCompoundModalAnalysesAtStiffnesses]':
        '''List[PointLoadCompoundModalAnalysesAtStiffnesses]: 'PointLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PointLoads, constructor.new(_3902.PointLoadCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def power_loads(self) -> 'List[_3903.PowerLoadCompoundModalAnalysesAtStiffnesses]':
        '''List[PowerLoadCompoundModalAnalysesAtStiffnesses]: 'PowerLoads' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.PowerLoads, constructor.new(_3903.PowerLoadCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def shaft_hub_connections(self) -> 'List[_3910.ShaftHubConnectionCompoundModalAnalysesAtStiffnesses]':
        '''List[ShaftHubConnectionCompoundModalAnalysesAtStiffnesses]: 'ShaftHubConnections' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ShaftHubConnections, constructor.new(_3910.ShaftHubConnectionCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def rolling_ring_assemblies(self) -> 'List[_3905.RollingRingAssemblyCompoundModalAnalysesAtStiffnesses]':
        '''List[RollingRingAssemblyCompoundModalAnalysesAtStiffnesses]: 'RollingRingAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RollingRingAssemblies, constructor.new(_3905.RollingRingAssemblyCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def shafts(self) -> 'List[_3909.ShaftCompoundModalAnalysesAtStiffnesses]':
        '''List[ShaftCompoundModalAnalysesAtStiffnesses]: 'Shafts' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Shafts, constructor.new(_3909.ShaftCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def spiral_bevel_gear_sets(self) -> 'List[_3915.SpiralBevelGearSetCompoundModalAnalysesAtStiffnesses]':
        '''List[SpiralBevelGearSetCompoundModalAnalysesAtStiffnesses]: 'SpiralBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpiralBevelGearSets, constructor.new(_3915.SpiralBevelGearSetCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def spring_dampers(self) -> 'List[_3916.SpringDamperCompoundModalAnalysesAtStiffnesses]':
        '''List[SpringDamperCompoundModalAnalysesAtStiffnesses]: 'SpringDampers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.SpringDampers, constructor.new(_3916.SpringDamperCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def straight_bevel_diff_gear_sets(self) -> 'List[_3921.StraightBevelDiffGearSetCompoundModalAnalysesAtStiffnesses]':
        '''List[StraightBevelDiffGearSetCompoundModalAnalysesAtStiffnesses]: 'StraightBevelDiffGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelDiffGearSets, constructor.new(_3921.StraightBevelDiffGearSetCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def straight_bevel_gear_sets(self) -> 'List[_3924.StraightBevelGearSetCompoundModalAnalysesAtStiffnesses]':
        '''List[StraightBevelGearSetCompoundModalAnalysesAtStiffnesses]: 'StraightBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearSets, constructor.new(_3924.StraightBevelGearSetCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def synchronisers(self) -> 'List[_3927.SynchroniserCompoundModalAnalysesAtStiffnesses]':
        '''List[SynchroniserCompoundModalAnalysesAtStiffnesses]: 'Synchronisers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Synchronisers, constructor.new(_3927.SynchroniserCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def torque_converters(self) -> 'List[_3931.TorqueConverterCompoundModalAnalysesAtStiffnesses]':
        '''List[TorqueConverterCompoundModalAnalysesAtStiffnesses]: 'TorqueConverters' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.TorqueConverters, constructor.new(_3931.TorqueConverterCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def unbalanced_masses(self) -> 'List[_3935.UnbalancedMassCompoundModalAnalysesAtStiffnesses]':
        '''List[UnbalancedMassCompoundModalAnalysesAtStiffnesses]: 'UnbalancedMasses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.UnbalancedMasses, constructor.new(_3935.UnbalancedMassCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def worm_gear_sets(self) -> 'List[_3939.WormGearSetCompoundModalAnalysesAtStiffnesses]':
        '''List[WormGearSetCompoundModalAnalysesAtStiffnesses]: 'WormGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearSets, constructor.new(_3939.WormGearSetCompoundModalAnalysesAtStiffnesses))
        return value

    @property
    def zerol_bevel_gear_sets(self) -> 'List[_3942.ZerolBevelGearSetCompoundModalAnalysesAtStiffnesses]':
        '''List[ZerolBevelGearSetCompoundModalAnalysesAtStiffnesses]: 'ZerolBevelGearSets' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearSets, constructor.new(_3942.ZerolBevelGearSetCompoundModalAnalysesAtStiffnesses))
        return value
