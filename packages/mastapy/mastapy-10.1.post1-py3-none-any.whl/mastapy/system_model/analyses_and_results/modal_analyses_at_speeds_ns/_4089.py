'''_4089.py

ZerolBevelGearSetModalAnalysesAtSpeeds
'''


from typing import List

from mastapy.system_model.part_model.gears import _2092
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6213
from mastapy.system_model.analyses_and_results.modal_analyses_at_speeds_ns import _4088, _4087, _3981
from mastapy._internal.python_net import python_net_import

_ZEROL_BEVEL_GEAR_SET_MODAL_ANALYSES_AT_SPEEDS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtSpeedsNS', 'ZerolBevelGearSetModalAnalysesAtSpeeds')


__docformat__ = 'restructuredtext en'
__all__ = ('ZerolBevelGearSetModalAnalysesAtSpeeds',)


class ZerolBevelGearSetModalAnalysesAtSpeeds(_3981.BevelGearSetModalAnalysesAtSpeeds):
    '''ZerolBevelGearSetModalAnalysesAtSpeeds

    This is a mastapy class.
    '''

    TYPE = _ZEROL_BEVEL_GEAR_SET_MODAL_ANALYSES_AT_SPEEDS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ZerolBevelGearSetModalAnalysesAtSpeeds.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2092.ZerolBevelGearSet':
        '''ZerolBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2092.ZerolBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6213.ZerolBevelGearSetLoadCase':
        '''ZerolBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6213.ZerolBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def zerol_bevel_gears_modal_analyses_at_speeds(self) -> 'List[_4088.ZerolBevelGearModalAnalysesAtSpeeds]':
        '''List[ZerolBevelGearModalAnalysesAtSpeeds]: 'ZerolBevelGearsModalAnalysesAtSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelGearsModalAnalysesAtSpeeds, constructor.new(_4088.ZerolBevelGearModalAnalysesAtSpeeds))
        return value

    @property
    def zerol_bevel_meshes_modal_analyses_at_speeds(self) -> 'List[_4087.ZerolBevelGearMeshModalAnalysesAtSpeeds]':
        '''List[ZerolBevelGearMeshModalAnalysesAtSpeeds]: 'ZerolBevelMeshesModalAnalysesAtSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.ZerolBevelMeshesModalAnalysesAtSpeeds, constructor.new(_4087.ZerolBevelGearMeshModalAnalysesAtSpeeds))
        return value
