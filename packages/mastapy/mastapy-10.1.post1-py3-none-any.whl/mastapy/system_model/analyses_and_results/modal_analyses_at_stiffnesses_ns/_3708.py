'''_3708.py

BevelDifferentialGearModalAnalysesAtStiffnesses
'''


from mastapy.system_model.part_model.gears import _2031
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6034
from mastapy.system_model.analyses_and_results.modal_analyses_at_stiffnesses_ns import _3713
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_GEAR_MODAL_ANALYSES_AT_STIFFNESSES = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalysesAtStiffnessesNS', 'BevelDifferentialGearModalAnalysesAtStiffnesses')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialGearModalAnalysesAtStiffnesses',)


class BevelDifferentialGearModalAnalysesAtStiffnesses(_3713.BevelGearModalAnalysesAtStiffnesses):
    '''BevelDifferentialGearModalAnalysesAtStiffnesses

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_GEAR_MODAL_ANALYSES_AT_STIFFNESSES

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialGearModalAnalysesAtStiffnesses.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2031.BevelDifferentialGear':
        '''BevelDifferentialGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2031.BevelDifferentialGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6034.BevelDifferentialGearLoadCase':
        '''BevelDifferentialGearLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6034.BevelDifferentialGearLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
