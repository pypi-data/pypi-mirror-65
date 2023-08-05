'''_2147.py

ParametricStudyToolAnalysis
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
from mastapy.system_model.analyses_and_results.parametric_study_tools import (
    _3573, _3575, _3576, _3532,
    _3531, _3448, _3461, _3460,
    _3466, _3465, _3477, _3476,
    _3479, _3480, _3538, _3543,
    _3541, _3539, _3552, _3551,
    _3562, _3561, _3563, _3564,
    _3566, _3567, _3568, _3478,
    _3447, _3462, _3473, _3505,
    _3533, _3540, _3545, _3449,
    _3467, _3493, _3553, _3454,
    _3470, _3442, _3481, _3501,
    _3506, _3509, _3512, _3547,
    _3556, _3571, _3574, _3497,
    _3530, _3459, _3464, _3475,
    _3550, _3565, _3440, _3441,
    _3446, _3458, _3457, _3463,
    _3474, _3485, _3492, _3496,
    _3445, _3500, _3504, _3515,
    _3516, _3518, _3519, _3529,
    _3535, _3536, _3537, _3542,
    _3546, _3569, _3570, _3544,
    _3468, _3469, _3494, _3495,
    _3443, _3444, _3450, _3451,
    _3452, _3453, _3455, _3456,
    _3471, _3472, _3482, _3483,
    _3484, _3498, _3499, _3502,
    _3503, _3507, _3508, _3510,
    _3511, _3513, _3514, _3534,
    _3548, _3549, _3554, _3555,
    _3557, _3558, _3559, _3560,
    _3572
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

_PARAMETRIC_STUDY_TOOL_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'ParametricStudyToolAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('ParametricStudyToolAnalysis',)


class ParametricStudyToolAnalysis(_2130.SingleAnalysis):
    '''ParametricStudyToolAnalysis

    This is a mastapy class.
    '''

    TYPE = _PARAMETRIC_STUDY_TOOL_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ParametricStudyToolAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    def results_for_worm_gear_set_load_case(self, design_entity_analysis: '_6188.WormGearSetLoadCase') -> '_3573.WormGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.WormGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3573.WormGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_zerol_bevel_gear(self, design_entity: '_2069.ZerolBevelGear') -> '_3575.ZerolBevelGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ZerolBevelGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3575.ZerolBevelGearParametricStudyTool)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_load_case(self, design_entity_analysis: '_6189.ZerolBevelGearLoadCase') -> '_3575.ZerolBevelGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ZerolBevelGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3575.ZerolBevelGearParametricStudyTool)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_set(self, design_entity: '_2070.ZerolBevelGearSet') -> '_3576.ZerolBevelGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ZerolBevelGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3576.ZerolBevelGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_set_load_case(self, design_entity_analysis: '_6191.ZerolBevelGearSetLoadCase') -> '_3576.ZerolBevelGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ZerolBevelGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3576.ZerolBevelGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling(self, design_entity: '_2099.PartToPartShearCoupling') -> '_3532.PartToPartShearCouplingParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCoupling)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.PartToPartShearCouplingParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3532.PartToPartShearCouplingParametricStudyTool)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_load_case(self, design_entity_analysis: '_6135.PartToPartShearCouplingLoadCase') -> '_3532.PartToPartShearCouplingParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.PartToPartShearCouplingParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3532.PartToPartShearCouplingParametricStudyTool)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_half(self, design_entity: '_2100.PartToPartShearCouplingHalf') -> '_3531.PartToPartShearCouplingHalfParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.PartToPartShearCouplingHalfParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3531.PartToPartShearCouplingHalfParametricStudyTool)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_half_load_case(self, design_entity_analysis: '_6134.PartToPartShearCouplingHalfLoadCase') -> '_3531.PartToPartShearCouplingHalfParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.PartToPartShearCouplingHalfParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3531.PartToPartShearCouplingHalfParametricStudyTool)(method_result) if method_result else None

    def results_for_belt_drive(self, design_entity: '_2088.BeltDrive') -> '_3448.BeltDriveParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BeltDriveParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3448.BeltDriveParametricStudyTool)(method_result) if method_result else None

    def results_for_belt_drive_load_case(self, design_entity_analysis: '_6033.BeltDriveLoadCase') -> '_3448.BeltDriveParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BeltDriveLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BeltDriveParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3448.BeltDriveParametricStudyTool)(method_result) if method_result else None

    def results_for_clutch(self, design_entity: '_2090.Clutch') -> '_3461.ClutchParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ClutchParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3461.ClutchParametricStudyTool)(method_result) if method_result else None

    def results_for_clutch_load_case(self, design_entity_analysis: '_6046.ClutchLoadCase') -> '_3461.ClutchParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ClutchParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3461.ClutchParametricStudyTool)(method_result) if method_result else None

    def results_for_clutch_half(self, design_entity: '_2091.ClutchHalf') -> '_3460.ClutchHalfParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ClutchHalfParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3460.ClutchHalfParametricStudyTool)(method_result) if method_result else None

    def results_for_clutch_half_load_case(self, design_entity_analysis: '_6045.ClutchHalfLoadCase') -> '_3460.ClutchHalfParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ClutchHalfParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3460.ClutchHalfParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_coupling(self, design_entity: '_2093.ConceptCoupling') -> '_3466.ConceptCouplingParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ConceptCouplingParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3466.ConceptCouplingParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_coupling_load_case(self, design_entity_analysis: '_6051.ConceptCouplingLoadCase') -> '_3466.ConceptCouplingParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ConceptCouplingParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3466.ConceptCouplingParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_coupling_half(self, design_entity: '_2094.ConceptCouplingHalf') -> '_3465.ConceptCouplingHalfParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ConceptCouplingHalfParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3465.ConceptCouplingHalfParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_coupling_half_load_case(self, design_entity_analysis: '_6050.ConceptCouplingHalfLoadCase') -> '_3465.ConceptCouplingHalfParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ConceptCouplingHalfParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3465.ConceptCouplingHalfParametricStudyTool)(method_result) if method_result else None

    def results_for_coupling(self, design_entity: '_2095.Coupling') -> '_3477.CouplingParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.CouplingParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3477.CouplingParametricStudyTool)(method_result) if method_result else None

    def results_for_coupling_load_case(self, design_entity_analysis: '_6064.CouplingLoadCase') -> '_3477.CouplingParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.CouplingParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3477.CouplingParametricStudyTool)(method_result) if method_result else None

    def results_for_coupling_half(self, design_entity: '_2096.CouplingHalf') -> '_3476.CouplingHalfParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.CouplingHalfParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3476.CouplingHalfParametricStudyTool)(method_result) if method_result else None

    def results_for_coupling_half_load_case(self, design_entity_analysis: '_6063.CouplingHalfLoadCase') -> '_3476.CouplingHalfParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.CouplingHalfParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3476.CouplingHalfParametricStudyTool)(method_result) if method_result else None

    def results_for_cvt(self, design_entity: '_2097.CVT') -> '_3479.CVTParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.CVTParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3479.CVTParametricStudyTool)(method_result) if method_result else None

    def results_for_cvt_load_case(self, design_entity_analysis: '_6066.CVTLoadCase') -> '_3479.CVTParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.CVTParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3479.CVTParametricStudyTool)(method_result) if method_result else None

    def results_for_cvt_pulley(self, design_entity: '_2098.CVTPulley') -> '_3480.CVTPulleyParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.CVTPulleyParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3480.CVTPulleyParametricStudyTool)(method_result) if method_result else None

    def results_for_cvt_pulley_load_case(self, design_entity_analysis: '_6067.CVTPulleyLoadCase') -> '_3480.CVTPulleyParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTPulleyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.CVTPulleyParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3480.CVTPulleyParametricStudyTool)(method_result) if method_result else None

    def results_for_pulley(self, design_entity: '_2101.Pulley') -> '_3538.PulleyParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.PulleyParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3538.PulleyParametricStudyTool)(method_result) if method_result else None

    def results_for_pulley_load_case(self, design_entity_analysis: '_6144.PulleyLoadCase') -> '_3538.PulleyParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PulleyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.PulleyParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3538.PulleyParametricStudyTool)(method_result) if method_result else None

    def results_for_shaft_hub_connection(self, design_entity: '_2109.ShaftHubConnection') -> '_3543.ShaftHubConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ShaftHubConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3543.ShaftHubConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_shaft_hub_connection_load_case(self, design_entity_analysis: '_6150.ShaftHubConnectionLoadCase') -> '_3543.ShaftHubConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftHubConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ShaftHubConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3543.ShaftHubConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_rolling_ring(self, design_entity: '_2107.RollingRing') -> '_3541.RollingRingParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.RollingRingParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3541.RollingRingParametricStudyTool)(method_result) if method_result else None

    def results_for_rolling_ring_load_case(self, design_entity_analysis: '_6148.RollingRingLoadCase') -> '_3541.RollingRingParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.RollingRingParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3541.RollingRingParametricStudyTool)(method_result) if method_result else None

    def results_for_rolling_ring_assembly(self, design_entity: '_2108.RollingRingAssembly') -> '_3539.RollingRingAssemblyParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.RollingRingAssemblyParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3539.RollingRingAssemblyParametricStudyTool)(method_result) if method_result else None

    def results_for_rolling_ring_assembly_load_case(self, design_entity_analysis: '_6146.RollingRingAssemblyLoadCase') -> '_3539.RollingRingAssemblyParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.RollingRingAssemblyParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3539.RollingRingAssemblyParametricStudyTool)(method_result) if method_result else None

    def results_for_spring_damper(self, design_entity: '_2110.SpringDamper') -> '_3552.SpringDamperParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.SpringDamperParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3552.SpringDamperParametricStudyTool)(method_result) if method_result else None

    def results_for_spring_damper_load_case(self, design_entity_analysis: '_6160.SpringDamperLoadCase') -> '_3552.SpringDamperParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.SpringDamperParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3552.SpringDamperParametricStudyTool)(method_result) if method_result else None

    def results_for_spring_damper_half(self, design_entity: '_2111.SpringDamperHalf') -> '_3551.SpringDamperHalfParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.SpringDamperHalfParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3551.SpringDamperHalfParametricStudyTool)(method_result) if method_result else None

    def results_for_spring_damper_half_load_case(self, design_entity_analysis: '_6159.SpringDamperHalfLoadCase') -> '_3551.SpringDamperHalfParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.SpringDamperHalfParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3551.SpringDamperHalfParametricStudyTool)(method_result) if method_result else None

    def results_for_synchroniser(self, design_entity: '_2112.Synchroniser') -> '_3562.SynchroniserParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.SynchroniserParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3562.SynchroniserParametricStudyTool)(method_result) if method_result else None

    def results_for_synchroniser_load_case(self, design_entity_analysis: '_6171.SynchroniserLoadCase') -> '_3562.SynchroniserParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.SynchroniserParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3562.SynchroniserParametricStudyTool)(method_result) if method_result else None

    def results_for_synchroniser_half(self, design_entity: '_2114.SynchroniserHalf') -> '_3561.SynchroniserHalfParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.SynchroniserHalfParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3561.SynchroniserHalfParametricStudyTool)(method_result) if method_result else None

    def results_for_synchroniser_half_load_case(self, design_entity_analysis: '_6170.SynchroniserHalfLoadCase') -> '_3561.SynchroniserHalfParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.SynchroniserHalfParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3561.SynchroniserHalfParametricStudyTool)(method_result) if method_result else None

    def results_for_synchroniser_part(self, design_entity: '_2115.SynchroniserPart') -> '_3563.SynchroniserPartParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.SynchroniserPartParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3563.SynchroniserPartParametricStudyTool)(method_result) if method_result else None

    def results_for_synchroniser_part_load_case(self, design_entity_analysis: '_6172.SynchroniserPartLoadCase') -> '_3563.SynchroniserPartParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserPartLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.SynchroniserPartParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3563.SynchroniserPartParametricStudyTool)(method_result) if method_result else None

    def results_for_synchroniser_sleeve(self, design_entity: '_2116.SynchroniserSleeve') -> '_3564.SynchroniserSleeveParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.SynchroniserSleeveParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3564.SynchroniserSleeveParametricStudyTool)(method_result) if method_result else None

    def results_for_synchroniser_sleeve_load_case(self, design_entity_analysis: '_6173.SynchroniserSleeveLoadCase') -> '_3564.SynchroniserSleeveParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserSleeveLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.SynchroniserSleeveParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3564.SynchroniserSleeveParametricStudyTool)(method_result) if method_result else None

    def results_for_torque_converter(self, design_entity: '_2117.TorqueConverter') -> '_3566.TorqueConverterParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.TorqueConverterParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3566.TorqueConverterParametricStudyTool)(method_result) if method_result else None

    def results_for_torque_converter_load_case(self, design_entity_analysis: '_6177.TorqueConverterLoadCase') -> '_3566.TorqueConverterParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.TorqueConverterParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3566.TorqueConverterParametricStudyTool)(method_result) if method_result else None

    def results_for_torque_converter_pump(self, design_entity: '_2118.TorqueConverterPump') -> '_3567.TorqueConverterPumpParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.TorqueConverterPumpParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3567.TorqueConverterPumpParametricStudyTool)(method_result) if method_result else None

    def results_for_torque_converter_pump_load_case(self, design_entity_analysis: '_6178.TorqueConverterPumpLoadCase') -> '_3567.TorqueConverterPumpParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterPumpLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.TorqueConverterPumpParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3567.TorqueConverterPumpParametricStudyTool)(method_result) if method_result else None

    def results_for_torque_converter_turbine(self, design_entity: '_2120.TorqueConverterTurbine') -> '_3568.TorqueConverterTurbineParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.TorqueConverterTurbineParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3568.TorqueConverterTurbineParametricStudyTool)(method_result) if method_result else None

    def results_for_torque_converter_turbine_load_case(self, design_entity_analysis: '_6179.TorqueConverterTurbineLoadCase') -> '_3568.TorqueConverterTurbineParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterTurbineLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.TorqueConverterTurbineParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3568.TorqueConverterTurbineParametricStudyTool)(method_result) if method_result else None

    def results_for_cvt_belt_connection(self, design_entity: '_1815.CVTBeltConnection') -> '_3478.CVTBeltConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.CVTBeltConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3478.CVTBeltConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_cvt_belt_connection_load_case(self, design_entity_analysis: '_6065.CVTBeltConnectionLoadCase') -> '_3478.CVTBeltConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTBeltConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.CVTBeltConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3478.CVTBeltConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_belt_connection(self, design_entity: '_1810.BeltConnection') -> '_3447.BeltConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BeltConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3447.BeltConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_belt_connection_load_case(self, design_entity_analysis: '_6032.BeltConnectionLoadCase') -> '_3447.BeltConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BeltConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BeltConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3447.BeltConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_coaxial_connection(self, design_entity: '_1811.CoaxialConnection') -> '_3462.CoaxialConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.CoaxialConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3462.CoaxialConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_coaxial_connection_load_case(self, design_entity_analysis: '_6047.CoaxialConnectionLoadCase') -> '_3462.CoaxialConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CoaxialConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.CoaxialConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3462.CoaxialConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_connection(self, design_entity: '_1814.Connection') -> '_3473.ConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3473.ConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_connection_load_case(self, design_entity_analysis: '_6060.ConnectionLoadCase') -> '_3473.ConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3473.ConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_inter_mountable_component_connection(self, design_entity: '_1823.InterMountableComponentConnection') -> '_3505.InterMountableComponentConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.InterMountableComponentConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3505.InterMountableComponentConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_inter_mountable_component_connection_load_case(self, design_entity_analysis: '_6115.InterMountableComponentConnectionLoadCase') -> '_3505.InterMountableComponentConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.InterMountableComponentConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.InterMountableComponentConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3505.InterMountableComponentConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_planetary_connection(self, design_entity: '_1826.PlanetaryConnection') -> '_3533.PlanetaryConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.PlanetaryConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3533.PlanetaryConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_planetary_connection_load_case(self, design_entity_analysis: '_6136.PlanetaryConnectionLoadCase') -> '_3533.PlanetaryConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetaryConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.PlanetaryConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3533.PlanetaryConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_rolling_ring_connection(self, design_entity: '_1830.RollingRingConnection') -> '_3540.RollingRingConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.RollingRingConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3540.RollingRingConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_rolling_ring_connection_load_case(self, design_entity_analysis: '_6147.RollingRingConnectionLoadCase') -> '_3540.RollingRingConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.RollingRingConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3540.RollingRingConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_shaft_to_mountable_component_connection(self, design_entity: '_1834.ShaftToMountableComponentConnection') -> '_3545.ShaftToMountableComponentConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ShaftToMountableComponentConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3545.ShaftToMountableComponentConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_shaft_to_mountable_component_connection_load_case(self, design_entity_analysis: '_6152.ShaftToMountableComponentConnectionLoadCase') -> '_3545.ShaftToMountableComponentConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftToMountableComponentConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ShaftToMountableComponentConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3545.ShaftToMountableComponentConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_differential_gear_mesh(self, design_entity: '_1840.BevelDifferentialGearMesh') -> '_3449.BevelDifferentialGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BevelDifferentialGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3449.BevelDifferentialGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_differential_gear_mesh_load_case(self, design_entity_analysis: '_6035.BevelDifferentialGearMeshLoadCase') -> '_3449.BevelDifferentialGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BevelDifferentialGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3449.BevelDifferentialGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_gear_mesh(self, design_entity: '_1844.ConceptGearMesh') -> '_3467.ConceptGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ConceptGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3467.ConceptGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_gear_mesh_load_case(self, design_entity_analysis: '_6053.ConceptGearMeshLoadCase') -> '_3467.ConceptGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ConceptGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3467.ConceptGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_face_gear_mesh(self, design_entity: '_1850.FaceGearMesh') -> '_3493.FaceGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.FaceGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3493.FaceGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_face_gear_mesh_load_case(self, design_entity_analysis: '_6091.FaceGearMeshLoadCase') -> '_3493.FaceGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.FaceGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3493.FaceGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_mesh(self, design_entity: '_1864.StraightBevelDiffGearMesh') -> '_3553.StraightBevelDiffGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelDiffGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3553.StraightBevelDiffGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_mesh_load_case(self, design_entity_analysis: '_6163.StraightBevelDiffGearMeshLoadCase') -> '_3553.StraightBevelDiffGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelDiffGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3553.StraightBevelDiffGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_gear_mesh(self, design_entity: '_1842.BevelGearMesh') -> '_3454.BevelGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BevelGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3454.BevelGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6040.BevelGearMeshLoadCase') -> '_3454.BevelGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BevelGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3454.BevelGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_conical_gear_mesh(self, design_entity: '_1846.ConicalGearMesh') -> '_3470.ConicalGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ConicalGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3470.ConicalGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_conical_gear_mesh_load_case(self, design_entity_analysis: '_6057.ConicalGearMeshLoadCase') -> '_3470.ConicalGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ConicalGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3470.ConicalGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_mesh(self, design_entity: '_1838.AGMAGleasonConicalGearMesh') -> '_3442.AGMAGleasonConicalGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.AGMAGleasonConicalGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3442.AGMAGleasonConicalGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_mesh_load_case(self, design_entity_analysis: '_6027.AGMAGleasonConicalGearMeshLoadCase') -> '_3442.AGMAGleasonConicalGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.AGMAGleasonConicalGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3442.AGMAGleasonConicalGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_cylindrical_gear_mesh(self, design_entity: '_1848.CylindricalGearMesh') -> '_3481.CylindricalGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.CylindricalGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3481.CylindricalGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_cylindrical_gear_mesh_load_case(self, design_entity_analysis: '_6070.CylindricalGearMeshLoadCase') -> '_3481.CylindricalGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.CylindricalGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3481.CylindricalGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_hypoid_gear_mesh(self, design_entity: '_1854.HypoidGearMesh') -> '_3501.HypoidGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.HypoidGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3501.HypoidGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_hypoid_gear_mesh_load_case(self, design_entity_analysis: '_6111.HypoidGearMeshLoadCase') -> '_3501.HypoidGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.HypoidGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3501.HypoidGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh(self, design_entity: '_1857.KlingelnbergCycloPalloidConicalGearMesh') -> '_3506.KlingelnbergCycloPalloidConicalGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidConicalGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3506.KlingelnbergCycloPalloidConicalGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh_load_case(self, design_entity_analysis: '_6117.KlingelnbergCycloPalloidConicalGearMeshLoadCase') -> '_3506.KlingelnbergCycloPalloidConicalGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidConicalGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3506.KlingelnbergCycloPalloidConicalGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, design_entity: '_1858.KlingelnbergCycloPalloidHypoidGearMesh') -> '_3509.KlingelnbergCycloPalloidHypoidGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidHypoidGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3509.KlingelnbergCycloPalloidHypoidGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh_load_case(self, design_entity_analysis: '_6120.KlingelnbergCycloPalloidHypoidGearMeshLoadCase') -> '_3509.KlingelnbergCycloPalloidHypoidGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidHypoidGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3509.KlingelnbergCycloPalloidHypoidGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, design_entity: '_1859.KlingelnbergCycloPalloidSpiralBevelGearMesh') -> '_3512.KlingelnbergCycloPalloidSpiralBevelGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidSpiralBevelGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3512.KlingelnbergCycloPalloidSpiralBevelGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6123.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase') -> '_3512.KlingelnbergCycloPalloidSpiralBevelGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidSpiralBevelGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3512.KlingelnbergCycloPalloidSpiralBevelGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_mesh(self, design_entity: '_1862.SpiralBevelGearMesh') -> '_3547.SpiralBevelGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.SpiralBevelGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3547.SpiralBevelGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6156.SpiralBevelGearMeshLoadCase') -> '_3547.SpiralBevelGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.SpiralBevelGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3547.SpiralBevelGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_gear_mesh(self, design_entity: '_1866.StraightBevelGearMesh') -> '_3556.StraightBevelGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3556.StraightBevelGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6166.StraightBevelGearMeshLoadCase') -> '_3556.StraightBevelGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3556.StraightBevelGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_worm_gear_mesh(self, design_entity: '_1868.WormGearMesh') -> '_3571.WormGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.WormGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3571.WormGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_worm_gear_mesh_load_case(self, design_entity_analysis: '_6187.WormGearMeshLoadCase') -> '_3571.WormGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.WormGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3571.WormGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_mesh(self, design_entity: '_1870.ZerolBevelGearMesh') -> '_3574.ZerolBevelGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ZerolBevelGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3574.ZerolBevelGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6190.ZerolBevelGearMeshLoadCase') -> '_3574.ZerolBevelGearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ZerolBevelGearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3574.ZerolBevelGearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_gear_mesh(self, design_entity: '_1852.GearMesh') -> '_3497.GearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.GearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3497.GearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_gear_mesh_load_case(self, design_entity_analysis: '_6097.GearMeshLoadCase') -> '_3497.GearMeshParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.GearMeshParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3497.GearMeshParametricStudyTool)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_connection(self, design_entity: '_1878.PartToPartShearCouplingConnection') -> '_3530.PartToPartShearCouplingConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.PartToPartShearCouplingConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3530.PartToPartShearCouplingConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_connection_load_case(self, design_entity_analysis: '_6133.PartToPartShearCouplingConnectionLoadCase') -> '_3530.PartToPartShearCouplingConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.PartToPartShearCouplingConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3530.PartToPartShearCouplingConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_clutch_connection(self, design_entity: '_1872.ClutchConnection') -> '_3459.ClutchConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ClutchConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3459.ClutchConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_clutch_connection_load_case(self, design_entity_analysis: '_6044.ClutchConnectionLoadCase') -> '_3459.ClutchConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ClutchConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3459.ClutchConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_coupling_connection(self, design_entity: '_1874.ConceptCouplingConnection') -> '_3464.ConceptCouplingConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ConceptCouplingConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3464.ConceptCouplingConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_coupling_connection_load_case(self, design_entity_analysis: '_6049.ConceptCouplingConnectionLoadCase') -> '_3464.ConceptCouplingConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ConceptCouplingConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3464.ConceptCouplingConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_coupling_connection(self, design_entity: '_1876.CouplingConnection') -> '_3475.CouplingConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.CouplingConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3475.CouplingConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_coupling_connection_load_case(self, design_entity_analysis: '_6062.CouplingConnectionLoadCase') -> '_3475.CouplingConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.CouplingConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3475.CouplingConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_spring_damper_connection(self, design_entity: '_1880.SpringDamperConnection') -> '_3550.SpringDamperConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.SpringDamperConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3550.SpringDamperConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_spring_damper_connection_load_case(self, design_entity_analysis: '_6158.SpringDamperConnectionLoadCase') -> '_3550.SpringDamperConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.SpringDamperConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3550.SpringDamperConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_torque_converter_connection(self, design_entity: '_1882.TorqueConverterConnection') -> '_3565.TorqueConverterConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.TorqueConverterConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3565.TorqueConverterConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_torque_converter_connection_load_case(self, design_entity_analysis: '_6176.TorqueConverterConnectionLoadCase') -> '_3565.TorqueConverterConnectionParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.TorqueConverterConnectionParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3565.TorqueConverterConnectionParametricStudyTool)(method_result) if method_result else None

    def results_for_abstract_assembly(self, design_entity: '_1958.AbstractAssembly') -> '_3440.AbstractAssemblyParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.AbstractAssemblyParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3440.AbstractAssemblyParametricStudyTool)(method_result) if method_result else None

    def results_for_abstract_assembly_load_case(self, design_entity_analysis: '_6023.AbstractAssemblyLoadCase') -> '_3440.AbstractAssemblyParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.AbstractAssemblyParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3440.AbstractAssemblyParametricStudyTool)(method_result) if method_result else None

    def results_for_abstract_shaft_or_housing(self, design_entity: '_1959.AbstractShaftOrHousing') -> '_3441.AbstractShaftOrHousingParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.AbstractShaftOrHousingParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3441.AbstractShaftOrHousingParametricStudyTool)(method_result) if method_result else None

    def results_for_abstract_shaft_or_housing_load_case(self, design_entity_analysis: '_6024.AbstractShaftOrHousingLoadCase') -> '_3441.AbstractShaftOrHousingParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractShaftOrHousingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.AbstractShaftOrHousingParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3441.AbstractShaftOrHousingParametricStudyTool)(method_result) if method_result else None

    def results_for_bearing(self, design_entity: '_1962.Bearing') -> '_3446.BearingParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BearingParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3446.BearingParametricStudyTool)(method_result) if method_result else None

    def results_for_bearing_load_case(self, design_entity_analysis: '_6031.BearingLoadCase') -> '_3446.BearingParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BearingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BearingParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3446.BearingParametricStudyTool)(method_result) if method_result else None

    def results_for_bolt(self, design_entity: '_1964.Bolt') -> '_3458.BoltParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BoltParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3458.BoltParametricStudyTool)(method_result) if method_result else None

    def results_for_bolt_load_case(self, design_entity_analysis: '_6043.BoltLoadCase') -> '_3458.BoltParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BoltLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BoltParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3458.BoltParametricStudyTool)(method_result) if method_result else None

    def results_for_bolted_joint(self, design_entity: '_1965.BoltedJoint') -> '_3457.BoltedJointParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BoltedJointParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3457.BoltedJointParametricStudyTool)(method_result) if method_result else None

    def results_for_bolted_joint_load_case(self, design_entity_analysis: '_6042.BoltedJointLoadCase') -> '_3457.BoltedJointParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BoltedJointLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BoltedJointParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3457.BoltedJointParametricStudyTool)(method_result) if method_result else None

    def results_for_component(self, design_entity: '_1966.Component') -> '_3463.ComponentParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ComponentParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3463.ComponentParametricStudyTool)(method_result) if method_result else None

    def results_for_component_load_case(self, design_entity_analysis: '_6048.ComponentLoadCase') -> '_3463.ComponentParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ComponentParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3463.ComponentParametricStudyTool)(method_result) if method_result else None

    def results_for_connector(self, design_entity: '_1969.Connector') -> '_3474.ConnectorParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Connector)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ConnectorParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3474.ConnectorParametricStudyTool)(method_result) if method_result else None

    def results_for_connector_load_case(self, design_entity_analysis: '_6061.ConnectorLoadCase') -> '_3474.ConnectorParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConnectorLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ConnectorParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3474.ConnectorParametricStudyTool)(method_result) if method_result else None

    def results_for_datum(self, design_entity: '_1970.Datum') -> '_3485.DatumParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Datum)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.DatumParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3485.DatumParametricStudyTool)(method_result) if method_result else None

    def results_for_datum_load_case(self, design_entity_analysis: '_6076.DatumLoadCase') -> '_3485.DatumParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.DatumLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.DatumParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3485.DatumParametricStudyTool)(method_result) if method_result else None

    def results_for_external_cad_model(self, design_entity: '_1973.ExternalCADModel') -> '_3492.ExternalCADModelParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ExternalCADModelParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3492.ExternalCADModelParametricStudyTool)(method_result) if method_result else None

    def results_for_external_cad_model_load_case(self, design_entity_analysis: '_6089.ExternalCADModelLoadCase') -> '_3492.ExternalCADModelParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ExternalCADModelLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ExternalCADModelParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3492.ExternalCADModelParametricStudyTool)(method_result) if method_result else None

    def results_for_flexible_pin_assembly(self, design_entity: '_1974.FlexiblePinAssembly') -> '_3496.FlexiblePinAssemblyParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.FlexiblePinAssemblyParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3496.FlexiblePinAssemblyParametricStudyTool)(method_result) if method_result else None

    def results_for_flexible_pin_assembly_load_case(self, design_entity_analysis: '_6093.FlexiblePinAssemblyLoadCase') -> '_3496.FlexiblePinAssemblyParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FlexiblePinAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.FlexiblePinAssemblyParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3496.FlexiblePinAssemblyParametricStudyTool)(method_result) if method_result else None

    def results_for_assembly(self, design_entity: '_1957.Assembly') -> '_3445.AssemblyParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.AssemblyParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3445.AssemblyParametricStudyTool)(method_result) if method_result else None

    def results_for_assembly_load_case(self, design_entity_analysis: '_6030.AssemblyLoadCase') -> '_3445.AssemblyParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.AssemblyParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3445.AssemblyParametricStudyTool)(method_result) if method_result else None

    def results_for_guide_dxf_model(self, design_entity: '_1975.GuideDxfModel') -> '_3500.GuideDxfModelParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.GuideDxfModelParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3500.GuideDxfModelParametricStudyTool)(method_result) if method_result else None

    def results_for_guide_dxf_model_load_case(self, design_entity_analysis: '_6101.GuideDxfModelLoadCase') -> '_3500.GuideDxfModelParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GuideDxfModelLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.GuideDxfModelParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3500.GuideDxfModelParametricStudyTool)(method_result) if method_result else None

    def results_for_imported_fe_component(self, design_entity: '_1978.ImportedFEComponent') -> '_3504.ImportedFEComponentParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ImportedFEComponent)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ImportedFEComponentParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3504.ImportedFEComponentParametricStudyTool)(method_result) if method_result else None

    def results_for_imported_fe_component_load_case(self, design_entity_analysis: '_6113.ImportedFEComponentLoadCase') -> '_3504.ImportedFEComponentParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ImportedFEComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ImportedFEComponentParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3504.ImportedFEComponentParametricStudyTool)(method_result) if method_result else None

    def results_for_mass_disc(self, design_entity: '_1981.MassDisc') -> '_3515.MassDiscParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.MassDiscParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3515.MassDiscParametricStudyTool)(method_result) if method_result else None

    def results_for_mass_disc_load_case(self, design_entity_analysis: '_6125.MassDiscLoadCase') -> '_3515.MassDiscParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MassDiscLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.MassDiscParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3515.MassDiscParametricStudyTool)(method_result) if method_result else None

    def results_for_measurement_component(self, design_entity: '_1982.MeasurementComponent') -> '_3516.MeasurementComponentParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.MeasurementComponentParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3516.MeasurementComponentParametricStudyTool)(method_result) if method_result else None

    def results_for_measurement_component_load_case(self, design_entity_analysis: '_6126.MeasurementComponentLoadCase') -> '_3516.MeasurementComponentParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MeasurementComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.MeasurementComponentParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3516.MeasurementComponentParametricStudyTool)(method_result) if method_result else None

    def results_for_mountable_component(self, design_entity: '_1983.MountableComponent') -> '_3518.MountableComponentParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.MountableComponentParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3518.MountableComponentParametricStudyTool)(method_result) if method_result else None

    def results_for_mountable_component_load_case(self, design_entity_analysis: '_6128.MountableComponentLoadCase') -> '_3518.MountableComponentParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MountableComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.MountableComponentParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3518.MountableComponentParametricStudyTool)(method_result) if method_result else None

    def results_for_oil_seal(self, design_entity: '_1985.OilSeal') -> '_3519.OilSealParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.OilSealParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3519.OilSealParametricStudyTool)(method_result) if method_result else None

    def results_for_oil_seal_load_case(self, design_entity_analysis: '_6130.OilSealLoadCase') -> '_3519.OilSealParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.OilSealLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.OilSealParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3519.OilSealParametricStudyTool)(method_result) if method_result else None

    def results_for_part(self, design_entity: '_1986.Part') -> '_3529.PartParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Part)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.PartParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3529.PartParametricStudyTool)(method_result) if method_result else None

    def results_for_part_load_case(self, design_entity_analysis: '_6132.PartLoadCase') -> '_3529.PartParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.PartParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3529.PartParametricStudyTool)(method_result) if method_result else None

    def results_for_planet_carrier(self, design_entity: '_1987.PlanetCarrier') -> '_3535.PlanetCarrierParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.PlanetCarrierParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3535.PlanetCarrierParametricStudyTool)(method_result) if method_result else None

    def results_for_planet_carrier_load_case(self, design_entity_analysis: '_6139.PlanetCarrierLoadCase') -> '_3535.PlanetCarrierParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetCarrierLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.PlanetCarrierParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3535.PlanetCarrierParametricStudyTool)(method_result) if method_result else None

    def results_for_point_load(self, design_entity: '_1989.PointLoad') -> '_3536.PointLoadParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.PointLoadParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3536.PointLoadParametricStudyTool)(method_result) if method_result else None

    def results_for_point_load_load_case(self, design_entity_analysis: '_6142.PointLoadLoadCase') -> '_3536.PointLoadParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PointLoadLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.PointLoadParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3536.PointLoadParametricStudyTool)(method_result) if method_result else None

    def results_for_power_load(self, design_entity: '_1990.PowerLoad') -> '_3537.PowerLoadParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.PowerLoadParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3537.PowerLoadParametricStudyTool)(method_result) if method_result else None

    def results_for_power_load_load_case(self, design_entity_analysis: '_6143.PowerLoadLoadCase') -> '_3537.PowerLoadParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PowerLoadLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.PowerLoadParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3537.PowerLoadParametricStudyTool)(method_result) if method_result else None

    def results_for_root_assembly(self, design_entity: '_1992.RootAssembly') -> '_3542.RootAssemblyParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.RootAssemblyParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3542.RootAssemblyParametricStudyTool)(method_result) if method_result else None

    def results_for_root_assembly_load_case(self, design_entity_analysis: '_6149.RootAssemblyLoadCase') -> '_3542.RootAssemblyParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RootAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.RootAssemblyParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3542.RootAssemblyParametricStudyTool)(method_result) if method_result else None

    def results_for_specialised_assembly(self, design_entity: '_1994.SpecialisedAssembly') -> '_3546.SpecialisedAssemblyParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.SpecialisedAssemblyParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3546.SpecialisedAssemblyParametricStudyTool)(method_result) if method_result else None

    def results_for_specialised_assembly_load_case(self, design_entity_analysis: '_6153.SpecialisedAssemblyLoadCase') -> '_3546.SpecialisedAssemblyParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpecialisedAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.SpecialisedAssemblyParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3546.SpecialisedAssemblyParametricStudyTool)(method_result) if method_result else None

    def results_for_unbalanced_mass(self, design_entity: '_1995.UnbalancedMass') -> '_3569.UnbalancedMassParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.UnbalancedMassParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3569.UnbalancedMassParametricStudyTool)(method_result) if method_result else None

    def results_for_unbalanced_mass_load_case(self, design_entity_analysis: '_6184.UnbalancedMassLoadCase') -> '_3569.UnbalancedMassParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.UnbalancedMassLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.UnbalancedMassParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3569.UnbalancedMassParametricStudyTool)(method_result) if method_result else None

    def results_for_virtual_component(self, design_entity: '_1996.VirtualComponent') -> '_3570.VirtualComponentParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.VirtualComponentParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3570.VirtualComponentParametricStudyTool)(method_result) if method_result else None

    def results_for_virtual_component_load_case(self, design_entity_analysis: '_6185.VirtualComponentLoadCase') -> '_3570.VirtualComponentParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.VirtualComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.VirtualComponentParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3570.VirtualComponentParametricStudyTool)(method_result) if method_result else None

    def results_for_shaft(self, design_entity: '_1999.Shaft') -> '_3544.ShaftParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ShaftParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3544.ShaftParametricStudyTool)(method_result) if method_result else None

    def results_for_shaft_load_case(self, design_entity_analysis: '_6151.ShaftLoadCase') -> '_3544.ShaftParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ShaftParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3544.ShaftParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_gear(self, design_entity: '_2037.ConceptGear') -> '_3468.ConceptGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ConceptGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3468.ConceptGearParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_gear_load_case(self, design_entity_analysis: '_6052.ConceptGearLoadCase') -> '_3468.ConceptGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ConceptGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3468.ConceptGearParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_gear_set(self, design_entity: '_2038.ConceptGearSet') -> '_3469.ConceptGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ConceptGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3469.ConceptGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_concept_gear_set_load_case(self, design_entity_analysis: '_6054.ConceptGearSetLoadCase') -> '_3469.ConceptGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ConceptGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3469.ConceptGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_face_gear(self, design_entity: '_2044.FaceGear') -> '_3494.FaceGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.FaceGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3494.FaceGearParametricStudyTool)(method_result) if method_result else None

    def results_for_face_gear_load_case(self, design_entity_analysis: '_6090.FaceGearLoadCase') -> '_3494.FaceGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.FaceGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3494.FaceGearParametricStudyTool)(method_result) if method_result else None

    def results_for_face_gear_set(self, design_entity: '_2045.FaceGearSet') -> '_3495.FaceGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.FaceGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3495.FaceGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_face_gear_set_load_case(self, design_entity_analysis: '_6092.FaceGearSetLoadCase') -> '_3495.FaceGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.FaceGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3495.FaceGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear(self, design_entity: '_2029.AGMAGleasonConicalGear') -> '_3443.AGMAGleasonConicalGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.AGMAGleasonConicalGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3443.AGMAGleasonConicalGearParametricStudyTool)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_load_case(self, design_entity_analysis: '_6026.AGMAGleasonConicalGearLoadCase') -> '_3443.AGMAGleasonConicalGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.AGMAGleasonConicalGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3443.AGMAGleasonConicalGearParametricStudyTool)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_set(self, design_entity: '_2030.AGMAGleasonConicalGearSet') -> '_3444.AGMAGleasonConicalGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.AGMAGleasonConicalGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3444.AGMAGleasonConicalGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_set_load_case(self, design_entity_analysis: '_6028.AGMAGleasonConicalGearSetLoadCase') -> '_3444.AGMAGleasonConicalGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.AGMAGleasonConicalGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3444.AGMAGleasonConicalGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_differential_gear(self, design_entity: '_2031.BevelDifferentialGear') -> '_3450.BevelDifferentialGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BevelDifferentialGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3450.BevelDifferentialGearParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_differential_gear_load_case(self, design_entity_analysis: '_6034.BevelDifferentialGearLoadCase') -> '_3450.BevelDifferentialGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BevelDifferentialGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3450.BevelDifferentialGearParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_differential_gear_set(self, design_entity: '_2032.BevelDifferentialGearSet') -> '_3451.BevelDifferentialGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BevelDifferentialGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3451.BevelDifferentialGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_differential_gear_set_load_case(self, design_entity_analysis: '_6036.BevelDifferentialGearSetLoadCase') -> '_3451.BevelDifferentialGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BevelDifferentialGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3451.BevelDifferentialGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_differential_planet_gear(self, design_entity: '_2033.BevelDifferentialPlanetGear') -> '_3452.BevelDifferentialPlanetGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BevelDifferentialPlanetGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3452.BevelDifferentialPlanetGearParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_differential_planet_gear_load_case(self, design_entity_analysis: '_6037.BevelDifferentialPlanetGearLoadCase') -> '_3452.BevelDifferentialPlanetGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BevelDifferentialPlanetGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3452.BevelDifferentialPlanetGearParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_differential_sun_gear(self, design_entity: '_2034.BevelDifferentialSunGear') -> '_3453.BevelDifferentialSunGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BevelDifferentialSunGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3453.BevelDifferentialSunGearParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_differential_sun_gear_load_case(self, design_entity_analysis: '_6038.BevelDifferentialSunGearLoadCase') -> '_3453.BevelDifferentialSunGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialSunGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BevelDifferentialSunGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3453.BevelDifferentialSunGearParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_gear(self, design_entity: '_2035.BevelGear') -> '_3455.BevelGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BevelGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3455.BevelGearParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_gear_load_case(self, design_entity_analysis: '_6039.BevelGearLoadCase') -> '_3455.BevelGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BevelGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3455.BevelGearParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_gear_set(self, design_entity: '_2036.BevelGearSet') -> '_3456.BevelGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BevelGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3456.BevelGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_bevel_gear_set_load_case(self, design_entity_analysis: '_6041.BevelGearSetLoadCase') -> '_3456.BevelGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.BevelGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3456.BevelGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_conical_gear(self, design_entity: '_2039.ConicalGear') -> '_3471.ConicalGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ConicalGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3471.ConicalGearParametricStudyTool)(method_result) if method_result else None

    def results_for_conical_gear_load_case(self, design_entity_analysis: '_6055.ConicalGearLoadCase') -> '_3471.ConicalGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ConicalGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3471.ConicalGearParametricStudyTool)(method_result) if method_result else None

    def results_for_conical_gear_set(self, design_entity: '_2040.ConicalGearSet') -> '_3472.ConicalGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ConicalGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3472.ConicalGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_conical_gear_set_load_case(self, design_entity_analysis: '_6059.ConicalGearSetLoadCase') -> '_3472.ConicalGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.ConicalGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3472.ConicalGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_cylindrical_gear(self, design_entity: '_2041.CylindricalGear') -> '_3482.CylindricalGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.CylindricalGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3482.CylindricalGearParametricStudyTool)(method_result) if method_result else None

    def results_for_cylindrical_gear_load_case(self, design_entity_analysis: '_6068.CylindricalGearLoadCase') -> '_3482.CylindricalGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.CylindricalGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3482.CylindricalGearParametricStudyTool)(method_result) if method_result else None

    def results_for_cylindrical_gear_set(self, design_entity: '_2042.CylindricalGearSet') -> '_3483.CylindricalGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.CylindricalGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3483.CylindricalGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_cylindrical_gear_set_load_case(self, design_entity_analysis: '_6072.CylindricalGearSetLoadCase') -> '_3483.CylindricalGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.CylindricalGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3483.CylindricalGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_cylindrical_planet_gear(self, design_entity: '_2043.CylindricalPlanetGear') -> '_3484.CylindricalPlanetGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.CylindricalPlanetGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3484.CylindricalPlanetGearParametricStudyTool)(method_result) if method_result else None

    def results_for_cylindrical_planet_gear_load_case(self, design_entity_analysis: '_6073.CylindricalPlanetGearLoadCase') -> '_3484.CylindricalPlanetGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.CylindricalPlanetGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3484.CylindricalPlanetGearParametricStudyTool)(method_result) if method_result else None

    def results_for_gear(self, design_entity: '_2046.Gear') -> '_3498.GearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.GearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3498.GearParametricStudyTool)(method_result) if method_result else None

    def results_for_gear_load_case(self, design_entity_analysis: '_6095.GearLoadCase') -> '_3498.GearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.GearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3498.GearParametricStudyTool)(method_result) if method_result else None

    def results_for_gear_set(self, design_entity: '_2048.GearSet') -> '_3499.GearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.GearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3499.GearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_gear_set_load_case(self, design_entity_analysis: '_6100.GearSetLoadCase') -> '_3499.GearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.GearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3499.GearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_hypoid_gear(self, design_entity: '_2050.HypoidGear') -> '_3502.HypoidGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.HypoidGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3502.HypoidGearParametricStudyTool)(method_result) if method_result else None

    def results_for_hypoid_gear_load_case(self, design_entity_analysis: '_6110.HypoidGearLoadCase') -> '_3502.HypoidGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.HypoidGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3502.HypoidGearParametricStudyTool)(method_result) if method_result else None

    def results_for_hypoid_gear_set(self, design_entity: '_2051.HypoidGearSet') -> '_3503.HypoidGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.HypoidGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3503.HypoidGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_hypoid_gear_set_load_case(self, design_entity_analysis: '_6112.HypoidGearSetLoadCase') -> '_3503.HypoidGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.HypoidGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3503.HypoidGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear(self, design_entity: '_2052.KlingelnbergCycloPalloidConicalGear') -> '_3507.KlingelnbergCycloPalloidConicalGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidConicalGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3507.KlingelnbergCycloPalloidConicalGearParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_load_case(self, design_entity_analysis: '_6116.KlingelnbergCycloPalloidConicalGearLoadCase') -> '_3507.KlingelnbergCycloPalloidConicalGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidConicalGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3507.KlingelnbergCycloPalloidConicalGearParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set(self, design_entity: '_2053.KlingelnbergCycloPalloidConicalGearSet') -> '_3508.KlingelnbergCycloPalloidConicalGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidConicalGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3508.KlingelnbergCycloPalloidConicalGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set_load_case(self, design_entity_analysis: '_6118.KlingelnbergCycloPalloidConicalGearSetLoadCase') -> '_3508.KlingelnbergCycloPalloidConicalGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidConicalGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3508.KlingelnbergCycloPalloidConicalGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear(self, design_entity: '_2054.KlingelnbergCycloPalloidHypoidGear') -> '_3510.KlingelnbergCycloPalloidHypoidGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidHypoidGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3510.KlingelnbergCycloPalloidHypoidGearParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_load_case(self, design_entity_analysis: '_6119.KlingelnbergCycloPalloidHypoidGearLoadCase') -> '_3510.KlingelnbergCycloPalloidHypoidGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidHypoidGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3510.KlingelnbergCycloPalloidHypoidGearParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set(self, design_entity: '_2055.KlingelnbergCycloPalloidHypoidGearSet') -> '_3511.KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3511.KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set_load_case(self, design_entity_analysis: '_6121.KlingelnbergCycloPalloidHypoidGearSetLoadCase') -> '_3511.KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3511.KlingelnbergCycloPalloidHypoidGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, design_entity: '_2056.KlingelnbergCycloPalloidSpiralBevelGear') -> '_3513.KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3513.KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_load_case(self, design_entity_analysis: '_6122.KlingelnbergCycloPalloidSpiralBevelGearLoadCase') -> '_3513.KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3513.KlingelnbergCycloPalloidSpiralBevelGearParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, design_entity: '_2057.KlingelnbergCycloPalloidSpiralBevelGearSet') -> '_3514.KlingelnbergCycloPalloidSpiralBevelGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidSpiralBevelGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3514.KlingelnbergCycloPalloidSpiralBevelGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_load_case(self, design_entity_analysis: '_6124.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase') -> '_3514.KlingelnbergCycloPalloidSpiralBevelGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.KlingelnbergCycloPalloidSpiralBevelGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3514.KlingelnbergCycloPalloidSpiralBevelGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_planetary_gear_set(self, design_entity: '_2058.PlanetaryGearSet') -> '_3534.PlanetaryGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.PlanetaryGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3534.PlanetaryGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_planetary_gear_set_load_case(self, design_entity_analysis: '_6137.PlanetaryGearSetLoadCase') -> '_3534.PlanetaryGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetaryGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.PlanetaryGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3534.PlanetaryGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_spiral_bevel_gear(self, design_entity: '_2059.SpiralBevelGear') -> '_3548.SpiralBevelGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.SpiralBevelGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3548.SpiralBevelGearParametricStudyTool)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_load_case(self, design_entity_analysis: '_6155.SpiralBevelGearLoadCase') -> '_3548.SpiralBevelGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.SpiralBevelGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3548.SpiralBevelGearParametricStudyTool)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_set(self, design_entity: '_2060.SpiralBevelGearSet') -> '_3549.SpiralBevelGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.SpiralBevelGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3549.SpiralBevelGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_set_load_case(self, design_entity_analysis: '_6157.SpiralBevelGearSetLoadCase') -> '_3549.SpiralBevelGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.SpiralBevelGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3549.SpiralBevelGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear(self, design_entity: '_2061.StraightBevelDiffGear') -> '_3554.StraightBevelDiffGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelDiffGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3554.StraightBevelDiffGearParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_load_case(self, design_entity_analysis: '_6162.StraightBevelDiffGearLoadCase') -> '_3554.StraightBevelDiffGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelDiffGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3554.StraightBevelDiffGearParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_set(self, design_entity: '_2062.StraightBevelDiffGearSet') -> '_3555.StraightBevelDiffGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelDiffGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3555.StraightBevelDiffGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_set_load_case(self, design_entity_analysis: '_6164.StraightBevelDiffGearSetLoadCase') -> '_3555.StraightBevelDiffGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelDiffGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3555.StraightBevelDiffGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_gear(self, design_entity: '_2063.StraightBevelGear') -> '_3557.StraightBevelGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3557.StraightBevelGearParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_gear_load_case(self, design_entity_analysis: '_6165.StraightBevelGearLoadCase') -> '_3557.StraightBevelGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3557.StraightBevelGearParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_gear_set(self, design_entity: '_2064.StraightBevelGearSet') -> '_3558.StraightBevelGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3558.StraightBevelGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_gear_set_load_case(self, design_entity_analysis: '_6167.StraightBevelGearSetLoadCase') -> '_3558.StraightBevelGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3558.StraightBevelGearSetParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_planet_gear(self, design_entity: '_2065.StraightBevelPlanetGear') -> '_3559.StraightBevelPlanetGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelPlanetGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3559.StraightBevelPlanetGearParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_planet_gear_load_case(self, design_entity_analysis: '_6168.StraightBevelPlanetGearLoadCase') -> '_3559.StraightBevelPlanetGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelPlanetGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3559.StraightBevelPlanetGearParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_sun_gear(self, design_entity: '_2066.StraightBevelSunGear') -> '_3560.StraightBevelSunGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelSunGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3560.StraightBevelSunGearParametricStudyTool)(method_result) if method_result else None

    def results_for_straight_bevel_sun_gear_load_case(self, design_entity_analysis: '_6169.StraightBevelSunGearLoadCase') -> '_3560.StraightBevelSunGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelSunGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.StraightBevelSunGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3560.StraightBevelSunGearParametricStudyTool)(method_result) if method_result else None

    def results_for_worm_gear(self, design_entity: '_2067.WormGear') -> '_3572.WormGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.WormGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3572.WormGearParametricStudyTool)(method_result) if method_result else None

    def results_for_worm_gear_load_case(self, design_entity_analysis: '_6186.WormGearLoadCase') -> '_3572.WormGearParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.WormGearParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_3572.WormGearParametricStudyTool)(method_result) if method_result else None

    def results_for_worm_gear_set(self, design_entity: '_2068.WormGearSet') -> '_3573.WormGearSetParametricStudyTool':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.parametric_study_tools.WormGearSetParametricStudyTool
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_3573.WormGearSetParametricStudyTool)(method_result) if method_result else None
