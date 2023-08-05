'''_3448.py

BeltDriveParametricStudyTool
'''


from typing import List

from mastapy.system_model.part_model.couplings import _2088
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6033
from mastapy.system_model.analyses_and_results.system_deflections import _2192
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3546
from mastapy._internal.python_net import python_net_import

_BELT_DRIVE_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'BeltDriveParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltDriveParametricStudyTool',)


class BeltDriveParametricStudyTool(_3546.SpecialisedAssemblyParametricStudyTool):
    '''BeltDriveParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _BELT_DRIVE_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BeltDriveParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2088.BeltDrive':
        '''BeltDrive: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2088.BeltDrive)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6033.BeltDriveLoadCase':
        '''BeltDriveLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6033.BeltDriveLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def assembly_system_deflection_results(self) -> 'List[_2192.BeltDriveSystemDeflection]':
        '''List[BeltDriveSystemDeflection]: 'AssemblySystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.AssemblySystemDeflectionResults, constructor.new(_2192.BeltDriveSystemDeflection))
        return value
