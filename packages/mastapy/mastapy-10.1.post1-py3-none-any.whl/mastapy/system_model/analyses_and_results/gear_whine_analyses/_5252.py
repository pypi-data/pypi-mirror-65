'''_5252.py

AbstractPeriodicExcitationDetail
'''


from mastapy.system_model.analyses_and_results.static_loads import (
    _6125, _6080, _6093, _6102,
    _6103, _6104, _6105, _6121,
    _6163, _6176, _6205
)
from mastapy._internal import constructor
from mastapy._internal.cast_exception import CastException
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_ABSTRACT_PERIODIC_EXCITATION_DETAIL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.GearWhineAnalyses', 'AbstractPeriodicExcitationDetail')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractPeriodicExcitationDetail',)


class AbstractPeriodicExcitationDetail(_0.APIBase):
    '''AbstractPeriodicExcitationDetail

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_PERIODIC_EXCITATION_DETAIL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractPeriodicExcitationDetail.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def harmonic_load_data(self) -> '_6125.HarmonicLoadDataBase':
        '''HarmonicLoadDataBase: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_6125.HarmonicLoadDataBase)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData else None

    @property
    def harmonic_load_data_of_type_conical_gear_set_harmonic_load_data(self) -> '_6080.ConicalGearSetHarmonicLoadData':
        '''ConicalGearSetHarmonicLoadData: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6080.ConicalGearSetHarmonicLoadData.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to ConicalGearSetHarmonicLoadData. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new(_6080.ConicalGearSetHarmonicLoadData)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData else None

    @property
    def harmonic_load_data_of_type_cylindrical_gear_set_harmonic_load_data(self) -> '_6093.CylindricalGearSetHarmonicLoadData':
        '''CylindricalGearSetHarmonicLoadData: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6093.CylindricalGearSetHarmonicLoadData.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to CylindricalGearSetHarmonicLoadData. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new(_6093.CylindricalGearSetHarmonicLoadData)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData else None

    @property
    def harmonic_load_data_of_type_electric_machine_harmonic_load_data(self) -> '_6102.ElectricMachineHarmonicLoadData':
        '''ElectricMachineHarmonicLoadData: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6102.ElectricMachineHarmonicLoadData.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to ElectricMachineHarmonicLoadData. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new(_6102.ElectricMachineHarmonicLoadData)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData else None

    @property
    def harmonic_load_data_of_type_electric_machine_harmonic_load_data_from_excel(self) -> '_6103.ElectricMachineHarmonicLoadDataFromExcel':
        '''ElectricMachineHarmonicLoadDataFromExcel: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6103.ElectricMachineHarmonicLoadDataFromExcel.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to ElectricMachineHarmonicLoadDataFromExcel. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new(_6103.ElectricMachineHarmonicLoadDataFromExcel)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData else None

    @property
    def harmonic_load_data_of_type_electric_machine_harmonic_load_data_from_jmag(self) -> '_6104.ElectricMachineHarmonicLoadDataFromJMAG':
        '''ElectricMachineHarmonicLoadDataFromJMAG: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6104.ElectricMachineHarmonicLoadDataFromJMAG.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to ElectricMachineHarmonicLoadDataFromJMAG. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new(_6104.ElectricMachineHarmonicLoadDataFromJMAG)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData else None

    @property
    def harmonic_load_data_of_type_electric_machine_harmonic_load_data_from_motor_cad(self) -> '_6105.ElectricMachineHarmonicLoadDataFromMotorCAD':
        '''ElectricMachineHarmonicLoadDataFromMotorCAD: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6105.ElectricMachineHarmonicLoadDataFromMotorCAD.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to ElectricMachineHarmonicLoadDataFromMotorCAD. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new(_6105.ElectricMachineHarmonicLoadDataFromMotorCAD)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData else None

    @property
    def harmonic_load_data_of_type_gear_set_harmonic_load_data(self) -> '_6121.GearSetHarmonicLoadData':
        '''GearSetHarmonicLoadData: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6121.GearSetHarmonicLoadData.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to GearSetHarmonicLoadData. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new(_6121.GearSetHarmonicLoadData)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData else None

    @property
    def harmonic_load_data_of_type_point_load_harmonic_load_data(self) -> '_6163.PointLoadHarmonicLoadData':
        '''PointLoadHarmonicLoadData: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6163.PointLoadHarmonicLoadData.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to PointLoadHarmonicLoadData. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new(_6163.PointLoadHarmonicLoadData)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData else None

    @property
    def harmonic_load_data_of_type_speed_dependent_harmonic_load_data(self) -> '_6176.SpeedDependentHarmonicLoadData':
        '''SpeedDependentHarmonicLoadData: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6176.SpeedDependentHarmonicLoadData.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to SpeedDependentHarmonicLoadData. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new(_6176.SpeedDependentHarmonicLoadData)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData else None

    @property
    def harmonic_load_data_of_type_unbalanced_mass_harmonic_load_data(self) -> '_6205.UnbalancedMassHarmonicLoadData':
        '''UnbalancedMassHarmonicLoadData: 'HarmonicLoadData' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _6205.UnbalancedMassHarmonicLoadData.TYPE not in self.wrapped.HarmonicLoadData.__class__.__mro__:
            raise CastException('Failed to cast harmonic_load_data to UnbalancedMassHarmonicLoadData. Expected: {}.'.format(self.wrapped.HarmonicLoadData.__class__.__qualname__))

        return constructor.new(_6205.UnbalancedMassHarmonicLoadData)(self.wrapped.HarmonicLoadData) if self.wrapped.HarmonicLoadData else None
