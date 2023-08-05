'''_5282.py

ConceptGearSetGearWhineAnalysis
'''


from typing import List

from mastapy.system_model.part_model.gears import _2060
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6076
from mastapy.system_model.analyses_and_results.system_deflections import _2235
from mastapy.system_model.analyses_and_results.gear_whine_analyses import _5280, _5281, _5320
from mastapy._internal.python_net import python_net_import

_CONCEPT_GEAR_SET_GEAR_WHINE_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'ConceptGearSetGearWhineAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ConceptGearSetGearWhineAnalysis',)


class ConceptGearSetGearWhineAnalysis(_5320.GearSetGearWhineAnalysis):
    '''ConceptGearSetGearWhineAnalysis

    This is a mastapy class.
    '''

    TYPE = _CONCEPT_GEAR_SET_GEAR_WHINE_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ConceptGearSetGearWhineAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2060.ConceptGearSet':
        '''ConceptGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2060.ConceptGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6076.ConceptGearSetLoadCase':
        '''ConceptGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6076.ConceptGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def system_deflection_results(self) -> '_2235.ConceptGearSetSystemDeflection':
        '''ConceptGearSetSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2235.ConceptGearSetSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None

    @property
    def gears_gear_whine_analysis(self) -> 'List[_5280.ConceptGearGearWhineAnalysis]':
        '''List[ConceptGearGearWhineAnalysis]: 'GearsGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearsGearWhineAnalysis, constructor.new(_5280.ConceptGearGearWhineAnalysis))
        return value

    @property
    def concept_gears_gear_whine_analysis(self) -> 'List[_5280.ConceptGearGearWhineAnalysis]':
        '''List[ConceptGearGearWhineAnalysis]: 'ConceptGearsGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptGearsGearWhineAnalysis, constructor.new(_5280.ConceptGearGearWhineAnalysis))
        return value

    @property
    def meshes_gear_whine_analysis(self) -> 'List[_5281.ConceptGearMeshGearWhineAnalysis]':
        '''List[ConceptGearMeshGearWhineAnalysis]: 'MeshesGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshesGearWhineAnalysis, constructor.new(_5281.ConceptGearMeshGearWhineAnalysis))
        return value

    @property
    def concept_meshes_gear_whine_analysis(self) -> 'List[_5281.ConceptGearMeshGearWhineAnalysis]':
        '''List[ConceptGearMeshGearWhineAnalysis]: 'ConceptMeshesGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConceptMeshesGearWhineAnalysis, constructor.new(_5281.ConceptGearMeshGearWhineAnalysis))
        return value
