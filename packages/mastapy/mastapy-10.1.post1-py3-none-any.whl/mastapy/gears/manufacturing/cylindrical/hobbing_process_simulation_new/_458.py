'''_458.py

HobbingProcessSimulationNew
'''


from mastapy.gears.manufacturing.cylindrical.hobbing_process_simulation_new import (
    _453, _455, _456, _452,
    _454, _460, _471, _457
)
from mastapy._internal import constructor
from mastapy._internal.python_net import python_net_import

_HOBBING_PROCESS_SIMULATION_NEW = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical.HobbingProcessSimulationNew', 'HobbingProcessSimulationNew')


__docformat__ = 'restructuredtext en'
__all__ = ('HobbingProcessSimulationNew',)


class HobbingProcessSimulationNew(_471.ProcessSimulationNew['_457.HobbingProcessSimulationInput']):
    '''HobbingProcessSimulationNew

    This is a mastapy class.
    '''

    TYPE = _HOBBING_PROCESS_SIMULATION_NEW

    __hash__ = None

    def __init__(self, instance_to_wrap: 'HobbingProcessSimulationNew.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def hobbing_process_lead_calculation(self) -> '_453.HobbingProcessLeadCalculation':
        '''HobbingProcessLeadCalculation: 'HobbingProcessLeadCalculation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_453.HobbingProcessLeadCalculation)(self.wrapped.HobbingProcessLeadCalculation) if self.wrapped.HobbingProcessLeadCalculation else None

    @property
    def hobbing_process_pitch_calculation(self) -> '_455.HobbingProcessPitchCalculation':
        '''HobbingProcessPitchCalculation: 'HobbingProcessPitchCalculation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_455.HobbingProcessPitchCalculation)(self.wrapped.HobbingProcessPitchCalculation) if self.wrapped.HobbingProcessPitchCalculation else None

    @property
    def hobbing_process_profile_calculation(self) -> '_456.HobbingProcessProfileCalculation':
        '''HobbingProcessProfileCalculation: 'HobbingProcessProfileCalculation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_456.HobbingProcessProfileCalculation)(self.wrapped.HobbingProcessProfileCalculation) if self.wrapped.HobbingProcessProfileCalculation else None

    @property
    def hobbing_process_gear_shape_calculation(self) -> '_452.HobbingProcessGearShape':
        '''HobbingProcessGearShape: 'HobbingProcessGearShapeCalculation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_452.HobbingProcessGearShape)(self.wrapped.HobbingProcessGearShapeCalculation) if self.wrapped.HobbingProcessGearShapeCalculation else None

    @property
    def hobbing_process_mark_on_shaft_calculation(self) -> '_454.HobbingProcessMarkOnShaft':
        '''HobbingProcessMarkOnShaft: 'HobbingProcessMarkOnShaftCalculation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_454.HobbingProcessMarkOnShaft)(self.wrapped.HobbingProcessMarkOnShaftCalculation) if self.wrapped.HobbingProcessMarkOnShaftCalculation else None

    @property
    def hobbing_process_total_modification(self) -> '_460.HobbingProcessTotalModificationCalculation':
        '''HobbingProcessTotalModificationCalculation: 'HobbingProcessTotalModification' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_460.HobbingProcessTotalModificationCalculation)(self.wrapped.HobbingProcessTotalModification) if self.wrapped.HobbingProcessTotalModification else None
