'''_5705.py

CylindricalGearCompoundGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2063
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5294
from mastapy.system_model.analyses_and_results.gear_whine_analyses.compound import _5715
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_COMPOUND_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses.Compound', 'CylindricalGearCompoundGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearCompoundGearWhineAnalysis',)


class CylindricalGearCompoundGearWhineAnalysis(_5715.GearCompoundGearWhineAnalysis):
    '''CylindricalGearCompoundGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_COMPOUND_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearCompoundGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2063.CylindricalGear':
        '''CylindricalGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2063.CylindricalGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def load_case_analyses_ready(self) -> 'List[_5294.CylindricalGearGearWhineAnalysis]':
        '''List[CylindricalGearGearWhineAnalysis]: 'LoadCaseAnalysesReady' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseAnalysesReady, constructor.new(_5294.CylindricalGearGearWhineAnalysis))
        return value

    @property
    def component_gear_whine_analysis_load_cases(self) -> 'List[_5294.CylindricalGearGearWhineAnalysis]':
        '''List[CylindricalGearGearWhineAnalysis]: 'ComponentGearWhineAnalysisLoadCases' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ComponentGearWhineAnalysisLoadCases, constructor.new(_5294.CylindricalGearGearWhineAnalysis))
        return value

    @property
    def planetaries(self) -> 'List[CylindricalGearCompoundGearWhineAnalysis]':
        '''List[CylindricalGearCompoundGearWhineAnalysis]: 'Planetaries' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Planetaries, constructor.new(CylindricalGearCompoundGearWhineAnalysis))
        return value
