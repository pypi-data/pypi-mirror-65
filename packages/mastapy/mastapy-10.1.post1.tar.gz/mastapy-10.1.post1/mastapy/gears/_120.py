'''_120.py

BevelHypoidGearRatingSettings
'''


from mastapy.gears.materials import _390
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy.gears.rating.hypoid import _244
from mastapy.gears.rating.iso_10300 import _231, _223, _238
from mastapy.utility import _1139
from mastapy._internal.python_net import python_net_import

_BEVEL_HYPOID_GEAR_RATING_SETTINGS = python_net_import('SMT.MastaAPI.Gears', 'BevelHypoidGearRatingSettings')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelHypoidGearRatingSettings',)


class BevelHypoidGearRatingSettings(_1139.PerMachineSettings):
    '''BevelHypoidGearRatingSettings

    This is a mastapy class.
    '''

    TYPE = _BEVEL_HYPOID_GEAR_RATING_SETTINGS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelHypoidGearRatingSettings.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def bevel_gear_rating_method(self) -> '_390.RatingMethods':
        '''RatingMethods: 'BevelGearRatingMethod' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.BevelGearRatingMethod)
        return constructor.new(_390.RatingMethods)(value) if value else None

    @bevel_gear_rating_method.setter
    def bevel_gear_rating_method(self, value: '_390.RatingMethods'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.BevelGearRatingMethod = value

    @property
    def hypoid_gear_rating_method(self) -> '_244.HypoidRatingMethod':
        '''HypoidRatingMethod: 'HypoidGearRatingMethod' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.HypoidGearRatingMethod)
        return constructor.new(_244.HypoidRatingMethod)(value) if value else None

    @hypoid_gear_rating_method.setter
    def hypoid_gear_rating_method(self, value: '_244.HypoidRatingMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.HypoidGearRatingMethod = value

    @property
    def include_mesh_node_misalignments_in_default_report(self) -> 'bool':
        '''bool: 'IncludeMeshNodeMisalignmentsInDefaultReport' is the original name of this property.'''

        return self.wrapped.IncludeMeshNodeMisalignmentsInDefaultReport

    @include_mesh_node_misalignments_in_default_report.setter
    def include_mesh_node_misalignments_in_default_report(self, value: 'bool'):
        self.wrapped.IncludeMeshNodeMisalignmentsInDefaultReport = bool(value) if value else False

    @property
    def iso_rating_method_for_bevel_gears(self) -> '_231.ISO10300RatingMethod':
        '''ISO10300RatingMethod: 'ISORatingMethodForBevelGears' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.ISORatingMethodForBevelGears)
        return constructor.new(_231.ISO10300RatingMethod)(value) if value else None

    @iso_rating_method_for_bevel_gears.setter
    def iso_rating_method_for_bevel_gears(self, value: '_231.ISO10300RatingMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ISORatingMethodForBevelGears = value

    @property
    def iso_rating_method_for_hypoid_gears(self) -> '_231.ISO10300RatingMethod':
        '''ISO10300RatingMethod: 'ISORatingMethodForHypoidGears' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.ISORatingMethodForHypoidGears)
        return constructor.new(_231.ISO10300RatingMethod)(value) if value else None

    @iso_rating_method_for_hypoid_gears.setter
    def iso_rating_method_for_hypoid_gears(self, value: '_231.ISO10300RatingMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.ISORatingMethodForHypoidGears = value

    @property
    def bevel_general_load_factors_k_method(self) -> '_223.GeneralLoadFactorCalculationMethod':
        '''GeneralLoadFactorCalculationMethod: 'BevelGeneralLoadFactorsKMethod' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.BevelGeneralLoadFactorsKMethod)
        return constructor.new(_223.GeneralLoadFactorCalculationMethod)(value) if value else None

    @bevel_general_load_factors_k_method.setter
    def bevel_general_load_factors_k_method(self, value: '_223.GeneralLoadFactorCalculationMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.BevelGeneralLoadFactorsKMethod = value

    @property
    def hypoid_general_load_factors_k_method(self) -> '_223.GeneralLoadFactorCalculationMethod':
        '''GeneralLoadFactorCalculationMethod: 'HypoidGeneralLoadFactorsKMethod' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.HypoidGeneralLoadFactorsKMethod)
        return constructor.new(_223.GeneralLoadFactorCalculationMethod)(value) if value else None

    @hypoid_general_load_factors_k_method.setter
    def hypoid_general_load_factors_k_method(self, value: '_223.GeneralLoadFactorCalculationMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.HypoidGeneralLoadFactorsKMethod = value

    @property
    def bevel_pitting_factor_calculation_method(self) -> '_238.PittingFactorCalculationMethod':
        '''PittingFactorCalculationMethod: 'BevelPittingFactorCalculationMethod' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.BevelPittingFactorCalculationMethod)
        return constructor.new(_238.PittingFactorCalculationMethod)(value) if value else None

    @bevel_pitting_factor_calculation_method.setter
    def bevel_pitting_factor_calculation_method(self, value: '_238.PittingFactorCalculationMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.BevelPittingFactorCalculationMethod = value

    @property
    def hypoid_pitting_factor_calculation_method(self) -> '_238.PittingFactorCalculationMethod':
        '''PittingFactorCalculationMethod: 'HypoidPittingFactorCalculationMethod' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.HypoidPittingFactorCalculationMethod)
        return constructor.new(_238.PittingFactorCalculationMethod)(value) if value else None

    @hypoid_pitting_factor_calculation_method.setter
    def hypoid_pitting_factor_calculation_method(self, value: '_238.PittingFactorCalculationMethod'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.HypoidPittingFactorCalculationMethod = value
