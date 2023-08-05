'''_3261.py

DatumPowerFlow
'''


from mastapy.system_model.part_model import _1992
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.static_loads import _6098
from mastapy.system_model.analyses_and_results.power_flows import _3238
from mastapy._internal.python_net import python_net_import

_DATUM_POWER_FLOW = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.PowerFlows', 'DatumPowerFlow')


__docformat__ = 'restructuredtext en'
__all__ = ('DatumPowerFlow',)


class DatumPowerFlow(_3238.ComponentPowerFlow):
    '''DatumPowerFlow

    This is a mastapy class.
    '''

    TYPE = _DATUM_POWER_FLOW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DatumPowerFlow.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_1992.Datum':
        '''Datum: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1992.Datum)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_load_case(self) -> '_6098.DatumLoadCase':
        '''DatumLoadCase: 'ComponentLoadCase' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6098.DatumLoadCase)(self.wrapped.ComponentLoadCase) if self.wrapped.ComponentLoadCase else None
