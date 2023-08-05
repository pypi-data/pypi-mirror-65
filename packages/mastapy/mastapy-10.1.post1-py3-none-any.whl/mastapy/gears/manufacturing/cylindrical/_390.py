'''_390.py

CylindricalGearManufacturingConfig
'''


from typing import Callable

from mastapy._internal.implicit import enum_with_selected_value, overridable
from mastapy.gears.manufacturing.cylindrical import _402, _401, _389
from mastapy._internal import enum_with_selected_value_runtime, conversion, constructor
from mastapy._internal.python_net import python_net_import
from mastapy.gears.manufacturing.cylindrical.cutters import (
    _508, _502, _503, _504,
    _505, _507, _509, _510,
    _513
)
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.cylindrical import _790, _766
from mastapy.gears.manufacturing.cylindrical.cutter_simulation import (
    _489, _486, _493, _483
)
from mastapy.gears.manufacturing.cylindrical.process_simulation import _417, _418, _419
from mastapy.gears.analysis import _942

_DATABASE_WITH_SELECTED_ITEM = python_net_import('SMT.MastaAPI.UtilityGUI.Databases', 'DatabaseWithSelectedItem')
_CYLINDRICAL_GEAR_MANUFACTURING_CONFIG = python_net_import('SMT.MastaAPI.Gears.Manufacturing.Cylindrical', 'CylindricalGearManufacturingConfig')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearManufacturingConfig',)


