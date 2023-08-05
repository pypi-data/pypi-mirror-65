'''_2205.py

AbstractShaftOrHousingSystemDeflection
'''


from mastapy._internal import constructor
from mastapy.system_model.part_model import _1979, _1998
from mastapy._internal.cast_exception import CastException
from mastapy.system_model.part_model.shaft_model import _2019
from mastapy.system_model.analyses_and_results.power_flows import _3214, _3272, _3304
from mastapy.system_model.analyses_and_results.system_deflections import _2227
from mastapy._internal.python_net import python_net_import

_ABSTRACT_SHAFT_OR_HOUSING_SYSTEM_DEFLECTION = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.SystemDeflections', 'AbstractShaftOrHousingSystemDeflection')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractShaftOrHousingSystemDeflection',)


class AbstractShaftOrHousingSystemDeflection(_2227.ComponentSystemDeflection):
    '''AbstractShaftOrHousingSystemDeflection

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_SHAFT_OR_HOUSING_SYSTEM_DEFLECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractShaftOrHousingSystemDeflection.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def mass_including_connected_components(self) -> 'float':
        '''float: 'MassIncludingConnectedComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MassIncludingConnectedComponents

    @property
    def polar_inertia_including_connected_components(self) -> 'float':
        '''float: 'PolarInertiaIncludingConnectedComponents' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PolarInertiaIncludingConnectedComponents

    @property
    def component_design(self) -> '_1979.AbstractShaftOrHousing':
        '''AbstractShaftOrHousing: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1979.AbstractShaftOrHousing)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_imported_fe_component(self) -> '_1998.ImportedFEComponent':
        '''ImportedFEComponent: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1998.ImportedFEComponent.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to ImportedFEComponent. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_1998.ImportedFEComponent)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def component_design_of_type_shaft(self) -> '_2019.Shaft':
        '''Shaft: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _2019.Shaft.TYPE not in self.wrapped.ComponentDesign.__class__.__mro__:
            raise CastException('Failed to cast component_design to Shaft. Expected: {}.'.format(self.wrapped.ComponentDesign.__class__.__qualname__))

        return constructor.new(_2019.Shaft)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None

    @property
    def power_flow_results(self) -> '_3214.AbstractShaftOrHousingPowerFlow':
        '''AbstractShaftOrHousingPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3214.AbstractShaftOrHousingPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_imported_fe_component_power_flow(self) -> '_3272.ImportedFEComponentPowerFlow':
        '''ImportedFEComponentPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3272.ImportedFEComponentPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to ImportedFEComponentPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new(_3272.ImportedFEComponentPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None

    @property
    def power_flow_results_of_type_shaft_power_flow(self) -> '_3304.ShaftPowerFlow':
        '''ShaftPowerFlow: 'PowerFlowResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _3304.ShaftPowerFlow.TYPE not in self.wrapped.PowerFlowResults.__class__.__mro__:
            raise CastException('Failed to cast power_flow_results to ShaftPowerFlow. Expected: {}.'.format(self.wrapped.PowerFlowResults.__class__.__qualname__))

        return constructor.new(_3304.ShaftPowerFlow)(self.wrapped.PowerFlowResults) if self.wrapped.PowerFlowResults else None
