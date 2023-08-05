'''_3825.py

StraightBevelGearSetModalAnalysesAtStiffnesses
'''


from typing import List

from mastapy.system_model.part_model.gears import _2086
from mastapy._internal import constructor, conversion
from mastapy.system_model.analyses_and_results.static_loads import _6189
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3824, _3823, _3736
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_GEAR_SET_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'StraightBevelGearSetModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelGearSetModalAnalysesAtStiffnesses',)


class StraightBevelGearSetModalAnalysesAtStiffnesses(_3736.BevelGearSetModalAnalysesAtStiffnesses):
    '''StraightBevelGearSetModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_GEAR_SET_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelGearSetModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def assembly_design(self) -> '_2086.StraightBevelGearSet':
        '''StraightBevelGearSet: 'AssemblyDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2086.StraightBevelGearSet)(self.wrapped.AssemblyDesign) if self.wrapped.AssemblyDesign else None

    @property
    def assembly_load_case(self) -> '_6189.StraightBevelGearSetLoadCase':
        '''StraightBevelGearSetLoadCase: 'AssemblyLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6189.StraightBevelGearSetLoadCase)(self.wrapped.AssemblyLoadCase) if self.wrapped.AssemblyLoadCase else None

    @property
    def straight_bevel_gears_modal_analyses_at_stiffnesses(self) -> 'List[_3824.StraightBevelGearModalAnalysesAtStiffnesses]':
        '''List[StraightBevelGearModalAnalysesAtStiffnesses]: 'StraightBevelGearsModalAnalysesAtStiffnesses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelGearsModalAnalysesAtStiffnesses, constructor.new(_3824.StraightBevelGearModalAnalysesAtStiffnesses))
        return value

    @property
    def straight_bevel_meshes_modal_analyses_at_stiffnesses(self) -> 'List[_3823.StraightBevelGearMeshModalAnalysesAtStiffnesses]':
        '''List[StraightBevelGearMeshModalAnalysesAtStiffnesses]: 'StraightBevelMeshesModalAnalysesAtStiffnesses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.StraightBevelMeshesModalAnalysesAtStiffnesses, constructor.new(_3823.StraightBevelGearMeshModalAnalysesAtStiffnesses))
        return value
