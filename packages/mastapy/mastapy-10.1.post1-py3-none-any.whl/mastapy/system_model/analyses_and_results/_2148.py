'''_2148.py

PowerFlowAnalysis
'''


from mastapy.system_model.analyses_and_results.static_loads import (
    _6188, _6189, _6191, _6135,
    _6134, _6033, _6046, _6045,
    _6051, _6050, _6064, _6063,
    _6066, _6067, _6144, _6150,
    _6148, _6146, _6160, _6159,
    _6171, _6170, _6172, _6173,
    _6177, _6178, _6179, _6065,
    _6032, _6047, _6060, _6115,
    _6136, _6147, _6152, _6035,
    _6053, _6091, _6163, _6040,
    _6057, _6027, _6070, _6111,
    _6117, _6120, _6123, _6156,
    _6166, _6187, _6190, _6097,
    _6133, _6044, _6049, _6062,
    _6158, _6176, _6023, _6024,
    _6031, _6043, _6042, _6048,
    _6061, _6076, _6089, _6093,
    _6030, _6101, _6113, _6125,
    _6126, _6128, _6130, _6132,
    _6139, _6142, _6143, _6149,
    _6153, _6184, _6185, _6151,
    _6052, _6054, _6090, _6092,
    _6026, _6028, _6034, _6036,
    _6037, _6038, _6039, _6041,
    _6055, _6059, _6068, _6072,
    _6073, _6095, _6100, _6110,
    _6112, _6116, _6118, _6119,
    _6121, _6122, _6124, _6137,
    _6155, _6157, _6162, _6164,
    _6165, _6167, _6168, _6169,
    _6186
)
from mastapy.system_model.analyses_and_results.power_flows import (
    _3314, _3316, _3317, _3270,
    _3269, _3201, _3214, _3213,
    _3219, _3218, _3230, _3229,
    _3232, _3233, _3278, _3283,
    _3281, _3279, _3292, _3291,
    _3303, _3301, _3302, _3304,
    _3307, _3308, _3309, _3231,
    _3200, _3215, _3226, _3253,
    _3271, _3280, _3285, _3202,
    _3220, _3241, _3293, _3207,
    _3223, _3195, _3235, _3249,
    _3254, _3257, _3260, _3287,
    _3296, _3312, _3315, _3245,
    _3268, _3212, _3217, _3228,
    _3290, _3306, _3193, _3194,
    _3199, _3211, _3210, _3216,
    _3227, _3239, _3240, _3244,
    _3198, _3248, _3252, _3263,
    _3264, _3265, _3266, _3267,
    _3273, _3274, _3277, _3282,
    _3286, _3310, _3311, _3284,
    _3221, _3222, _3242, _3243,
    _3196, _3197, _3203, _3204,
    _3205, _3206, _3208, _3209,
    _3224, _3225, _3236, _3237,
    _3238, _3246, _3247, _3250,
    _3251, _3255, _3256, _3258,
    _3259, _3261, _3262, _3272,
    _3288, _3289, _3294, _3295,
    _3297, _3298, _3299, _3300,
    _3313
)
from mastapy._internal import constructor
from mastapy.system_model.part_model.gears import (
    _2069, _2070, _2037, _2038,
    _2044, _2045, _2029, _2030,
    _2031, _2032, _2033, _2034,
    _2035, _2036, _2039, _2040,
    _2041, _2042, _2043, _2046,
    _2048, _2050, _2051, _2052,
    _2053, _2054, _2055, _2056,
    _2057, _2058, _2059, _2060,
    _2061, _2062, _2063, _2064,
    _2065, _2066, _2067, _2068
)
from mastapy.system_model.part_model.couplings import (
    _2099, _2100, _2088, _2090,
    _2091, _2093, _2094, _2095,
    _2096, _2097, _2098, _2101,
    _2109, _2107, _2108, _2110,
    _2111, _2112, _2114, _2115,
    _2116, _2117, _2118, _2120
)
from mastapy.system_model.connections_and_sockets import (
    _1815, _1810, _1811, _1814,
    _1823, _1826, _1830, _1834
)
from mastapy.system_model.connections_and_sockets.gears import (
    _1840, _1844, _1850, _1864,
    _1842, _1846, _1838, _1848,
    _1854, _1857, _1858, _1859,
    _1862, _1866, _1868, _1870,
    _1852
)
from mastapy.system_model.connections_and_sockets.couplings import (
    _1878, _1872, _1874, _1876,
    _1880, _1882
)
from mastapy.system_model.part_model import (
    _1958, _1959, _1962, _1964,
    _1965, _1966, _1969, _1970,
    _1973, _1974, _1957, _1975,
    _1978, _1981, _1982, _1983,
    _1985, _1986, _1987, _1989,
    _1990, _1992, _1994, _1995,
    _1996
)
from mastapy.system_model.part_model.shaft_model import _1999
from mastapy.system_model.analyses_and_results import _2130
from mastapy._internal.python_net import python_net_import

_POWER_FLOW_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'PowerFlowAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('PowerFlowAnalysis',)


