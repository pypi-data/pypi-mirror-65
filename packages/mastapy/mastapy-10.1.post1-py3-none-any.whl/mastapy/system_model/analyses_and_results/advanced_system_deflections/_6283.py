'''_6283.py

FaceGearMeshAdvancedSystemDeflection
'''


from typing import List

from mastapy.system_model.connections_and_sockets.gears import _1871
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6113
from mastapy.gears.rating.face import _250
from mastapy.system_model.analyses_and_results.system_deflections import _2262
from mastapy.system_model.analyses_and_results.advanced_system_deflections import _6287
from mastapy._internal.python_net import python_net_import

_FACE_GEAR_MESH_ADVANCED_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.AdvancedSystemDeflections', 'FaceGearMeshAdvancedSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('FaceGearMeshAdvancedSystemDeflection',)


class FaceGearMeshAdvancedSystemDeflection(_6287.GearMeshAdvancedSystemDeflection):
    '''FaceGearMeshAdvancedSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _FACE_GEAR_MESH_ADVANCED_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'FaceGearMeshAdvancedSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def connection_design(self) -> '_1871.FaceGearMesh':
        '''FaceGearMesh: 'ConnectionDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1871.FaceGearMesh)(self.wrapped.ConnectionDesign) if self.wrapped.ConnectionDesign else None

    @property
    def connection_load_case(self) -> '_6113.FaceGearMeshLoadCase':
        '''FaceGearMeshLoadCase: 'ConnectionLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6113.FaceGearMeshLoadCase)(self.wrapped.ConnectionLoadCase) if self.wrapped.ConnectionLoadCase else None

    @property
    def component_detailed_analysis(self) -> '_250.FaceGearMeshRating':
        '''FaceGearMeshRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_250.FaceGearMeshRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def connection_system_deflection_results(self) -> 'List[_2262.FaceGearMeshSystemDeflection]':
        '''List[FaceGearMeshSystemDeflection]: 'ConnectionSystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ConnectionSystemDeflectionResults, constructor.new(_2262.FaceGearMeshSystemDeflection))
        return value
