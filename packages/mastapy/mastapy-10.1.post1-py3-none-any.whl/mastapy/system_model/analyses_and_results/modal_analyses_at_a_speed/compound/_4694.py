'''_4694.py

WormGearSetCompoundModalAnalysisAtASpeed
'''


from typing import List

from mastapy.system_model.part_model.gears import _2090
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed.compound import _4692, _4693, _4630
from mastapy.system_model.analyses_and_results.modal_analyses_at_a_speed import _4573
from mastapy._internal.python_net import python_net_import

_WORM_GEAR_SET_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtASpeed.Compound', 'WormGearSetCompoundModalAnalysisAtASpeed')


__docformat__ = 'restructuredtext en'
__all__ = ('WormGearSetCompoundModalAnalysisAtASpeed',)


class WormGearSetCompoundModalAnalysisAtASpeed(_4630.GearSetCompoundModalAnalysisAtASpeed):
    '''WormGearSetCompoundModalAnalysisAtASpeed

    This is a mastapy class.
    '''

    TYPE = _WORM_GEAR_SET_COMPOUND_MODAL_ANALYSIS_AT_A_SPEED

    __hash__ = None

    def __init__(self, instance_to_wrap: 'WormGearSetCompoundModalAnalysisAtASpeed.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2090.WormGearSet':
        '''WormGearSet: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2090.WormGearSet)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def assembly_design(self) -> '_2090.WormGearSet':
        '''WormGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2090.WormGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def worm_gears_compound_modal_analysis_at_a_speed(self) -> 'List[_4692.WormGearCompoundModalAnalysisAtASpeed]':
        '''List[WormGearCompoundModalAnalysisAtASpeed]: 'WormGearsCompoundModalAnalysisAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormGearsCompoundModalAnalysisAtASpeed, constructor.new(_4692.WormGearCompoundModalAnalysisAtASpeed))
        return value

    @property
    def worm_meshes_compound_modal_analysis_at_a_speed(self) -> 'List[_4693.WormGearMeshCompoundModalAnalysisAtASpeed]':
        '''List[WormGearMeshCompoundModalAnalysisAtASpeed]: 'WormMeshesCompoundModalAnalysisAtASpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.WormMeshesCompoundModalAnalysisAtASpeed, constructor.new(_4693.WormGearMeshCompoundModalAnalysisAtASpeed))
        return value

    @property
    def load_case_analyses_ready(self) -> 'List[_4573.WormGearSetModalAnalysisAtASpeed]':
        '''List[WormGearSetModalAnalysisAtASpeed]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_4573.WormGearSetModalAnalysisAtASpeed))
        return value

    @property
    def assembly_modal_analysis_at_a_speed_load_cases(self) -> 'List[_4573.WormGearSetModalAnalysisAtASpeed]':
        '''List[WormGearSetModalAnalysisAtASpeed]: 'AssemblyModalAnalysisAtASpeedLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblyModalAnalysisAtASpeedLoadCases, constructor.new(_4573.WormGearSetModalAnalysisAtASpeed))
        return value
