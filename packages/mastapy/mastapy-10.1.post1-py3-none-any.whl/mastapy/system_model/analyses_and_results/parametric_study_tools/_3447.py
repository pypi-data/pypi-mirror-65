'''_3447.py

BeltConnectionParametricStudyTool
'''


from typing import List

from mastapy.system_model.connections_and_sockets import _1810
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6032
from mastapy.system_model.analyses_and_results.system_deflections import _2191
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3505
from mastapy._internal.python_net import python_net_import

_BELT_CONNECTION_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'BeltConnectionParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('BeltConnectionParametricStudyTool',)


class BeltConnectionParametricStudyTool(_3505.InterMountableComponentConnectionParametricStudyTool):
    '''BeltConnectionParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _BELT_CONNECTION_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BeltConnectionParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1810.BeltConnection':
        '''BeltConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1810.BeltConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6032.BeltConnectionLoadCase':
        '''BeltConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6032.BeltConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def connection_system_deflection_results(self) -> 'List[_2191.BeltConnectionSystemDeflection]':
        '''List[BeltConnectionSystemDeflection]: 'ConnectionSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSystemDeflectionResults, constructor.new(_2191.BeltConnectionSystemDeflection))
        return value