class PowerFlowAnalysis(_2130.SingleAnalysis):
    '''PowerFlowAnalysis

    This is a mastapy class.
    '''

    TYPE = _POWER_FLOW_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PowerFlowAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    def results_for_worm_gear_set_load_case(self, design_entity_analysis: '_6188.WormGearSetLoadCase') -> '_3314.WormGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.WormGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3314.WormGearSetPowerFlow)(method_result) if method_result else None

    def results_for_zerol_bevel_gear(self, design_entity: '_2069.ZerolBevelGear') -> '_3316.ZerolBevelGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ZerolBevelGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3316.ZerolBevelGearPowerFlow)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_load_case(self, design_entity_analysis: '_6189.ZerolBevelGearLoadCase') -> '_3316.ZerolBevelGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ZerolBevelGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3316.ZerolBevelGearPowerFlow)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_set(self, design_entity: '_2070.ZerolBevelGearSet') -> '_3317.ZerolBevelGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ZerolBevelGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3317.ZerolBevelGearSetPowerFlow)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_set_load_case(self, design_entity_analysis: '_6191.ZerolBevelGearSetLoadCase') -> '_3317.ZerolBevelGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ZerolBevelGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3317.ZerolBevelGearSetPowerFlow)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling(self, design_entity: '_2099.PartToPartShearCoupling') -> '_3270.PartToPartShearCouplingPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCoupling)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PartToPartShearCouplingPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3270.PartToPartShearCouplingPowerFlow)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_load_case(self, design_entity_analysis: '_6135.PartToPartShearCouplingLoadCase') -> '_3270.PartToPartShearCouplingPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PartToPartShearCouplingPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3270.PartToPartShearCouplingPowerFlow)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_half(self, design_entity: '_2100.PartToPartShearCouplingHalf') -> '_3269.PartToPartShearCouplingHalfPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PartToPartShearCouplingHalfPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3269.PartToPartShearCouplingHalfPowerFlow)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_half_load_case(self, design_entity_analysis: '_6134.PartToPartShearCouplingHalfLoadCase') -> '_3269.PartToPartShearCouplingHalfPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PartToPartShearCouplingHalfPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3269.PartToPartShearCouplingHalfPowerFlow)(method_result) if method_result else None

    def results_for_belt_drive(self, design_entity: '_2088.BeltDrive') -> '_3201.BeltDrivePowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BeltDrivePowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3201.BeltDrivePowerFlow)(method_result) if method_result else None

    def results_for_belt_drive_load_case(self, design_entity_analysis: '_6033.BeltDriveLoadCase') -> '_3201.BeltDrivePowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BeltDriveLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BeltDrivePowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3201.BeltDrivePowerFlow)(method_result) if method_result else None

    def results_for_clutch(self, design_entity: '_2090.Clutch') -> '_3214.ClutchPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ClutchPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3214.ClutchPowerFlow)(method_result) if method_result else None

    def results_for_clutch_load_case(self, design_entity_analysis: '_6046.ClutchLoadCase') -> '_3214.ClutchPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ClutchPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3214.ClutchPowerFlow)(method_result) if method_result else None

    def results_for_clutch_half(self, design_entity: '_2091.ClutchHalf') -> '_3213.ClutchHalfPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ClutchHalfPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3213.ClutchHalfPowerFlow)(method_result) if method_result else None

    def results_for_clutch_half_load_case(self, design_entity_analysis: '_6045.ClutchHalfLoadCase') -> '_3213.ClutchHalfPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ClutchHalfPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3213.ClutchHalfPowerFlow)(method_result) if method_result else None

    def results_for_concept_coupling(self, design_entity: '_2093.ConceptCoupling') -> '_3219.ConceptCouplingPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConceptCouplingPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3219.ConceptCouplingPowerFlow)(method_result) if method_result else None

    def results_for_concept_coupling_load_case(self, design_entity_analysis: '_6051.ConceptCouplingLoadCase') -> '_3219.ConceptCouplingPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConceptCouplingPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3219.ConceptCouplingPowerFlow)(method_result) if method_result else None

    def results_for_concept_coupling_half(self, design_entity: '_2094.ConceptCouplingHalf') -> '_3218.ConceptCouplingHalfPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConceptCouplingHalfPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3218.ConceptCouplingHalfPowerFlow)(method_result) if method_result else None

    def results_for_concept_coupling_half_load_case(self, design_entity_analysis: '_6050.ConceptCouplingHalfLoadCase') -> '_3218.ConceptCouplingHalfPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConceptCouplingHalfPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3218.ConceptCouplingHalfPowerFlow)(method_result) if method_result else None

    def results_for_coupling(self, design_entity: '_2095.Coupling') -> '_3230.CouplingPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CouplingPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3230.CouplingPowerFlow)(method_result) if method_result else None

    def results_for_coupling_load_case(self, design_entity_analysis: '_6064.CouplingLoadCase') -> '_3230.CouplingPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CouplingPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3230.CouplingPowerFlow)(method_result) if method_result else None

    def results_for_coupling_half(self, design_entity: '_2096.CouplingHalf') -> '_3229.CouplingHalfPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CouplingHalfPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3229.CouplingHalfPowerFlow)(method_result) if method_result else None

    def results_for_coupling_half_load_case(self, design_entity_analysis: '_6063.CouplingHalfLoadCase') -> '_3229.CouplingHalfPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CouplingHalfPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3229.CouplingHalfPowerFlow)(method_result) if method_result else None

    def results_for_cvt(self, design_entity: '_2097.CVT') -> '_3232.CVTPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CVTPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3232.CVTPowerFlow)(method_result) if method_result else None

    def results_for_cvt_load_case(self, design_entity_analysis: '_6066.CVTLoadCase') -> '_3232.CVTPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CVTPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3232.CVTPowerFlow)(method_result) if method_result else None

    def results_for_cvt_pulley(self, design_entity: '_2098.CVTPulley') -> '_3233.CVTPulleyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CVTPulleyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3233.CVTPulleyPowerFlow)(method_result) if method_result else None

    def results_for_cvt_pulley_load_case(self, design_entity_analysis: '_6067.CVTPulleyLoadCase') -> '_3233.CVTPulleyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTPulleyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CVTPulleyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3233.CVTPulleyPowerFlow)(method_result) if method_result else None

    def results_for_pulley(self, design_entity: '_2101.Pulley') -> '_3278.PulleyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PulleyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3278.PulleyPowerFlow)(method_result) if method_result else None

    def results_for_pulley_load_case(self, design_entity_analysis: '_6144.PulleyLoadCase') -> '_3278.PulleyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PulleyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PulleyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3278.PulleyPowerFlow)(method_result) if method_result else None

    def results_for_shaft_hub_connection(self, design_entity: '_2109.ShaftHubConnection') -> '_3283.ShaftHubConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ShaftHubConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3283.ShaftHubConnectionPowerFlow)(method_result) if method_result else None

    def results_for_shaft_hub_connection_load_case(self, design_entity_analysis: '_6150.ShaftHubConnectionLoadCase') -> '_3283.ShaftHubConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftHubConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ShaftHubConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3283.ShaftHubConnectionPowerFlow)(method_result) if method_result else None

    def results_for_rolling_ring(self, design_entity: '_2107.RollingRing') -> '_3281.RollingRingPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.RollingRingPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3281.RollingRingPowerFlow)(method_result) if method_result else None

    def results_for_rolling_ring_load_case(self, design_entity_analysis: '_6148.RollingRingLoadCase') -> '_3281.RollingRingPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.RollingRingPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3281.RollingRingPowerFlow)(method_result) if method_result else None

    def results_for_rolling_ring_assembly(self, design_entity: '_2108.RollingRingAssembly') -> '_3279.RollingRingAssemblyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.RollingRingAssemblyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3279.RollingRingAssemblyPowerFlow)(method_result) if method_result else None

    def results_for_rolling_ring_assembly_load_case(self, design_entity_analysis: '_6146.RollingRingAssemblyLoadCase') -> '_3279.RollingRingAssemblyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.RollingRingAssemblyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3279.RollingRingAssemblyPowerFlow)(method_result) if method_result else None

    def results_for_spring_damper(self, design_entity: '_2110.SpringDamper') -> '_3292.SpringDamperPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SpringDamperPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3292.SpringDamperPowerFlow)(method_result) if method_result else None

    def results_for_spring_damper_load_case(self, design_entity_analysis: '_6160.SpringDamperLoadCase') -> '_3292.SpringDamperPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SpringDamperPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3292.SpringDamperPowerFlow)(method_result) if method_result else None

    def results_for_spring_damper_half(self, design_entity: '_2111.SpringDamperHalf') -> '_3291.SpringDamperHalfPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SpringDamperHalfPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3291.SpringDamperHalfPowerFlow)(method_result) if method_result else None

    def results_for_spring_damper_half_load_case(self, design_entity_analysis: '_6159.SpringDamperHalfLoadCase') -> '_3291.SpringDamperHalfPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SpringDamperHalfPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3291.SpringDamperHalfPowerFlow)(method_result) if method_result else None

    def results_for_synchroniser(self, design_entity: '_2112.Synchroniser') -> '_3303.SynchroniserPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SynchroniserPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3303.SynchroniserPowerFlow)(method_result) if method_result else None

    def results_for_synchroniser_load_case(self, design_entity_analysis: '_6171.SynchroniserLoadCase') -> '_3303.SynchroniserPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SynchroniserPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3303.SynchroniserPowerFlow)(method_result) if method_result else None

    def results_for_synchroniser_half(self, design_entity: '_2114.SynchroniserHalf') -> '_3301.SynchroniserHalfPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SynchroniserHalfPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3301.SynchroniserHalfPowerFlow)(method_result) if method_result else None

    def results_for_synchroniser_half_load_case(self, design_entity_analysis: '_6170.SynchroniserHalfLoadCase') -> '_3301.SynchroniserHalfPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SynchroniserHalfPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3301.SynchroniserHalfPowerFlow)(method_result) if method_result else None

    def results_for_synchroniser_part(self, design_entity: '_2115.SynchroniserPart') -> '_3302.SynchroniserPartPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SynchroniserPartPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3302.SynchroniserPartPowerFlow)(method_result) if method_result else None

    def results_for_synchroniser_part_load_case(self, design_entity_analysis: '_6172.SynchroniserPartLoadCase') -> '_3302.SynchroniserPartPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserPartLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SynchroniserPartPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3302.SynchroniserPartPowerFlow)(method_result) if method_result else None

    def results_for_synchroniser_sleeve(self, design_entity: '_2116.SynchroniserSleeve') -> '_3304.SynchroniserSleevePowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SynchroniserSleevePowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3304.SynchroniserSleevePowerFlow)(method_result) if method_result else None

    def results_for_synchroniser_sleeve_load_case(self, design_entity_analysis: '_6173.SynchroniserSleeveLoadCase') -> '_3304.SynchroniserSleevePowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserSleeveLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SynchroniserSleevePowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3304.SynchroniserSleevePowerFlow)(method_result) if method_result else None

    def results_for_torque_converter(self, design_entity: '_2117.TorqueConverter') -> '_3307.TorqueConverterPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.TorqueConverterPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3307.TorqueConverterPowerFlow)(method_result) if method_result else None

    def results_for_torque_converter_load_case(self, design_entity_analysis: '_6177.TorqueConverterLoadCase') -> '_3307.TorqueConverterPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.TorqueConverterPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3307.TorqueConverterPowerFlow)(method_result) if method_result else None

    def results_for_torque_converter_pump(self, design_entity: '_2118.TorqueConverterPump') -> '_3308.TorqueConverterPumpPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.TorqueConverterPumpPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3308.TorqueConverterPumpPowerFlow)(method_result) if method_result else None

    def results_for_torque_converter_pump_load_case(self, design_entity_analysis: '_6178.TorqueConverterPumpLoadCase') -> '_3308.TorqueConverterPumpPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterPumpLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.TorqueConverterPumpPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3308.TorqueConverterPumpPowerFlow)(method_result) if method_result else None

    def results_for_torque_converter_turbine(self, design_entity: '_2120.TorqueConverterTurbine') -> '_3309.TorqueConverterTurbinePowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.TorqueConverterTurbinePowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3309.TorqueConverterTurbinePowerFlow)(method_result) if method_result else None

    def results_for_torque_converter_turbine_load_case(self, design_entity_analysis: '_6179.TorqueConverterTurbineLoadCase') -> '_3309.TorqueConverterTurbinePowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterTurbineLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.TorqueConverterTurbinePowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3309.TorqueConverterTurbinePowerFlow)(method_result) if method_result else None

    def results_for_cvt_belt_connection(self, design_entity: '_1815.CVTBeltConnection') -> '_3231.CVTBeltConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CVTBeltConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3231.CVTBeltConnectionPowerFlow)(method_result) if method_result else None

    def results_for_cvt_belt_connection_load_case(self, design_entity_analysis: '_6065.CVTBeltConnectionLoadCase') -> '_3231.CVTBeltConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTBeltConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CVTBeltConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3231.CVTBeltConnectionPowerFlow)(method_result) if method_result else None

    def results_for_belt_connection(self, design_entity: '_1810.BeltConnection') -> '_3200.BeltConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BeltConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3200.BeltConnectionPowerFlow)(method_result) if method_result else None

    def results_for_belt_connection_load_case(self, design_entity_analysis: '_6032.BeltConnectionLoadCase') -> '_3200.BeltConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BeltConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BeltConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3200.BeltConnectionPowerFlow)(method_result) if method_result else None

    def results_for_coaxial_connection(self, design_entity: '_1811.CoaxialConnection') -> '_3215.CoaxialConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CoaxialConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3215.CoaxialConnectionPowerFlow)(method_result) if method_result else None

    def results_for_coaxial_connection_load_case(self, design_entity_analysis: '_6047.CoaxialConnectionLoadCase') -> '_3215.CoaxialConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CoaxialConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CoaxialConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3215.CoaxialConnectionPowerFlow)(method_result) if method_result else None

    def results_for_connection(self, design_entity: '_1814.Connection') -> '_3226.ConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3226.ConnectionPowerFlow)(method_result) if method_result else None

    def results_for_connection_load_case(self, design_entity_analysis: '_6060.ConnectionLoadCase') -> '_3226.ConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3226.ConnectionPowerFlow)(method_result) if method_result else None

    def results_for_inter_mountable_component_connection(self, design_entity: '_1823.InterMountableComponentConnection') -> '_3253.InterMountableComponentConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.InterMountableComponentConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3253.InterMountableComponentConnectionPowerFlow)(method_result) if method_result else None

    def results_for_inter_mountable_component_connection_load_case(self, design_entity_analysis: '_6115.InterMountableComponentConnectionLoadCase') -> '_3253.InterMountableComponentConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.InterMountableComponentConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.InterMountableComponentConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3253.InterMountableComponentConnectionPowerFlow)(method_result) if method_result else None

    def results_for_planetary_connection(self, design_entity: '_1826.PlanetaryConnection') -> '_3271.PlanetaryConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PlanetaryConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3271.PlanetaryConnectionPowerFlow)(method_result) if method_result else None

    def results_for_planetary_connection_load_case(self, design_entity_analysis: '_6136.PlanetaryConnectionLoadCase') -> '_3271.PlanetaryConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetaryConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PlanetaryConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3271.PlanetaryConnectionPowerFlow)(method_result) if method_result else None

    def results_for_rolling_ring_connection(self, design_entity: '_1830.RollingRingConnection') -> '_3280.RollingRingConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.RollingRingConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3280.RollingRingConnectionPowerFlow)(method_result) if method_result else None

    def results_for_rolling_ring_connection_load_case(self, design_entity_analysis: '_6147.RollingRingConnectionLoadCase') -> '_3280.RollingRingConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.RollingRingConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3280.RollingRingConnectionPowerFlow)(method_result) if method_result else None

    def results_for_shaft_to_mountable_component_connection(self, design_entity: '_1834.ShaftToMountableComponentConnection') -> '_3285.ShaftToMountableComponentConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ShaftToMountableComponentConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3285.ShaftToMountableComponentConnectionPowerFlow)(method_result) if method_result else None

    def results_for_shaft_to_mountable_component_connection_load_case(self, design_entity_analysis: '_6152.ShaftToMountableComponentConnectionLoadCase') -> '_3285.ShaftToMountableComponentConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftToMountableComponentConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ShaftToMountableComponentConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3285.ShaftToMountableComponentConnectionPowerFlow)(method_result) if method_result else None

    def results_for_bevel_differential_gear_mesh(self, design_entity: '_1840.BevelDifferentialGearMesh') -> '_3202.BevelDifferentialGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelDifferentialGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3202.BevelDifferentialGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_bevel_differential_gear_mesh_load_case(self, design_entity_analysis: '_6035.BevelDifferentialGearMeshLoadCase') -> '_3202.BevelDifferentialGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelDifferentialGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3202.BevelDifferentialGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_concept_gear_mesh(self, design_entity: '_1844.ConceptGearMesh') -> '_3220.ConceptGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConceptGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3220.ConceptGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_concept_gear_mesh_load_case(self, design_entity_analysis: '_6053.ConceptGearMeshLoadCase') -> '_3220.ConceptGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConceptGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3220.ConceptGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_face_gear_mesh(self, design_entity: '_1850.FaceGearMesh') -> '_3241.FaceGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.FaceGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3241.FaceGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_face_gear_mesh_load_case(self, design_entity_analysis: '_6091.FaceGearMeshLoadCase') -> '_3241.FaceGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.FaceGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3241.FaceGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_mesh(self, design_entity: '_1864.StraightBevelDiffGearMesh') -> '_3293.StraightBevelDiffGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelDiffGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3293.StraightBevelDiffGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_mesh_load_case(self, design_entity_analysis: '_6163.StraightBevelDiffGearMeshLoadCase') -> '_3293.StraightBevelDiffGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelDiffGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3293.StraightBevelDiffGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_bevel_gear_mesh(self, design_entity: '_1842.BevelGearMesh') -> '_3207.BevelGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3207.BevelGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6040.BevelGearMeshLoadCase') -> '_3207.BevelGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3207.BevelGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_conical_gear_mesh(self, design_entity: '_1846.ConicalGearMesh') -> '_3223.ConicalGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConicalGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3223.ConicalGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_conical_gear_mesh_load_case(self, design_entity_analysis: '_6057.ConicalGearMeshLoadCase') -> '_3223.ConicalGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConicalGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3223.ConicalGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_mesh(self, design_entity: '_1838.AGMAGleasonConicalGearMesh') -> '_3195.AGMAGleasonConicalGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.AGMAGleasonConicalGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3195.AGMAGleasonConicalGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_mesh_load_case(self, design_entity_analysis: '_6027.AGMAGleasonConicalGearMeshLoadCase') -> '_3195.AGMAGleasonConicalGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.AGMAGleasonConicalGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3195.AGMAGleasonConicalGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_cylindrical_gear_mesh(self, design_entity: '_1848.CylindricalGearMesh') -> '_3235.CylindricalGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CylindricalGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3235.CylindricalGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_cylindrical_gear_mesh_load_case(self, design_entity_analysis: '_6070.CylindricalGearMeshLoadCase') -> '_3235.CylindricalGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CylindricalGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3235.CylindricalGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_hypoid_gear_mesh(self, design_entity: '_1854.HypoidGearMesh') -> '_3249.HypoidGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.HypoidGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3249.HypoidGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_hypoid_gear_mesh_load_case(self, design_entity_analysis: '_6111.HypoidGearMeshLoadCase') -> '_3249.HypoidGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.HypoidGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3249.HypoidGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh(self, design_entity: '_1857.KlingelnbergCycloPalloidConicalGearMesh') -> '_3254.KlingelnbergCycloPalloidConicalGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidConicalGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3254.KlingelnbergCycloPalloidConicalGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh_load_case(self, design_entity_analysis: '_6117.KlingelnbergCycloPalloidConicalGearMeshLoadCase') -> '_3254.KlingelnbergCycloPalloidConicalGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidConicalGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3254.KlingelnbergCycloPalloidConicalGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, design_entity: '_1858.KlingelnbergCycloPalloidHypoidGearMesh') -> '_3257.KlingelnbergCycloPalloidHypoidGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidHypoidGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3257.KlingelnbergCycloPalloidHypoidGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh_load_case(self, design_entity_analysis: '_6120.KlingelnbergCycloPalloidHypoidGearMeshLoadCase') -> '_3257.KlingelnbergCycloPalloidHypoidGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidHypoidGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3257.KlingelnbergCycloPalloidHypoidGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, design_entity: '_1859.KlingelnbergCycloPalloidSpiralBevelGearMesh') -> '_3260.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3260.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6123.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase') -> '_3260.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3260.KlingelnbergCycloPalloidSpiralBevelGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_mesh(self, design_entity: '_1862.SpiralBevelGearMesh') -> '_3287.SpiralBevelGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SpiralBevelGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3287.SpiralBevelGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6156.SpiralBevelGearMeshLoadCase') -> '_3287.SpiralBevelGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SpiralBevelGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3287.SpiralBevelGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_gear_mesh(self, design_entity: '_1866.StraightBevelGearMesh') -> '_3296.StraightBevelGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3296.StraightBevelGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6166.StraightBevelGearMeshLoadCase') -> '_3296.StraightBevelGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3296.StraightBevelGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_worm_gear_mesh(self, design_entity: '_1868.WormGearMesh') -> '_3312.WormGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.WormGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3312.WormGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_worm_gear_mesh_load_case(self, design_entity_analysis: '_6187.WormGearMeshLoadCase') -> '_3312.WormGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.WormGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3312.WormGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_mesh(self, design_entity: '_1870.ZerolBevelGearMesh') -> '_3315.ZerolBevelGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ZerolBevelGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3315.ZerolBevelGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6190.ZerolBevelGearMeshLoadCase') -> '_3315.ZerolBevelGearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ZerolBevelGearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3315.ZerolBevelGearMeshPowerFlow)(method_result) if method_result else None

    def results_for_gear_mesh(self, design_entity: '_1852.GearMesh') -> '_3245.GearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.GearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3245.GearMeshPowerFlow)(method_result) if method_result else None

    def results_for_gear_mesh_load_case(self, design_entity_analysis: '_6097.GearMeshLoadCase') -> '_3245.GearMeshPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.GearMeshPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3245.GearMeshPowerFlow)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_connection(self, design_entity: '_1878.PartToPartShearCouplingConnection') -> '_3268.PartToPartShearCouplingConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PartToPartShearCouplingConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3268.PartToPartShearCouplingConnectionPowerFlow)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_connection_load_case(self, design_entity_analysis: '_6133.PartToPartShearCouplingConnectionLoadCase') -> '_3268.PartToPartShearCouplingConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PartToPartShearCouplingConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3268.PartToPartShearCouplingConnectionPowerFlow)(method_result) if method_result else None

    def results_for_clutch_connection(self, design_entity: '_1872.ClutchConnection') -> '_3212.ClutchConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ClutchConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3212.ClutchConnectionPowerFlow)(method_result) if method_result else None

    def results_for_clutch_connection_load_case(self, design_entity_analysis: '_6044.ClutchConnectionLoadCase') -> '_3212.ClutchConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ClutchConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3212.ClutchConnectionPowerFlow)(method_result) if method_result else None

    def results_for_concept_coupling_connection(self, design_entity: '_1874.ConceptCouplingConnection') -> '_3217.ConceptCouplingConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConceptCouplingConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3217.ConceptCouplingConnectionPowerFlow)(method_result) if method_result else None

    def results_for_concept_coupling_connection_load_case(self, design_entity_analysis: '_6049.ConceptCouplingConnectionLoadCase') -> '_3217.ConceptCouplingConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConceptCouplingConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3217.ConceptCouplingConnectionPowerFlow)(method_result) if method_result else None

    def results_for_coupling_connection(self, design_entity: '_1876.CouplingConnection') -> '_3228.CouplingConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CouplingConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3228.CouplingConnectionPowerFlow)(method_result) if method_result else None

    def results_for_coupling_connection_load_case(self, design_entity_analysis: '_6062.CouplingConnectionLoadCase') -> '_3228.CouplingConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CouplingConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3228.CouplingConnectionPowerFlow)(method_result) if method_result else None

    def results_for_spring_damper_connection(self, design_entity: '_1880.SpringDamperConnection') -> '_3290.SpringDamperConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SpringDamperConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3290.SpringDamperConnectionPowerFlow)(method_result) if method_result else None

    def results_for_spring_damper_connection_load_case(self, design_entity_analysis: '_6158.SpringDamperConnectionLoadCase') -> '_3290.SpringDamperConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SpringDamperConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3290.SpringDamperConnectionPowerFlow)(method_result) if method_result else None

    def results_for_torque_converter_connection(self, design_entity: '_1882.TorqueConverterConnection') -> '_3306.TorqueConverterConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.TorqueConverterConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3306.TorqueConverterConnectionPowerFlow)(method_result) if method_result else None

    def results_for_torque_converter_connection_load_case(self, design_entity_analysis: '_6176.TorqueConverterConnectionLoadCase') -> '_3306.TorqueConverterConnectionPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.TorqueConverterConnectionPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3306.TorqueConverterConnectionPowerFlow)(method_result) if method_result else None

    def results_for_abstract_assembly(self, design_entity: '_1958.AbstractAssembly') -> '_3193.AbstractAssemblyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.AbstractAssemblyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3193.AbstractAssemblyPowerFlow)(method_result) if method_result else None

    def results_for_abstract_assembly_load_case(self, design_entity_analysis: '_6023.AbstractAssemblyLoadCase') -> '_3193.AbstractAssemblyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.AbstractAssemblyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3193.AbstractAssemblyPowerFlow)(method_result) if method_result else None

    def results_for_abstract_shaft_or_housing(self, design_entity: '_1959.AbstractShaftOrHousing') -> '_3194.AbstractShaftOrHousingPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.AbstractShaftOrHousingPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3194.AbstractShaftOrHousingPowerFlow)(method_result) if method_result else None

    def results_for_abstract_shaft_or_housing_load_case(self, design_entity_analysis: '_6024.AbstractShaftOrHousingLoadCase') -> '_3194.AbstractShaftOrHousingPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractShaftOrHousingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.AbstractShaftOrHousingPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3194.AbstractShaftOrHousingPowerFlow)(method_result) if method_result else None

    def results_for_bearing(self, design_entity: '_1962.Bearing') -> '_3199.BearingPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BearingPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3199.BearingPowerFlow)(method_result) if method_result else None

    def results_for_bearing_load_case(self, design_entity_analysis: '_6031.BearingLoadCase') -> '_3199.BearingPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BearingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BearingPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3199.BearingPowerFlow)(method_result) if method_result else None

    def results_for_bolt(self, design_entity: '_1964.Bolt') -> '_3211.BoltPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BoltPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3211.BoltPowerFlow)(method_result) if method_result else None

    def results_for_bolt_load_case(self, design_entity_analysis: '_6043.BoltLoadCase') -> '_3211.BoltPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BoltLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BoltPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3211.BoltPowerFlow)(method_result) if method_result else None

    def results_for_bolted_joint(self, design_entity: '_1965.BoltedJoint') -> '_3210.BoltedJointPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BoltedJointPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3210.BoltedJointPowerFlow)(method_result) if method_result else None

    def results_for_bolted_joint_load_case(self, design_entity_analysis: '_6042.BoltedJointLoadCase') -> '_3210.BoltedJointPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BoltedJointLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BoltedJointPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3210.BoltedJointPowerFlow)(method_result) if method_result else None

    def results_for_component(self, design_entity: '_1966.Component') -> '_3216.ComponentPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ComponentPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3216.ComponentPowerFlow)(method_result) if method_result else None

    def results_for_component_load_case(self, design_entity_analysis: '_6048.ComponentLoadCase') -> '_3216.ComponentPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ComponentPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3216.ComponentPowerFlow)(method_result) if method_result else None

    def results_for_connector(self, design_entity: '_1969.Connector') -> '_3227.ConnectorPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Connector)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConnectorPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3227.ConnectorPowerFlow)(method_result) if method_result else None

    def results_for_connector_load_case(self, design_entity_analysis: '_6061.ConnectorLoadCase') -> '_3227.ConnectorPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConnectorLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConnectorPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3227.ConnectorPowerFlow)(method_result) if method_result else None

    def results_for_datum(self, design_entity: '_1970.Datum') -> '_3239.DatumPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Datum)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.DatumPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3239.DatumPowerFlow)(method_result) if method_result else None

    def results_for_datum_load_case(self, design_entity_analysis: '_6076.DatumLoadCase') -> '_3239.DatumPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.DatumLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.DatumPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3239.DatumPowerFlow)(method_result) if method_result else None

    def results_for_external_cad_model(self, design_entity: '_1973.ExternalCADModel') -> '_3240.ExternalCADModelPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ExternalCADModelPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3240.ExternalCADModelPowerFlow)(method_result) if method_result else None

    def results_for_external_cad_model_load_case(self, design_entity_analysis: '_6089.ExternalCADModelLoadCase') -> '_3240.ExternalCADModelPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ExternalCADModelLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ExternalCADModelPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3240.ExternalCADModelPowerFlow)(method_result) if method_result else None

    def results_for_flexible_pin_assembly(self, design_entity: '_1974.FlexiblePinAssembly') -> '_3244.FlexiblePinAssemblyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.FlexiblePinAssemblyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3244.FlexiblePinAssemblyPowerFlow)(method_result) if method_result else None

    def results_for_flexible_pin_assembly_load_case(self, design_entity_analysis: '_6093.FlexiblePinAssemblyLoadCase') -> '_3244.FlexiblePinAssemblyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FlexiblePinAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.FlexiblePinAssemblyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3244.FlexiblePinAssemblyPowerFlow)(method_result) if method_result else None

    def results_for_assembly(self, design_entity: '_1957.Assembly') -> '_3198.AssemblyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.AssemblyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3198.AssemblyPowerFlow)(method_result) if method_result else None

    def results_for_assembly_load_case(self, design_entity_analysis: '_6030.AssemblyLoadCase') -> '_3198.AssemblyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.AssemblyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3198.AssemblyPowerFlow)(method_result) if method_result else None

    def results_for_guide_dxf_model(self, design_entity: '_1975.GuideDxfModel') -> '_3248.GuideDxfModelPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.GuideDxfModelPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3248.GuideDxfModelPowerFlow)(method_result) if method_result else None

    def results_for_guide_dxf_model_load_case(self, design_entity_analysis: '_6101.GuideDxfModelLoadCase') -> '_3248.GuideDxfModelPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GuideDxfModelLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.GuideDxfModelPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3248.GuideDxfModelPowerFlow)(method_result) if method_result else None

    def results_for_imported_fe_component(self, design_entity: '_1978.ImportedFEComponent') -> '_3252.ImportedFEComponentPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ImportedFEComponent)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ImportedFEComponentPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3252.ImportedFEComponentPowerFlow)(method_result) if method_result else None

    def results_for_imported_fe_component_load_case(self, design_entity_analysis: '_6113.ImportedFEComponentLoadCase') -> '_3252.ImportedFEComponentPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ImportedFEComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ImportedFEComponentPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3252.ImportedFEComponentPowerFlow)(method_result) if method_result else None

    def results_for_mass_disc(self, design_entity: '_1981.MassDisc') -> '_3263.MassDiscPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.MassDiscPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3263.MassDiscPowerFlow)(method_result) if method_result else None

    def results_for_mass_disc_load_case(self, design_entity_analysis: '_6125.MassDiscLoadCase') -> '_3263.MassDiscPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MassDiscLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.MassDiscPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3263.MassDiscPowerFlow)(method_result) if method_result else None

    def results_for_measurement_component(self, design_entity: '_1982.MeasurementComponent') -> '_3264.MeasurementComponentPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.MeasurementComponentPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3264.MeasurementComponentPowerFlow)(method_result) if method_result else None

    def results_for_measurement_component_load_case(self, design_entity_analysis: '_6126.MeasurementComponentLoadCase') -> '_3264.MeasurementComponentPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MeasurementComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.MeasurementComponentPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3264.MeasurementComponentPowerFlow)(method_result) if method_result else None

    def results_for_mountable_component(self, design_entity: '_1983.MountableComponent') -> '_3265.MountableComponentPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.MountableComponentPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3265.MountableComponentPowerFlow)(method_result) if method_result else None

    def results_for_mountable_component_load_case(self, design_entity_analysis: '_6128.MountableComponentLoadCase') -> '_3265.MountableComponentPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MountableComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.MountableComponentPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3265.MountableComponentPowerFlow)(method_result) if method_result else None

    def results_for_oil_seal(self, design_entity: '_1985.OilSeal') -> '_3266.OilSealPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.OilSealPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3266.OilSealPowerFlow)(method_result) if method_result else None

    def results_for_oil_seal_load_case(self, design_entity_analysis: '_6130.OilSealLoadCase') -> '_3266.OilSealPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.OilSealLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.OilSealPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3266.OilSealPowerFlow)(method_result) if method_result else None

    def results_for_part(self, design_entity: '_1986.Part') -> '_3267.PartPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Part)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PartPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3267.PartPowerFlow)(method_result) if method_result else None

    def results_for_part_load_case(self, design_entity_analysis: '_6132.PartLoadCase') -> '_3267.PartPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PartPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3267.PartPowerFlow)(method_result) if method_result else None

    def results_for_planet_carrier(self, design_entity: '_1987.PlanetCarrier') -> '_3273.PlanetCarrierPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PlanetCarrierPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3273.PlanetCarrierPowerFlow)(method_result) if method_result else None

    def results_for_planet_carrier_load_case(self, design_entity_analysis: '_6139.PlanetCarrierLoadCase') -> '_3273.PlanetCarrierPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetCarrierLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PlanetCarrierPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3273.PlanetCarrierPowerFlow)(method_result) if method_result else None

    def results_for_point_load(self, design_entity: '_1989.PointLoad') -> '_3274.PointLoadPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PointLoadPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3274.PointLoadPowerFlow)(method_result) if method_result else None

    def results_for_point_load_load_case(self, design_entity_analysis: '_6142.PointLoadLoadCase') -> '_3274.PointLoadPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PointLoadLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PointLoadPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3274.PointLoadPowerFlow)(method_result) if method_result else None

    def results_for_power_load(self, design_entity: '_1990.PowerLoad') -> '_3277.PowerLoadPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PowerLoadPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3277.PowerLoadPowerFlow)(method_result) if method_result else None

    def results_for_power_load_load_case(self, design_entity_analysis: '_6143.PowerLoadLoadCase') -> '_3277.PowerLoadPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PowerLoadLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PowerLoadPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3277.PowerLoadPowerFlow)(method_result) if method_result else None

    def results_for_root_assembly(self, design_entity: '_1992.RootAssembly') -> '_3282.RootAssemblyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.RootAssemblyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3282.RootAssemblyPowerFlow)(method_result) if method_result else None

    def results_for_root_assembly_load_case(self, design_entity_analysis: '_6149.RootAssemblyLoadCase') -> '_3282.RootAssemblyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RootAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.RootAssemblyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3282.RootAssemblyPowerFlow)(method_result) if method_result else None

    def results_for_specialised_assembly(self, design_entity: '_1994.SpecialisedAssembly') -> '_3286.SpecialisedAssemblyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SpecialisedAssemblyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3286.SpecialisedAssemblyPowerFlow)(method_result) if method_result else None

    def results_for_specialised_assembly_load_case(self, design_entity_analysis: '_6153.SpecialisedAssemblyLoadCase') -> '_3286.SpecialisedAssemblyPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpecialisedAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SpecialisedAssemblyPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3286.SpecialisedAssemblyPowerFlow)(method_result) if method_result else None

    def results_for_unbalanced_mass(self, design_entity: '_1995.UnbalancedMass') -> '_3310.UnbalancedMassPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.UnbalancedMassPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3310.UnbalancedMassPowerFlow)(method_result) if method_result else None

    def results_for_unbalanced_mass_load_case(self, design_entity_analysis: '_6184.UnbalancedMassLoadCase') -> '_3310.UnbalancedMassPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.UnbalancedMassLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.UnbalancedMassPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3310.UnbalancedMassPowerFlow)(method_result) if method_result else None

    def results_for_virtual_component(self, design_entity: '_1996.VirtualComponent') -> '_3311.VirtualComponentPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.VirtualComponentPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3311.VirtualComponentPowerFlow)(method_result) if method_result else None

    def results_for_virtual_component_load_case(self, design_entity_analysis: '_6185.VirtualComponentLoadCase') -> '_3311.VirtualComponentPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.VirtualComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.VirtualComponentPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3311.VirtualComponentPowerFlow)(method_result) if method_result else None

    def results_for_shaft(self, design_entity: '_1999.Shaft') -> '_3284.ShaftPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ShaftPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3284.ShaftPowerFlow)(method_result) if method_result else None

    def results_for_shaft_load_case(self, design_entity_analysis: '_6151.ShaftLoadCase') -> '_3284.ShaftPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ShaftPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3284.ShaftPowerFlow)(method_result) if method_result else None

    def results_for_concept_gear(self, design_entity: '_2037.ConceptGear') -> '_3221.ConceptGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConceptGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3221.ConceptGearPowerFlow)(method_result) if method_result else None

    def results_for_concept_gear_load_case(self, design_entity_analysis: '_6052.ConceptGearLoadCase') -> '_3221.ConceptGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConceptGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3221.ConceptGearPowerFlow)(method_result) if method_result else None

    def results_for_concept_gear_set(self, design_entity: '_2038.ConceptGearSet') -> '_3222.ConceptGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConceptGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3222.ConceptGearSetPowerFlow)(method_result) if method_result else None

    def results_for_concept_gear_set_load_case(self, design_entity_analysis: '_6054.ConceptGearSetLoadCase') -> '_3222.ConceptGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConceptGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3222.ConceptGearSetPowerFlow)(method_result) if method_result else None

    def results_for_face_gear(self, design_entity: '_2044.FaceGear') -> '_3242.FaceGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.FaceGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3242.FaceGearPowerFlow)(method_result) if method_result else None

    def results_for_face_gear_load_case(self, design_entity_analysis: '_6090.FaceGearLoadCase') -> '_3242.FaceGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.FaceGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3242.FaceGearPowerFlow)(method_result) if method_result else None

    def results_for_face_gear_set(self, design_entity: '_2045.FaceGearSet') -> '_3243.FaceGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.FaceGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3243.FaceGearSetPowerFlow)(method_result) if method_result else None

    def results_for_face_gear_set_load_case(self, design_entity_analysis: '_6092.FaceGearSetLoadCase') -> '_3243.FaceGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.FaceGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3243.FaceGearSetPowerFlow)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear(self, design_entity: '_2029.AGMAGleasonConicalGear') -> '_3196.AGMAGleasonConicalGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.AGMAGleasonConicalGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3196.AGMAGleasonConicalGearPowerFlow)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_load_case(self, design_entity_analysis: '_6026.AGMAGleasonConicalGearLoadCase') -> '_3196.AGMAGleasonConicalGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.AGMAGleasonConicalGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3196.AGMAGleasonConicalGearPowerFlow)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_set(self, design_entity: '_2030.AGMAGleasonConicalGearSet') -> '_3197.AGMAGleasonConicalGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.AGMAGleasonConicalGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3197.AGMAGleasonConicalGearSetPowerFlow)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_set_load_case(self, design_entity_analysis: '_6028.AGMAGleasonConicalGearSetLoadCase') -> '_3197.AGMAGleasonConicalGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.AGMAGleasonConicalGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3197.AGMAGleasonConicalGearSetPowerFlow)(method_result) if method_result else None

    def results_for_bevel_differential_gear(self, design_entity: '_2031.BevelDifferentialGear') -> '_3203.BevelDifferentialGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelDifferentialGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3203.BevelDifferentialGearPowerFlow)(method_result) if method_result else None

    def results_for_bevel_differential_gear_load_case(self, design_entity_analysis: '_6034.BevelDifferentialGearLoadCase') -> '_3203.BevelDifferentialGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelDifferentialGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3203.BevelDifferentialGearPowerFlow)(method_result) if method_result else None

    def results_for_bevel_differential_gear_set(self, design_entity: '_2032.BevelDifferentialGearSet') -> '_3204.BevelDifferentialGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelDifferentialGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3204.BevelDifferentialGearSetPowerFlow)(method_result) if method_result else None

    def results_for_bevel_differential_gear_set_load_case(self, design_entity_analysis: '_6036.BevelDifferentialGearSetLoadCase') -> '_3204.BevelDifferentialGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelDifferentialGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3204.BevelDifferentialGearSetPowerFlow)(method_result) if method_result else None

    def results_for_bevel_differential_planet_gear(self, design_entity: '_2033.BevelDifferentialPlanetGear') -> '_3205.BevelDifferentialPlanetGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelDifferentialPlanetGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3205.BevelDifferentialPlanetGearPowerFlow)(method_result) if method_result else None

    def results_for_bevel_differential_planet_gear_load_case(self, design_entity_analysis: '_6037.BevelDifferentialPlanetGearLoadCase') -> '_3205.BevelDifferentialPlanetGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelDifferentialPlanetGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3205.BevelDifferentialPlanetGearPowerFlow)(method_result) if method_result else None

    def results_for_bevel_differential_sun_gear(self, design_entity: '_2034.BevelDifferentialSunGear') -> '_3206.BevelDifferentialSunGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelDifferentialSunGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3206.BevelDifferentialSunGearPowerFlow)(method_result) if method_result else None

    def results_for_bevel_differential_sun_gear_load_case(self, design_entity_analysis: '_6038.BevelDifferentialSunGearLoadCase') -> '_3206.BevelDifferentialSunGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialSunGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelDifferentialSunGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3206.BevelDifferentialSunGearPowerFlow)(method_result) if method_result else None

    def results_for_bevel_gear(self, design_entity: '_2035.BevelGear') -> '_3208.BevelGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3208.BevelGearPowerFlow)(method_result) if method_result else None

    def results_for_bevel_gear_load_case(self, design_entity_analysis: '_6039.BevelGearLoadCase') -> '_3208.BevelGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3208.BevelGearPowerFlow)(method_result) if method_result else None

    def results_for_bevel_gear_set(self, design_entity: '_2036.BevelGearSet') -> '_3209.BevelGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3209.BevelGearSetPowerFlow)(method_result) if method_result else None

    def results_for_bevel_gear_set_load_case(self, design_entity_analysis: '_6041.BevelGearSetLoadCase') -> '_3209.BevelGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.BevelGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3209.BevelGearSetPowerFlow)(method_result) if method_result else None

    def results_for_conical_gear(self, design_entity: '_2039.ConicalGear') -> '_3224.ConicalGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConicalGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3224.ConicalGearPowerFlow)(method_result) if method_result else None

    def results_for_conical_gear_load_case(self, design_entity_analysis: '_6055.ConicalGearLoadCase') -> '_3224.ConicalGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConicalGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3224.ConicalGearPowerFlow)(method_result) if method_result else None

    def results_for_conical_gear_set(self, design_entity: '_2040.ConicalGearSet') -> '_3225.ConicalGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConicalGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3225.ConicalGearSetPowerFlow)(method_result) if method_result else None

    def results_for_conical_gear_set_load_case(self, design_entity_analysis: '_6059.ConicalGearSetLoadCase') -> '_3225.ConicalGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.ConicalGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3225.ConicalGearSetPowerFlow)(method_result) if method_result else None

    def results_for_cylindrical_gear(self, design_entity: '_2041.CylindricalGear') -> '_3236.CylindricalGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CylindricalGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3236.CylindricalGearPowerFlow)(method_result) if method_result else None

    def results_for_cylindrical_gear_load_case(self, design_entity_analysis: '_6068.CylindricalGearLoadCase') -> '_3236.CylindricalGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CylindricalGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3236.CylindricalGearPowerFlow)(method_result) if method_result else None

    def results_for_cylindrical_gear_set(self, design_entity: '_2042.CylindricalGearSet') -> '_3237.CylindricalGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CylindricalGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3237.CylindricalGearSetPowerFlow)(method_result) if method_result else None

    def results_for_cylindrical_gear_set_load_case(self, design_entity_analysis: '_6072.CylindricalGearSetLoadCase') -> '_3237.CylindricalGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CylindricalGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3237.CylindricalGearSetPowerFlow)(method_result) if method_result else None

    def results_for_cylindrical_planet_gear(self, design_entity: '_2043.CylindricalPlanetGear') -> '_3238.CylindricalPlanetGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CylindricalPlanetGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3238.CylindricalPlanetGearPowerFlow)(method_result) if method_result else None

    def results_for_cylindrical_planet_gear_load_case(self, design_entity_analysis: '_6073.CylindricalPlanetGearLoadCase') -> '_3238.CylindricalPlanetGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.CylindricalPlanetGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3238.CylindricalPlanetGearPowerFlow)(method_result) if method_result else None

    def results_for_gear(self, design_entity: '_2046.Gear') -> '_3246.GearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.GearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3246.GearPowerFlow)(method_result) if method_result else None

    def results_for_gear_load_case(self, design_entity_analysis: '_6095.GearLoadCase') -> '_3246.GearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.GearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3246.GearPowerFlow)(method_result) if method_result else None

    def results_for_gear_set(self, design_entity: '_2048.GearSet') -> '_3247.GearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.GearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3247.GearSetPowerFlow)(method_result) if method_result else None

    def results_for_gear_set_load_case(self, design_entity_analysis: '_6100.GearSetLoadCase') -> '_3247.GearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.GearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3247.GearSetPowerFlow)(method_result) if method_result else None

    def results_for_hypoid_gear(self, design_entity: '_2050.HypoidGear') -> '_3250.HypoidGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.HypoidGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3250.HypoidGearPowerFlow)(method_result) if method_result else None

    def results_for_hypoid_gear_load_case(self, design_entity_analysis: '_6110.HypoidGearLoadCase') -> '_3250.HypoidGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.HypoidGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3250.HypoidGearPowerFlow)(method_result) if method_result else None

    def results_for_hypoid_gear_set(self, design_entity: '_2051.HypoidGearSet') -> '_3251.HypoidGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.HypoidGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3251.HypoidGearSetPowerFlow)(method_result) if method_result else None

    def results_for_hypoid_gear_set_load_case(self, design_entity_analysis: '_6112.HypoidGearSetLoadCase') -> '_3251.HypoidGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.HypoidGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3251.HypoidGearSetPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear(self, design_entity: '_2052.KlingelnbergCycloPalloidConicalGear') -> '_3255.KlingelnbergCycloPalloidConicalGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidConicalGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3255.KlingelnbergCycloPalloidConicalGearPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_load_case(self, design_entity_analysis: '_6116.KlingelnbergCycloPalloidConicalGearLoadCase') -> '_3255.KlingelnbergCycloPalloidConicalGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidConicalGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3255.KlingelnbergCycloPalloidConicalGearPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set(self, design_entity: '_2053.KlingelnbergCycloPalloidConicalGearSet') -> '_3256.KlingelnbergCycloPalloidConicalGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidConicalGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3256.KlingelnbergCycloPalloidConicalGearSetPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set_load_case(self, design_entity_analysis: '_6118.KlingelnbergCycloPalloidConicalGearSetLoadCase') -> '_3256.KlingelnbergCycloPalloidConicalGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidConicalGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3256.KlingelnbergCycloPalloidConicalGearSetPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear(self, design_entity: '_2054.KlingelnbergCycloPalloidHypoidGear') -> '_3258.KlingelnbergCycloPalloidHypoidGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidHypoidGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3258.KlingelnbergCycloPalloidHypoidGearPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_load_case(self, design_entity_analysis: '_6119.KlingelnbergCycloPalloidHypoidGearLoadCase') -> '_3258.KlingelnbergCycloPalloidHypoidGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidHypoidGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3258.KlingelnbergCycloPalloidHypoidGearPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set(self, design_entity: '_2055.KlingelnbergCycloPalloidHypoidGearSet') -> '_3259.KlingelnbergCycloPalloidHypoidGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidHypoidGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3259.KlingelnbergCycloPalloidHypoidGearSetPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set_load_case(self, design_entity_analysis: '_6121.KlingelnbergCycloPalloidHypoidGearSetLoadCase') -> '_3259.KlingelnbergCycloPalloidHypoidGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidHypoidGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3259.KlingelnbergCycloPalloidHypoidGearSetPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, design_entity: '_2056.KlingelnbergCycloPalloidSpiralBevelGear') -> '_3261.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3261.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_load_case(self, design_entity_analysis: '_6122.KlingelnbergCycloPalloidSpiralBevelGearLoadCase') -> '_3261.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3261.KlingelnbergCycloPalloidSpiralBevelGearPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, design_entity: '_2057.KlingelnbergCycloPalloidSpiralBevelGearSet') -> '_3262.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3262.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_load_case(self, design_entity_analysis: '_6124.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase') -> '_3262.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3262.KlingelnbergCycloPalloidSpiralBevelGearSetPowerFlow)(method_result) if method_result else None

    def results_for_planetary_gear_set(self, design_entity: '_2058.PlanetaryGearSet') -> '_3272.PlanetaryGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PlanetaryGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3272.PlanetaryGearSetPowerFlow)(method_result) if method_result else None

    def results_for_planetary_gear_set_load_case(self, design_entity_analysis: '_6137.PlanetaryGearSetLoadCase') -> '_3272.PlanetaryGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetaryGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.PlanetaryGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3272.PlanetaryGearSetPowerFlow)(method_result) if method_result else None

    def results_for_spiral_bevel_gear(self, design_entity: '_2059.SpiralBevelGear') -> '_3288.SpiralBevelGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SpiralBevelGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3288.SpiralBevelGearPowerFlow)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_load_case(self, design_entity_analysis: '_6155.SpiralBevelGearLoadCase') -> '_3288.SpiralBevelGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SpiralBevelGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3288.SpiralBevelGearPowerFlow)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_set(self, design_entity: '_2060.SpiralBevelGearSet') -> '_3289.SpiralBevelGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SpiralBevelGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3289.SpiralBevelGearSetPowerFlow)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_set_load_case(self, design_entity_analysis: '_6157.SpiralBevelGearSetLoadCase') -> '_3289.SpiralBevelGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.SpiralBevelGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3289.SpiralBevelGearSetPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear(self, design_entity: '_2061.StraightBevelDiffGear') -> '_3294.StraightBevelDiffGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelDiffGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3294.StraightBevelDiffGearPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_load_case(self, design_entity_analysis: '_6162.StraightBevelDiffGearLoadCase') -> '_3294.StraightBevelDiffGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelDiffGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3294.StraightBevelDiffGearPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_set(self, design_entity: '_2062.StraightBevelDiffGearSet') -> '_3295.StraightBevelDiffGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelDiffGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3295.StraightBevelDiffGearSetPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_set_load_case(self, design_entity_analysis: '_6164.StraightBevelDiffGearSetLoadCase') -> '_3295.StraightBevelDiffGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelDiffGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3295.StraightBevelDiffGearSetPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_gear(self, design_entity: '_2063.StraightBevelGear') -> '_3297.StraightBevelGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3297.StraightBevelGearPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_gear_load_case(self, design_entity_analysis: '_6165.StraightBevelGearLoadCase') -> '_3297.StraightBevelGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3297.StraightBevelGearPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_gear_set(self, design_entity: '_2064.StraightBevelGearSet') -> '_3298.StraightBevelGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3298.StraightBevelGearSetPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_gear_set_load_case(self, design_entity_analysis: '_6167.StraightBevelGearSetLoadCase') -> '_3298.StraightBevelGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3298.StraightBevelGearSetPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_planet_gear(self, design_entity: '_2065.StraightBevelPlanetGear') -> '_3299.StraightBevelPlanetGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelPlanetGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3299.StraightBevelPlanetGearPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_planet_gear_load_case(self, design_entity_analysis: '_6168.StraightBevelPlanetGearLoadCase') -> '_3299.StraightBevelPlanetGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelPlanetGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3299.StraightBevelPlanetGearPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_sun_gear(self, design_entity: '_2066.StraightBevelSunGear') -> '_3300.StraightBevelSunGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelSunGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3300.StraightBevelSunGearPowerFlow)(method_result) if method_result else None

    def results_for_straight_bevel_sun_gear_load_case(self, design_entity_analysis: '_6169.StraightBevelSunGearLoadCase') -> '_3300.StraightBevelSunGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelSunGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.StraightBevelSunGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3300.StraightBevelSunGearPowerFlow)(method_result) if method_result else None

    def results_for_worm_gear(self, design_entity: '_2067.WormGear') -> '_3313.WormGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.WormGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3313.WormGearPowerFlow)(method_result) if method_result else None

    def results_for_worm_gear_load_case(self, design_entity_analysis: '_6186.WormGearLoadCase') -> '_3313.WormGearPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.WormGearPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3313.WormGearPowerFlow)(method_result) if method_result else None

    def results_for_worm_gear_set(self, design_entity: '_2068.WormGearSet') -> '_3314.WormGearSetPowerFlow':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.power_flows.WormGearSetPowerFlow
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3314.WormGearSetPowerFlow)(method_result) if method_result else None
