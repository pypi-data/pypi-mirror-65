'''_3259.py

CylindricalGearSetPowerFlow
'''


from typing import List

from mastapy.system_model.part_model.gears import _2064
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6094
from mastapy.gears.rating.cylindrical import _265
from mastapy.system_model.analyses_and_results.power_flows import _3258, _3257, _3269
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_SET_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'CylindricalGearSetPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearSetPowerFlow',)


class CylindricalGearSetPowerFlow(_3269.GearSetPowerFlow):
    '''CylindricalGearSetPowerFlow

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_SET_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearSetPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2064.CylindricalGearSet':
        '''CylindricalGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2064.CylindricalGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6094.CylindricalGearSetLoadCase':
        '''CylindricalGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6094.CylindricalGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def rating(self) -> '_265.CylindricalGearSetRating':
        '''CylindricalGearSetRating: 'Rating' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_265.CylindricalGearSetRating)(self.wrapped.Rating) if self.wrapped.Rating else None

    @property
    def component_detailed_analysis(self) -> '_265.CylindricalGearSetRating':
        '''CylindricalGearSetRating: 'ComponentDetailedAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_265.CylindricalGearSetRating)(self.wrapped.ComponentDetailedAnalysis) if self.wrapped.ComponentDetailedAnalysis else None

    @property
    def gears_power_flow(self) -> 'List[_3258.CylindricalGearPowerFlow]':
        '''List[CylindricalGearPowerFlow]: 'GearsPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.GearsPowerFlow, constructor.new(_3258.CylindricalGearPowerFlow))
        return value

    @property
    def cylindrical_gears_power_flow(self) -> 'List[_3258.CylindricalGearPowerFlow]':
        '''List[CylindricalGearPowerFlow]: 'CylindricalGearsPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalGearsPowerFlow, constructor.new(_3258.CylindricalGearPowerFlow))
        return value

    @property
    def meshes_power_flow(self) -> 'List[_3257.CylindricalGearMeshPowerFlow]':
        '''List[CylindricalGearMeshPowerFlow]: 'MeshesPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.MeshesPowerFlow, constructor.new(_3257.CylindricalGearMeshPowerFlow))
        return value

    @property
    def cylindrical_meshes_power_flow(self) -> 'List[_3257.CylindricalGearMeshPowerFlow]':
        '''List[CylindricalGearMeshPowerFlow]: 'CylindricalMeshesPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.CylindricalMeshesPowerFlow, constructor.new(_3257.CylindricalGearMeshPowerFlow))
        return value

    @property
    def ratings_for_all_designs(self) -> 'List[_265.CylindricalGearSetRating]':
        '''List[CylindricalGearSetRating]: 'RatingsForAllDesigns' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RatingsForAllDesigns, constructor.new(_265.CylindricalGearSetRating))
        return value