class CylindricalGearManufacturingConfig(_942.GearImplementationDetail):
    '''CylindricalGearManufacturingConfig

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_MANUFACTURING_CONFIG

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearManufacturingConfig.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def roughing_method(self) -> 'enum_with_selected_value.EnumWithSelectedValue_CylindricalMftRoughingMethods':
        '''enum_with_selected_value.EnumWithSelectedValue_CylindricalMftRoughingMethods: 'RoughingMethod' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_CylindricalMftRoughingMethods.implicit_type()
        return enum_with_selected_value_runtime.create(self.wrapped.RoughingMethod, value) if self.wrapped.RoughingMethod else None

    @roughing_method.setter
    def roughing_method(self, value: 'enum_with_selected_value.EnumWithSelectedValue_CylindricalMftRoughingMethods.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_CylindricalMftRoughingMethods.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.RoughingMethod = value

    @property
    def finishing_method(self) -> 'enum_with_selected_value.EnumWithSelectedValue_CylindricalMftFinishingMethods':
        '''enum_with_selected_value.EnumWithSelectedValue_CylindricalMftFinishingMethods: 'FinishingMethod' is the original name of this property.'''

        value = enum_with_selected_value.EnumWithSelectedValue_CylindricalMftFinishingMethods.implicit_type()
        return enum_with_selected_value_runtime.create(self.wrapped.FinishingMethod, value) if self.wrapped.FinishingMethod else None

    @finishing_method.setter
    def finishing_method(self, value: 'enum_with_selected_value.EnumWithSelectedValue_CylindricalMftFinishingMethods.implicit_type()'):
        wrapper_type = enum_with_selected_value_runtime.ENUM_WITH_SELECTED_VALUE
        enclosed_type = enum_with_selected_value.EnumWithSelectedValue_CylindricalMftFinishingMethods.implicit_type()
        value = conversion.mp_to_pn_enum(value)
        value = wrapper_type[enclosed_type](value if value else None)
        self.wrapped.FinishingMethod = value

    @property
    def rough_cutter_database_selector(self) -> 'str':
        '''str: 'RoughCutterDatabaseSelector' is the original name of this property.'''

        return self.wrapped.RoughCutterDatabaseSelector.SelectedItemName

    @rough_cutter_database_selector.setter
    def rough_cutter_database_selector(self, value: 'str'):
        self.wrapped.RoughCutterDatabaseSelector.SetSelectedItem(str(value) if value else None)

    @property
    def finish_cutter_database_selector(self) -> 'str':
        '''str: 'FinishCutterDatabaseSelector' is the original name of this property.'''

        return self.wrapped.FinishCutterDatabaseSelector.SelectedItemName

    @finish_cutter_database_selector.setter
    def finish_cutter_database_selector(self, value: 'str'):
        self.wrapped.FinishCutterDatabaseSelector.SetSelectedItem(str(value) if value else None)

    @property
    def create_new_rough_cutter_compatible_with_gear_in_design_mode(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'CreateNewRoughCutterCompatibleWithGearInDesignMode' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CreateNewRoughCutterCompatibleWithGearInDesignMode

    @property
    def create_new_finish_cutter_compatible_with_gear_in_design_mode(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'CreateNewFinishCutterCompatibleWithGearInDesignMode' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.CreateNewFinishCutterCompatibleWithGearInDesignMode

    @property
    def minimum_finish_cutter_gear_root_clearance_factor(self) -> 'float':
        '''float: 'MinimumFinishCutterGearRootClearanceFactor' is the original name of this property.'''

        return self.wrapped.MinimumFinishCutterGearRootClearanceFactor

    @minimum_finish_cutter_gear_root_clearance_factor.setter
    def minimum_finish_cutter_gear_root_clearance_factor(self, value: 'float'):
        self.wrapped.MinimumFinishCutterGearRootClearanceFactor = float(value) if value else 0.0

    @property
    def number_of_points_for_reporting_main_profile_finish_stock(self) -> 'overridable.Overridable_int':
        '''overridable.Overridable_int: 'NumberOfPointsForReportingMainProfileFinishStock' is the original name of this property.'''

        return constructor.new(overridable.Overridable_int)(self.wrapped.NumberOfPointsForReportingMainProfileFinishStock) if self.wrapped.NumberOfPointsForReportingMainProfileFinishStock else None

    @number_of_points_for_reporting_main_profile_finish_stock.setter
    def number_of_points_for_reporting_main_profile_finish_stock(self, value: 'overridable.Overridable_int.implicit_type()'):
        wrapper_type = overridable.Overridable_int.wrapper_type()
        enclosed_type = overridable.Overridable_int.implicit_type()
        value = wrapper_type[enclosed_type](enclosed_type(value) if value else 0)
        self.wrapped.NumberOfPointsForReportingMainProfileFinishStock = value

    @property
    def rough_cutter(self) -> '_508.CylindricalGearRealCutterDesign':
        '''CylindricalGearRealCutterDesign: 'RoughCutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_508.CylindricalGearRealCutterDesign)(self.wrapped.RoughCutter) if self.wrapped.RoughCutter else None

    @property
    def rough_cutter_of_type_cylindrical_gear_form_grinding_wheel(self) -> '_502.CylindricalGearFormGrindingWheel':
        '''CylindricalGearFormGrindingWheel: 'RoughCutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _502.CylindricalGearFormGrindingWheel.TYPE not in self.wrapped.RoughCutter.__class__.__mro__:
            raise CastException('Failed to cast rough_cutter to CylindricalGearFormGrindingWheel. Expected: {}.'.format(self.wrapped.RoughCutter.__class__.__qualname__))

        return constructor.new(_502.CylindricalGearFormGrindingWheel)(self.wrapped.RoughCutter) if self.wrapped.RoughCutter else None

    @property
    def rough_cutter_of_type_cylindrical_gear_grinding_worm(self) -> '_503.CylindricalGearGrindingWorm':
        '''CylindricalGearGrindingWorm: 'RoughCutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _503.CylindricalGearGrindingWorm.TYPE not in self.wrapped.RoughCutter.__class__.__mro__:
            raise CastException('Failed to cast rough_cutter to CylindricalGearGrindingWorm. Expected: {}.'.format(self.wrapped.RoughCutter.__class__.__qualname__))

        return constructor.new(_503.CylindricalGearGrindingWorm)(self.wrapped.RoughCutter) if self.wrapped.RoughCutter else None

    @property
    def rough_cutter_of_type_cylindrical_gear_hob_design(self) -> '_504.CylindricalGearHobDesign':
        '''CylindricalGearHobDesign: 'RoughCutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _504.CylindricalGearHobDesign.TYPE not in self.wrapped.RoughCutter.__class__.__mro__:
            raise CastException('Failed to cast rough_cutter to CylindricalGearHobDesign. Expected: {}.'.format(self.wrapped.RoughCutter.__class__.__qualname__))

        return constructor.new(_504.CylindricalGearHobDesign)(self.wrapped.RoughCutter) if self.wrapped.RoughCutter else None

    @property
    def rough_cutter_of_type_cylindrical_gear_plunge_shaver(self) -> '_505.CylindricalGearPlungeShaver':
        '''CylindricalGearPlungeShaver: 'RoughCutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _505.CylindricalGearPlungeShaver.TYPE not in self.wrapped.RoughCutter.__class__.__mro__:
            raise CastException('Failed to cast rough_cutter to CylindricalGearPlungeShaver. Expected: {}.'.format(self.wrapped.RoughCutter.__class__.__qualname__))

        return constructor.new(_505.CylindricalGearPlungeShaver)(self.wrapped.RoughCutter) if self.wrapped.RoughCutter else None

    @property
    def rough_cutter_of_type_cylindrical_gear_rack_design(self) -> '_507.CylindricalGearRackDesign':
        '''CylindricalGearRackDesign: 'RoughCutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _507.CylindricalGearRackDesign.TYPE not in self.wrapped.RoughCutter.__class__.__mro__:
            raise CastException('Failed to cast rough_cutter to CylindricalGearRackDesign. Expected: {}.'.format(self.wrapped.RoughCutter.__class__.__qualname__))

        return constructor.new(_507.CylindricalGearRackDesign)(self.wrapped.RoughCutter) if self.wrapped.RoughCutter else None

    @property
    def rough_cutter_of_type_cylindrical_gear_shaper(self) -> '_509.CylindricalGearShaper':
        '''CylindricalGearShaper: 'RoughCutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _509.CylindricalGearShaper.TYPE not in self.wrapped.RoughCutter.__class__.__mro__:
            raise CastException('Failed to cast rough_cutter to CylindricalGearShaper. Expected: {}.'.format(self.wrapped.RoughCutter.__class__.__qualname__))

        return constructor.new(_509.CylindricalGearShaper)(self.wrapped.RoughCutter) if self.wrapped.RoughCutter else None

    @property
    def rough_cutter_of_type_cylindrical_gear_shaver(self) -> '_510.CylindricalGearShaver':
        '''CylindricalGearShaver: 'RoughCutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _510.CylindricalGearShaver.TYPE not in self.wrapped.RoughCutter.__class__.__mro__:
            raise CastException('Failed to cast rough_cutter to CylindricalGearShaver. Expected: {}.'.format(self.wrapped.RoughCutter.__class__.__qualname__))

        return constructor.new(_510.CylindricalGearShaver)(self.wrapped.RoughCutter) if self.wrapped.RoughCutter else None

    @property
    def rough_cutter_of_type_involute_cutter_design(self) -> '_513.InvoluteCutterDesign':
        '''InvoluteCutterDesign: 'RoughCutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _513.InvoluteCutterDesign.TYPE not in self.wrapped.RoughCutter.__class__.__mro__:
            raise CastException('Failed to cast rough_cutter to InvoluteCutterDesign. Expected: {}.'.format(self.wrapped.RoughCutter.__class__.__qualname__))

        return constructor.new(_513.InvoluteCutterDesign)(self.wrapped.RoughCutter) if self.wrapped.RoughCutter else None

    @property
    def finish_cutter(self) -> '_508.CylindricalGearRealCutterDesign':
        '''CylindricalGearRealCutterDesign: 'FinishCutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_508.CylindricalGearRealCutterDesign)(self.wrapped.FinishCutter) if self.wrapped.FinishCutter else None

    @property
    def finish_cutter_of_type_cylindrical_gear_form_grinding_wheel(self) -> '_502.CylindricalGearFormGrindingWheel':
        '''CylindricalGearFormGrindingWheel: 'FinishCutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _502.CylindricalGearFormGrindingWheel.TYPE not in self.wrapped.FinishCutter.__class__.__mro__:
            raise CastException('Failed to cast finish_cutter to CylindricalGearFormGrindingWheel. Expected: {}.'.format(self.wrapped.FinishCutter.__class__.__qualname__))

        return constructor.new(_502.CylindricalGearFormGrindingWheel)(self.wrapped.FinishCutter) if self.wrapped.FinishCutter else None

    @property
    def finish_cutter_of_type_cylindrical_gear_grinding_worm(self) -> '_503.CylindricalGearGrindingWorm':
        '''CylindricalGearGrindingWorm: 'FinishCutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _503.CylindricalGearGrindingWorm.TYPE not in self.wrapped.FinishCutter.__class__.__mro__:
            raise CastException('Failed to cast finish_cutter to CylindricalGearGrindingWorm. Expected: {}.'.format(self.wrapped.FinishCutter.__class__.__qualname__))

        return constructor.new(_503.CylindricalGearGrindingWorm)(self.wrapped.FinishCutter) if self.wrapped.FinishCutter else None

    @property
    def finish_cutter_of_type_cylindrical_gear_hob_design(self) -> '_504.CylindricalGearHobDesign':
        '''CylindricalGearHobDesign: 'FinishCutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _504.CylindricalGearHobDesign.TYPE not in self.wrapped.FinishCutter.__class__.__mro__:
            raise CastException('Failed to cast finish_cutter to CylindricalGearHobDesign. Expected: {}.'.format(self.wrapped.FinishCutter.__class__.__qualname__))

        return constructor.new(_504.CylindricalGearHobDesign)(self.wrapped.FinishCutter) if self.wrapped.FinishCutter else None

    @property
    def finish_cutter_of_type_cylindrical_gear_plunge_shaver(self) -> '_505.CylindricalGearPlungeShaver':
        '''CylindricalGearPlungeShaver: 'FinishCutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _505.CylindricalGearPlungeShaver.TYPE not in self.wrapped.FinishCutter.__class__.__mro__:
            raise CastException('Failed to cast finish_cutter to CylindricalGearPlungeShaver. Expected: {}.'.format(self.wrapped.FinishCutter.__class__.__qualname__))

        return constructor.new(_505.CylindricalGearPlungeShaver)(self.wrapped.FinishCutter) if self.wrapped.FinishCutter else None

    @property
    def finish_cutter_of_type_cylindrical_gear_rack_design(self) -> '_507.CylindricalGearRackDesign':
        '''CylindricalGearRackDesign: 'FinishCutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _507.CylindricalGearRackDesign.TYPE not in self.wrapped.FinishCutter.__class__.__mro__:
            raise CastException('Failed to cast finish_cutter to CylindricalGearRackDesign. Expected: {}.'.format(self.wrapped.FinishCutter.__class__.__qualname__))

        return constructor.new(_507.CylindricalGearRackDesign)(self.wrapped.FinishCutter) if self.wrapped.FinishCutter else None

    @property
    def finish_cutter_of_type_cylindrical_gear_shaper(self) -> '_509.CylindricalGearShaper':
        '''CylindricalGearShaper: 'FinishCutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _509.CylindricalGearShaper.TYPE not in self.wrapped.FinishCutter.__class__.__mro__:
            raise CastException('Failed to cast finish_cutter to CylindricalGearShaper. Expected: {}.'.format(self.wrapped.FinishCutter.__class__.__qualname__))

        return constructor.new(_509.CylindricalGearShaper)(self.wrapped.FinishCutter) if self.wrapped.FinishCutter else None

    @property
    def finish_cutter_of_type_cylindrical_gear_shaver(self) -> '_510.CylindricalGearShaver':
        '''CylindricalGearShaver: 'FinishCutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _510.CylindricalGearShaver.TYPE not in self.wrapped.FinishCutter.__class__.__mro__:
            raise CastException('Failed to cast finish_cutter to CylindricalGearShaver. Expected: {}.'.format(self.wrapped.FinishCutter.__class__.__qualname__))

        return constructor.new(_510.CylindricalGearShaver)(self.wrapped.FinishCutter) if self.wrapped.FinishCutter else None

    @property
    def finish_cutter_of_type_involute_cutter_design(self) -> '_513.InvoluteCutterDesign':
        '''InvoluteCutterDesign: 'FinishCutter' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _513.InvoluteCutterDesign.TYPE not in self.wrapped.FinishCutter.__class__.__mro__:
            raise CastException('Failed to cast finish_cutter to InvoluteCutterDesign. Expected: {}.'.format(self.wrapped.FinishCutter.__class__.__qualname__))

        return constructor.new(_513.InvoluteCutterDesign)(self.wrapped.FinishCutter) if self.wrapped.FinishCutter else None

    @property
    def finish_stock_specification(self) -> '_790.FinishStockSpecification':
        '''FinishStockSpecification: 'FinishStockSpecification' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_790.FinishStockSpecification)(self.wrapped.FinishStockSpecification) if self.wrapped.FinishStockSpecification else None

    @property
    def rough_cutter_simulation(self) -> '_489.GearCutterSimulation':
        '''GearCutterSimulation: 'RoughCutterSimulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_489.GearCutterSimulation)(self.wrapped.RoughCutterSimulation) if self.wrapped.RoughCutterSimulation else None

    @property
    def rough_cutter_simulation_of_type_finish_cutter_simulation(self) -> '_486.FinishCutterSimulation':
        '''FinishCutterSimulation: 'RoughCutterSimulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _486.FinishCutterSimulation.TYPE not in self.wrapped.RoughCutterSimulation.__class__.__mro__:
            raise CastException('Failed to cast rough_cutter_simulation to FinishCutterSimulation. Expected: {}.'.format(self.wrapped.RoughCutterSimulation.__class__.__qualname__))

        return constructor.new(_486.FinishCutterSimulation)(self.wrapped.RoughCutterSimulation) if self.wrapped.RoughCutterSimulation else None

    @property
    def rough_cutter_simulation_of_type_rough_cutter_simulation(self) -> '_493.RoughCutterSimulation':
        '''RoughCutterSimulation: 'RoughCutterSimulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _493.RoughCutterSimulation.TYPE not in self.wrapped.RoughCutterSimulation.__class__.__mro__:
            raise CastException('Failed to cast rough_cutter_simulation to RoughCutterSimulation. Expected: {}.'.format(self.wrapped.RoughCutterSimulation.__class__.__qualname__))

        return constructor.new(_493.RoughCutterSimulation)(self.wrapped.RoughCutterSimulation) if self.wrapped.RoughCutterSimulation else None

    @property
    def rough_process_simulation(self) -> '_417.CutterProcessSimulation':
        '''CutterProcessSimulation: 'RoughProcessSimulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_417.CutterProcessSimulation)(self.wrapped.RoughProcessSimulation) if self.wrapped.RoughProcessSimulation else None

    @property
    def rough_process_simulation_of_type_form_wheel_grinding_process_simulation(self) -> '_418.FormWheelGrindingProcessSimulation':
        '''FormWheelGrindingProcessSimulation: 'RoughProcessSimulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _418.FormWheelGrindingProcessSimulation.TYPE not in self.wrapped.RoughProcessSimulation.__class__.__mro__:
            raise CastException('Failed to cast rough_process_simulation to FormWheelGrindingProcessSimulation. Expected: {}.'.format(self.wrapped.RoughProcessSimulation.__class__.__qualname__))

        return constructor.new(_418.FormWheelGrindingProcessSimulation)(self.wrapped.RoughProcessSimulation) if self.wrapped.RoughProcessSimulation else None

    @property
    def rough_process_simulation_of_type_shaping_process_simulation(self) -> '_419.ShapingProcessSimulation':
        '''ShapingProcessSimulation: 'RoughProcessSimulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _419.ShapingProcessSimulation.TYPE not in self.wrapped.RoughProcessSimulation.__class__.__mro__:
            raise CastException('Failed to cast rough_process_simulation to ShapingProcessSimulation. Expected: {}.'.format(self.wrapped.RoughProcessSimulation.__class__.__qualname__))

        return constructor.new(_419.ShapingProcessSimulation)(self.wrapped.RoughProcessSimulation) if self.wrapped.RoughProcessSimulation else None

    @property
    def finish_cutter_simulation(self) -> '_489.GearCutterSimulation':
        '''GearCutterSimulation: 'FinishCutterSimulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_489.GearCutterSimulation)(self.wrapped.FinishCutterSimulation) if self.wrapped.FinishCutterSimulation else None

    @property
    def finish_cutter_simulation_of_type_finish_cutter_simulation(self) -> '_486.FinishCutterSimulation':
        '''FinishCutterSimulation: 'FinishCutterSimulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _486.FinishCutterSimulation.TYPE not in self.wrapped.FinishCutterSimulation.__class__.__mro__:
            raise CastException('Failed to cast finish_cutter_simulation to FinishCutterSimulation. Expected: {}.'.format(self.wrapped.FinishCutterSimulation.__class__.__qualname__))

        return constructor.new(_486.FinishCutterSimulation)(self.wrapped.FinishCutterSimulation) if self.wrapped.FinishCutterSimulation else None

    @property
    def finish_cutter_simulation_of_type_rough_cutter_simulation(self) -> '_493.RoughCutterSimulation':
        '''RoughCutterSimulation: 'FinishCutterSimulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _493.RoughCutterSimulation.TYPE not in self.wrapped.FinishCutterSimulation.__class__.__mro__:
            raise CastException('Failed to cast finish_cutter_simulation to RoughCutterSimulation. Expected: {}.'.format(self.wrapped.FinishCutterSimulation.__class__.__qualname__))

        return constructor.new(_493.RoughCutterSimulation)(self.wrapped.FinishCutterSimulation) if self.wrapped.FinishCutterSimulation else None

    @property
    def finish_process_simulation(self) -> '_417.CutterProcessSimulation':
        '''CutterProcessSimulation: 'FinishProcessSimulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_417.CutterProcessSimulation)(self.wrapped.FinishProcessSimulation) if self.wrapped.FinishProcessSimulation else None

    @property
    def finish_process_simulation_of_type_form_wheel_grinding_process_simulation(self) -> '_418.FormWheelGrindingProcessSimulation':
        '''FormWheelGrindingProcessSimulation: 'FinishProcessSimulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _418.FormWheelGrindingProcessSimulation.TYPE not in self.wrapped.FinishProcessSimulation.__class__.__mro__:
            raise CastException('Failed to cast finish_process_simulation to FormWheelGrindingProcessSimulation. Expected: {}.'.format(self.wrapped.FinishProcessSimulation.__class__.__qualname__))

        return constructor.new(_418.FormWheelGrindingProcessSimulation)(self.wrapped.FinishProcessSimulation) if self.wrapped.FinishProcessSimulation else None

    @property
    def finish_process_simulation_of_type_shaping_process_simulation(self) -> '_419.ShapingProcessSimulation':
        '''ShapingProcessSimulation: 'FinishProcessSimulation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _419.ShapingProcessSimulation.TYPE not in self.wrapped.FinishProcessSimulation.__class__.__mro__:
            raise CastException('Failed to cast finish_process_simulation to ShapingProcessSimulation. Expected: {}.'.format(self.wrapped.FinishProcessSimulation.__class__.__qualname__))

        return constructor.new(_419.ShapingProcessSimulation)(self.wrapped.FinishProcessSimulation) if self.wrapped.FinishProcessSimulation else None

    @property
    def design(self) -> '_766.CylindricalGearDesign':
        '''CylindricalGearDesign: 'Design' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_766.CylindricalGearDesign)(self.wrapped.Design) if self.wrapped.Design else None

    @property
    def rough_gear_specification(self) -> '_483.CylindricalGearSpecification':
        '''CylindricalGearSpecification: 'RoughGearSpecification' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_483.CylindricalGearSpecification)(self.wrapped.RoughGearSpecification) if self.wrapped.RoughGearSpecification else None

    @property
    def finished_gear_specification(self) -> '_483.CylindricalGearSpecification':
        '''CylindricalGearSpecification: 'FinishedGearSpecification' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_483.CylindricalGearSpecification)(self.wrapped.FinishedGearSpecification) if self.wrapped.FinishedGearSpecification else None

    @property
    def gear_blank(self) -> '_389.CylindricalGearBlank':
        '''CylindricalGearBlank: 'GearBlank' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_389.CylindricalGearBlank)(self.wrapped.GearBlank) if self.wrapped.GearBlank else None
