'''_4689.py

BevelDifferentialSunGearModalAnalysis
'''


from mastapy.system_model.part_model.gears import _2034
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.system_deflections import _2197
from mastapy.system_model.analyses_and_results.modal_analyses import _4686
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_SUN_GEAR_MODAL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ModalAnalyses', 'BevelDifferentialSunGearModalAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialSunGearModalAnalysis',)


class BevelDifferentialSunGearModalAnalysis(_4686.BevelDifferentialGearModalAnalysis):
    '''BevelDifferentialSunGearModalAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_SUN_GEAR_MODAL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialSunGearModalAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2034.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2034.BevelDifferentialSunGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def system_deflection_results(self) -> '_2197.BevelDifferentialSunGearSystemDeflection':
        '''BevelDifferentialSunGearSystemDeflection: 'SystemDeflectionResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2197.BevelDifferentialSunGearSystemDeflection)(self.wrapped.SystemDeflectionResults) if self.wrapped.SystemDeflectionResults else None
