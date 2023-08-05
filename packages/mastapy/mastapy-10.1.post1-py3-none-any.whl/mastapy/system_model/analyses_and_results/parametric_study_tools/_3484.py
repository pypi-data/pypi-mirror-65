'''_3484.py

CoaxialConnectionParametricStudyTool
'''


from typing import List

from mastapy.system_model.connections_and_sockets import _1832
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6069
from mastapy.system_model.analyses_and_results.system_deflections import _2228
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3567
from mastapy._internal.python_net import python_net_import

_COAXIAL_CONNECTION_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'CoaxialConnectionParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('CoaxialConnectionParametricStudyTool',)


class CoaxialConnectionParametricStudyTool(_3567.ShaftToMountableComponentConnectionParametricStudyTool):
    '''CoaxialConnectionParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _COAXIAL_CONNECTION_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CoaxialConnectionParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1832.CoaxialConnection':
        '''CoaxialConnection: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1832.CoaxialConnection)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6069.CoaxialConnectionLoadCase':
        '''CoaxialConnectionLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6069.CoaxialConnectionLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def connection_system_deflection_results(self) -> 'List[_2228.CoaxialConnectionSystemDeflection]':
        '''List[CoaxialConnectionSystemDeflection]: 'ConnectionSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSystemDeflectionResults, constructor.new(_2228.CoaxialConnectionSystemDeflection))
        return value
