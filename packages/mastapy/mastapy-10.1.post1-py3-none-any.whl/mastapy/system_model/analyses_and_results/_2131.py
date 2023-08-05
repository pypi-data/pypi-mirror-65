'''_2131.py

AdvancedSystemDeflectionAnalysis
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
from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
    _6333, _6334, _6336, _6288,
    _6290, _6220, _6231, _6233,
    _6236, _6238, _6247, _6249,
    _6250, _6252, _6296, _6302,
    _6297, _6298, _6308, _6310,
    _6319, _6320, _6321, _6322,
    _6323, _6325, _6326, _6251,
    _6219, _6234, _6245, _6272,
    _6291, _6299, _6303, _6222,
    _6240, _6261, _6312, _6227,
    _6243, _6215, _6254, _6269,
    _6274, _6277, _6280, _6306,
    _6315, _6332, _6335, _6265,
    _6289, _6232, _6237, _6248,
    _6309, _6324, _6209, _6210,
    _6218, _6229, _6230, _6235,
    _6246, _6258, _6259, _6263,
    _6217, _6267, _6271, _6283,
    _6284, _6285, _6286, _6287,
    _6293, _6294, _6295, _6300,
    _6304, _6328, _6330, _6301,
    _6239, _6241, _6260, _6262,
    _6214, _6216, _6221, _6223,
    _6224, _6225, _6226, _6228,
    _6242, _6244, _6253, _6255,
    _6257, _6264, _6266, _6268,
    _6270, _6273, _6275, _6276,
    _6278, _6279, _6281, _6292,
    _6305, _6307, _6311, _6313,
    _6314, _6316, _6317, _6318,
    _6331
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

_ADVANCED_SYSTEM_DEFLECTION_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'AdvancedSystemDeflectionAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AdvancedSystemDeflectionAnalysis',)


class AdvancedSystemDeflectionAnalysis(_2130.SingleAnalysis):
    '''AdvancedSystemDeflectionAnalysis

    This is a mastapy class.
    '''

    TYPE = _ADVANCED_SYSTEM_DEFLECTION_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AdvancedSystemDeflectionAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    def results_for_worm_gear_set_load_case(self, design_entity_analysis: '_6188.WormGearSetLoadCase') -> '_6333.WormGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.WormGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6333.WormGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_zerol_bevel_gear(self, design_entity: '_2069.ZerolBevelGear') -> '_6334.ZerolBevelGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ZerolBevelGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6334.ZerolBevelGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_load_case(self, design_entity_analysis: '_6189.ZerolBevelGearLoadCase') -> '_6334.ZerolBevelGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ZerolBevelGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6334.ZerolBevelGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_set(self, design_entity: '_2070.ZerolBevelGearSet') -> '_6336.ZerolBevelGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ZerolBevelGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6336.ZerolBevelGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_set_load_case(self, design_entity_analysis: '_6191.ZerolBevelGearSetLoadCase') -> '_6336.ZerolBevelGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ZerolBevelGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6336.ZerolBevelGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling(self, design_entity: '_2099.PartToPartShearCoupling') -> '_6288.PartToPartShearCouplingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCoupling)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PartToPartShearCouplingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6288.PartToPartShearCouplingAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_load_case(self, design_entity_analysis: '_6135.PartToPartShearCouplingLoadCase') -> '_6288.PartToPartShearCouplingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PartToPartShearCouplingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6288.PartToPartShearCouplingAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_half(self, design_entity: '_2100.PartToPartShearCouplingHalf') -> '_6290.PartToPartShearCouplingHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PartToPartShearCouplingHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6290.PartToPartShearCouplingHalfAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_half_load_case(self, design_entity_analysis: '_6134.PartToPartShearCouplingHalfLoadCase') -> '_6290.PartToPartShearCouplingHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PartToPartShearCouplingHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6290.PartToPartShearCouplingHalfAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_belt_drive(self, design_entity: '_2088.BeltDrive') -> '_6220.BeltDriveAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BeltDriveAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6220.BeltDriveAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_belt_drive_load_case(self, design_entity_analysis: '_6033.BeltDriveLoadCase') -> '_6220.BeltDriveAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BeltDriveLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BeltDriveAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6220.BeltDriveAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_clutch(self, design_entity: '_2090.Clutch') -> '_6231.ClutchAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ClutchAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6231.ClutchAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_clutch_load_case(self, design_entity_analysis: '_6046.ClutchLoadCase') -> '_6231.ClutchAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ClutchAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6231.ClutchAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_clutch_half(self, design_entity: '_2091.ClutchHalf') -> '_6233.ClutchHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ClutchHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6233.ClutchHalfAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_clutch_half_load_case(self, design_entity_analysis: '_6045.ClutchHalfLoadCase') -> '_6233.ClutchHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ClutchHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6233.ClutchHalfAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_concept_coupling(self, design_entity: '_2093.ConceptCoupling') -> '_6236.ConceptCouplingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptCouplingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6236.ConceptCouplingAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_concept_coupling_load_case(self, design_entity_analysis: '_6051.ConceptCouplingLoadCase') -> '_6236.ConceptCouplingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptCouplingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6236.ConceptCouplingAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_concept_coupling_half(self, design_entity: '_2094.ConceptCouplingHalf') -> '_6238.ConceptCouplingHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptCouplingHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6238.ConceptCouplingHalfAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_concept_coupling_half_load_case(self, design_entity_analysis: '_6050.ConceptCouplingHalfLoadCase') -> '_6238.ConceptCouplingHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptCouplingHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6238.ConceptCouplingHalfAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_coupling(self, design_entity: '_2095.Coupling') -> '_6247.CouplingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CouplingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6247.CouplingAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_coupling_load_case(self, design_entity_analysis: '_6064.CouplingLoadCase') -> '_6247.CouplingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CouplingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6247.CouplingAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_coupling_half(self, design_entity: '_2096.CouplingHalf') -> '_6249.CouplingHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CouplingHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6249.CouplingHalfAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_coupling_half_load_case(self, design_entity_analysis: '_6063.CouplingHalfLoadCase') -> '_6249.CouplingHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CouplingHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6249.CouplingHalfAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_cvt(self, design_entity: '_2097.CVT') -> '_6250.CVTAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CVTAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6250.CVTAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_cvt_load_case(self, design_entity_analysis: '_6066.CVTLoadCase') -> '_6250.CVTAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CVTAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6250.CVTAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_cvt_pulley(self, design_entity: '_2098.CVTPulley') -> '_6252.CVTPulleyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CVTPulleyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6252.CVTPulleyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_cvt_pulley_load_case(self, design_entity_analysis: '_6067.CVTPulleyLoadCase') -> '_6252.CVTPulleyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTPulleyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CVTPulleyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6252.CVTPulleyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_pulley(self, design_entity: '_2101.Pulley') -> '_6296.PulleyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PulleyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6296.PulleyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_pulley_load_case(self, design_entity_analysis: '_6144.PulleyLoadCase') -> '_6296.PulleyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PulleyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PulleyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6296.PulleyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_shaft_hub_connection(self, design_entity: '_2109.ShaftHubConnection') -> '_6302.ShaftHubConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ShaftHubConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6302.ShaftHubConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_shaft_hub_connection_load_case(self, design_entity_analysis: '_6150.ShaftHubConnectionLoadCase') -> '_6302.ShaftHubConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftHubConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ShaftHubConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6302.ShaftHubConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_rolling_ring(self, design_entity: '_2107.RollingRing') -> '_6297.RollingRingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.RollingRingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6297.RollingRingAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_rolling_ring_load_case(self, design_entity_analysis: '_6148.RollingRingLoadCase') -> '_6297.RollingRingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.RollingRingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6297.RollingRingAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_rolling_ring_assembly(self, design_entity: '_2108.RollingRingAssembly') -> '_6298.RollingRingAssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.RollingRingAssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6298.RollingRingAssemblyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_rolling_ring_assembly_load_case(self, design_entity_analysis: '_6146.RollingRingAssemblyLoadCase') -> '_6298.RollingRingAssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.RollingRingAssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6298.RollingRingAssemblyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_spring_damper(self, design_entity: '_2110.SpringDamper') -> '_6308.SpringDamperAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpringDamperAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6308.SpringDamperAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_spring_damper_load_case(self, design_entity_analysis: '_6160.SpringDamperLoadCase') -> '_6308.SpringDamperAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpringDamperAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6308.SpringDamperAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_spring_damper_half(self, design_entity: '_2111.SpringDamperHalf') -> '_6310.SpringDamperHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpringDamperHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6310.SpringDamperHalfAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_spring_damper_half_load_case(self, design_entity_analysis: '_6159.SpringDamperHalfLoadCase') -> '_6310.SpringDamperHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpringDamperHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6310.SpringDamperHalfAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_synchroniser(self, design_entity: '_2112.Synchroniser') -> '_6319.SynchroniserAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SynchroniserAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6319.SynchroniserAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_synchroniser_load_case(self, design_entity_analysis: '_6171.SynchroniserLoadCase') -> '_6319.SynchroniserAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SynchroniserAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6319.SynchroniserAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_synchroniser_half(self, design_entity: '_2114.SynchroniserHalf') -> '_6320.SynchroniserHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SynchroniserHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6320.SynchroniserHalfAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_synchroniser_half_load_case(self, design_entity_analysis: '_6170.SynchroniserHalfLoadCase') -> '_6320.SynchroniserHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SynchroniserHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6320.SynchroniserHalfAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_synchroniser_part(self, design_entity: '_2115.SynchroniserPart') -> '_6321.SynchroniserPartAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SynchroniserPartAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6321.SynchroniserPartAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_synchroniser_part_load_case(self, design_entity_analysis: '_6172.SynchroniserPartLoadCase') -> '_6321.SynchroniserPartAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserPartLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SynchroniserPartAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6321.SynchroniserPartAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_synchroniser_sleeve(self, design_entity: '_2116.SynchroniserSleeve') -> '_6322.SynchroniserSleeveAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SynchroniserSleeveAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6322.SynchroniserSleeveAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_synchroniser_sleeve_load_case(self, design_entity_analysis: '_6173.SynchroniserSleeveLoadCase') -> '_6322.SynchroniserSleeveAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserSleeveLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SynchroniserSleeveAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6322.SynchroniserSleeveAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_torque_converter(self, design_entity: '_2117.TorqueConverter') -> '_6323.TorqueConverterAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.TorqueConverterAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6323.TorqueConverterAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_torque_converter_load_case(self, design_entity_analysis: '_6177.TorqueConverterLoadCase') -> '_6323.TorqueConverterAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.TorqueConverterAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6323.TorqueConverterAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_torque_converter_pump(self, design_entity: '_2118.TorqueConverterPump') -> '_6325.TorqueConverterPumpAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.TorqueConverterPumpAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6325.TorqueConverterPumpAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_torque_converter_pump_load_case(self, design_entity_analysis: '_6178.TorqueConverterPumpLoadCase') -> '_6325.TorqueConverterPumpAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterPumpLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.TorqueConverterPumpAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6325.TorqueConverterPumpAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_torque_converter_turbine(self, design_entity: '_2120.TorqueConverterTurbine') -> '_6326.TorqueConverterTurbineAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.TorqueConverterTurbineAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6326.TorqueConverterTurbineAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_torque_converter_turbine_load_case(self, design_entity_analysis: '_6179.TorqueConverterTurbineLoadCase') -> '_6326.TorqueConverterTurbineAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterTurbineLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.TorqueConverterTurbineAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6326.TorqueConverterTurbineAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_cvt_belt_connection(self, design_entity: '_1815.CVTBeltConnection') -> '_6251.CVTBeltConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CVTBeltConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6251.CVTBeltConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_cvt_belt_connection_load_case(self, design_entity_analysis: '_6065.CVTBeltConnectionLoadCase') -> '_6251.CVTBeltConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTBeltConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CVTBeltConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6251.CVTBeltConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_belt_connection(self, design_entity: '_1810.BeltConnection') -> '_6219.BeltConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BeltConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6219.BeltConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_belt_connection_load_case(self, design_entity_analysis: '_6032.BeltConnectionLoadCase') -> '_6219.BeltConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BeltConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BeltConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6219.BeltConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_coaxial_connection(self, design_entity: '_1811.CoaxialConnection') -> '_6234.CoaxialConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CoaxialConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6234.CoaxialConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_coaxial_connection_load_case(self, design_entity_analysis: '_6047.CoaxialConnectionLoadCase') -> '_6234.CoaxialConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CoaxialConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CoaxialConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6234.CoaxialConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_connection(self, design_entity: '_1814.Connection') -> '_6245.ConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6245.ConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_connection_load_case(self, design_entity_analysis: '_6060.ConnectionLoadCase') -> '_6245.ConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6245.ConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_inter_mountable_component_connection(self, design_entity: '_1823.InterMountableComponentConnection') -> '_6272.InterMountableComponentConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.InterMountableComponentConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6272.InterMountableComponentConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_inter_mountable_component_connection_load_case(self, design_entity_analysis: '_6115.InterMountableComponentConnectionLoadCase') -> '_6272.InterMountableComponentConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.InterMountableComponentConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.InterMountableComponentConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6272.InterMountableComponentConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_planetary_connection(self, design_entity: '_1826.PlanetaryConnection') -> '_6291.PlanetaryConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PlanetaryConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6291.PlanetaryConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_planetary_connection_load_case(self, design_entity_analysis: '_6136.PlanetaryConnectionLoadCase') -> '_6291.PlanetaryConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetaryConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PlanetaryConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6291.PlanetaryConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_rolling_ring_connection(self, design_entity: '_1830.RollingRingConnection') -> '_6299.RollingRingConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.RollingRingConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6299.RollingRingConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_rolling_ring_connection_load_case(self, design_entity_analysis: '_6147.RollingRingConnectionLoadCase') -> '_6299.RollingRingConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.RollingRingConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6299.RollingRingConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_shaft_to_mountable_component_connection(self, design_entity: '_1834.ShaftToMountableComponentConnection') -> '_6303.ShaftToMountableComponentConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ShaftToMountableComponentConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6303.ShaftToMountableComponentConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_shaft_to_mountable_component_connection_load_case(self, design_entity_analysis: '_6152.ShaftToMountableComponentConnectionLoadCase') -> '_6303.ShaftToMountableComponentConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftToMountableComponentConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ShaftToMountableComponentConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6303.ShaftToMountableComponentConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_differential_gear_mesh(self, design_entity: '_1840.BevelDifferentialGearMesh') -> '_6222.BevelDifferentialGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelDifferentialGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6222.BevelDifferentialGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_differential_gear_mesh_load_case(self, design_entity_analysis: '_6035.BevelDifferentialGearMeshLoadCase') -> '_6222.BevelDifferentialGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelDifferentialGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6222.BevelDifferentialGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_concept_gear_mesh(self, design_entity: '_1844.ConceptGearMesh') -> '_6240.ConceptGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6240.ConceptGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_concept_gear_mesh_load_case(self, design_entity_analysis: '_6053.ConceptGearMeshLoadCase') -> '_6240.ConceptGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6240.ConceptGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_face_gear_mesh(self, design_entity: '_1850.FaceGearMesh') -> '_6261.FaceGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.FaceGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6261.FaceGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_face_gear_mesh_load_case(self, design_entity_analysis: '_6091.FaceGearMeshLoadCase') -> '_6261.FaceGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.FaceGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6261.FaceGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_mesh(self, design_entity: '_1864.StraightBevelDiffGearMesh') -> '_6312.StraightBevelDiffGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelDiffGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6312.StraightBevelDiffGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_mesh_load_case(self, design_entity_analysis: '_6163.StraightBevelDiffGearMeshLoadCase') -> '_6312.StraightBevelDiffGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelDiffGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6312.StraightBevelDiffGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_gear_mesh(self, design_entity: '_1842.BevelGearMesh') -> '_6227.BevelGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6227.BevelGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6040.BevelGearMeshLoadCase') -> '_6227.BevelGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6227.BevelGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_conical_gear_mesh(self, design_entity: '_1846.ConicalGearMesh') -> '_6243.ConicalGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConicalGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6243.ConicalGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_conical_gear_mesh_load_case(self, design_entity_analysis: '_6057.ConicalGearMeshLoadCase') -> '_6243.ConicalGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConicalGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6243.ConicalGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_mesh(self, design_entity: '_1838.AGMAGleasonConicalGearMesh') -> '_6215.AGMAGleasonConicalGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AGMAGleasonConicalGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6215.AGMAGleasonConicalGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_mesh_load_case(self, design_entity_analysis: '_6027.AGMAGleasonConicalGearMeshLoadCase') -> '_6215.AGMAGleasonConicalGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AGMAGleasonConicalGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6215.AGMAGleasonConicalGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_cylindrical_gear_mesh(self, design_entity: '_1848.CylindricalGearMesh') -> '_6254.CylindricalGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CylindricalGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6254.CylindricalGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_cylindrical_gear_mesh_load_case(self, design_entity_analysis: '_6070.CylindricalGearMeshLoadCase') -> '_6254.CylindricalGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CylindricalGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6254.CylindricalGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_hypoid_gear_mesh(self, design_entity: '_1854.HypoidGearMesh') -> '_6269.HypoidGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.HypoidGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6269.HypoidGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_hypoid_gear_mesh_load_case(self, design_entity_analysis: '_6111.HypoidGearMeshLoadCase') -> '_6269.HypoidGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.HypoidGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6269.HypoidGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh(self, design_entity: '_1857.KlingelnbergCycloPalloidConicalGearMesh') -> '_6274.KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6274.KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh_load_case(self, design_entity_analysis: '_6117.KlingelnbergCycloPalloidConicalGearMeshLoadCase') -> '_6274.KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6274.KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, design_entity: '_1858.KlingelnbergCycloPalloidHypoidGearMesh') -> '_6277.KlingelnbergCycloPalloidHypoidGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidHypoidGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6277.KlingelnbergCycloPalloidHypoidGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh_load_case(self, design_entity_analysis: '_6120.KlingelnbergCycloPalloidHypoidGearMeshLoadCase') -> '_6277.KlingelnbergCycloPalloidHypoidGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidHypoidGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6277.KlingelnbergCycloPalloidHypoidGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, design_entity: '_1859.KlingelnbergCycloPalloidSpiralBevelGearMesh') -> '_6280.KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6280.KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6123.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase') -> '_6280.KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6280.KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_mesh(self, design_entity: '_1862.SpiralBevelGearMesh') -> '_6306.SpiralBevelGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpiralBevelGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6306.SpiralBevelGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6156.SpiralBevelGearMeshLoadCase') -> '_6306.SpiralBevelGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpiralBevelGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6306.SpiralBevelGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_gear_mesh(self, design_entity: '_1866.StraightBevelGearMesh') -> '_6315.StraightBevelGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6315.StraightBevelGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6166.StraightBevelGearMeshLoadCase') -> '_6315.StraightBevelGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6315.StraightBevelGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_worm_gear_mesh(self, design_entity: '_1868.WormGearMesh') -> '_6332.WormGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.WormGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6332.WormGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_worm_gear_mesh_load_case(self, design_entity_analysis: '_6187.WormGearMeshLoadCase') -> '_6332.WormGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.WormGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6332.WormGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_mesh(self, design_entity: '_1870.ZerolBevelGearMesh') -> '_6335.ZerolBevelGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ZerolBevelGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6335.ZerolBevelGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6190.ZerolBevelGearMeshLoadCase') -> '_6335.ZerolBevelGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ZerolBevelGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6335.ZerolBevelGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_gear_mesh(self, design_entity: '_1852.GearMesh') -> '_6265.GearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.GearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6265.GearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_gear_mesh_load_case(self, design_entity_analysis: '_6097.GearMeshLoadCase') -> '_6265.GearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.GearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6265.GearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_connection(self, design_entity: '_1878.PartToPartShearCouplingConnection') -> '_6289.PartToPartShearCouplingConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PartToPartShearCouplingConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6289.PartToPartShearCouplingConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_connection_load_case(self, design_entity_analysis: '_6133.PartToPartShearCouplingConnectionLoadCase') -> '_6289.PartToPartShearCouplingConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PartToPartShearCouplingConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6289.PartToPartShearCouplingConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_clutch_connection(self, design_entity: '_1872.ClutchConnection') -> '_6232.ClutchConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ClutchConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6232.ClutchConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_clutch_connection_load_case(self, design_entity_analysis: '_6044.ClutchConnectionLoadCase') -> '_6232.ClutchConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ClutchConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6232.ClutchConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_concept_coupling_connection(self, design_entity: '_1874.ConceptCouplingConnection') -> '_6237.ConceptCouplingConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptCouplingConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6237.ConceptCouplingConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_concept_coupling_connection_load_case(self, design_entity_analysis: '_6049.ConceptCouplingConnectionLoadCase') -> '_6237.ConceptCouplingConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptCouplingConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6237.ConceptCouplingConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_coupling_connection(self, design_entity: '_1876.CouplingConnection') -> '_6248.CouplingConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CouplingConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6248.CouplingConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_coupling_connection_load_case(self, design_entity_analysis: '_6062.CouplingConnectionLoadCase') -> '_6248.CouplingConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CouplingConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6248.CouplingConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_spring_damper_connection(self, design_entity: '_1880.SpringDamperConnection') -> '_6309.SpringDamperConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpringDamperConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6309.SpringDamperConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_spring_damper_connection_load_case(self, design_entity_analysis: '_6158.SpringDamperConnectionLoadCase') -> '_6309.SpringDamperConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpringDamperConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6309.SpringDamperConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_torque_converter_connection(self, design_entity: '_1882.TorqueConverterConnection') -> '_6324.TorqueConverterConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.TorqueConverterConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6324.TorqueConverterConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_torque_converter_connection_load_case(self, design_entity_analysis: '_6176.TorqueConverterConnectionLoadCase') -> '_6324.TorqueConverterConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.TorqueConverterConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6324.TorqueConverterConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_abstract_assembly(self, design_entity: '_1958.AbstractAssembly') -> '_6209.AbstractAssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AbstractAssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6209.AbstractAssemblyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_abstract_assembly_load_case(self, design_entity_analysis: '_6023.AbstractAssemblyLoadCase') -> '_6209.AbstractAssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AbstractAssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6209.AbstractAssemblyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_abstract_shaft_or_housing(self, design_entity: '_1959.AbstractShaftOrHousing') -> '_6210.AbstractShaftOrHousingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AbstractShaftOrHousingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6210.AbstractShaftOrHousingAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_abstract_shaft_or_housing_load_case(self, design_entity_analysis: '_6024.AbstractShaftOrHousingLoadCase') -> '_6210.AbstractShaftOrHousingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractShaftOrHousingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AbstractShaftOrHousingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6210.AbstractShaftOrHousingAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bearing(self, design_entity: '_1962.Bearing') -> '_6218.BearingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BearingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6218.BearingAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bearing_load_case(self, design_entity_analysis: '_6031.BearingLoadCase') -> '_6218.BearingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BearingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BearingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6218.BearingAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bolt(self, design_entity: '_1964.Bolt') -> '_6229.BoltAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BoltAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6229.BoltAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bolt_load_case(self, design_entity_analysis: '_6043.BoltLoadCase') -> '_6229.BoltAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BoltLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BoltAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6229.BoltAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bolted_joint(self, design_entity: '_1965.BoltedJoint') -> '_6230.BoltedJointAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BoltedJointAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6230.BoltedJointAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bolted_joint_load_case(self, design_entity_analysis: '_6042.BoltedJointLoadCase') -> '_6230.BoltedJointAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BoltedJointLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BoltedJointAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6230.BoltedJointAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_component(self, design_entity: '_1966.Component') -> '_6235.ComponentAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ComponentAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6235.ComponentAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_component_load_case(self, design_entity_analysis: '_6048.ComponentLoadCase') -> '_6235.ComponentAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ComponentAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6235.ComponentAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_connector(self, design_entity: '_1969.Connector') -> '_6246.ConnectorAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Connector)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConnectorAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6246.ConnectorAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_connector_load_case(self, design_entity_analysis: '_6061.ConnectorLoadCase') -> '_6246.ConnectorAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConnectorLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConnectorAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6246.ConnectorAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_datum(self, design_entity: '_1970.Datum') -> '_6258.DatumAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Datum)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.DatumAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6258.DatumAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_datum_load_case(self, design_entity_analysis: '_6076.DatumLoadCase') -> '_6258.DatumAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.DatumLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.DatumAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6258.DatumAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_external_cad_model(self, design_entity: '_1973.ExternalCADModel') -> '_6259.ExternalCADModelAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ExternalCADModelAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6259.ExternalCADModelAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_external_cad_model_load_case(self, design_entity_analysis: '_6089.ExternalCADModelLoadCase') -> '_6259.ExternalCADModelAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ExternalCADModelLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ExternalCADModelAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6259.ExternalCADModelAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_flexible_pin_assembly(self, design_entity: '_1974.FlexiblePinAssembly') -> '_6263.FlexiblePinAssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.FlexiblePinAssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6263.FlexiblePinAssemblyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_flexible_pin_assembly_load_case(self, design_entity_analysis: '_6093.FlexiblePinAssemblyLoadCase') -> '_6263.FlexiblePinAssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FlexiblePinAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.FlexiblePinAssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6263.FlexiblePinAssemblyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_assembly(self, design_entity: '_1957.Assembly') -> '_6217.AssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6217.AssemblyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_assembly_load_case(self, design_entity_analysis: '_6030.AssemblyLoadCase') -> '_6217.AssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6217.AssemblyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_guide_dxf_model(self, design_entity: '_1975.GuideDxfModel') -> '_6267.GuideDxfModelAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.GuideDxfModelAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6267.GuideDxfModelAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_guide_dxf_model_load_case(self, design_entity_analysis: '_6101.GuideDxfModelLoadCase') -> '_6267.GuideDxfModelAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GuideDxfModelLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.GuideDxfModelAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6267.GuideDxfModelAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_imported_fe_component(self, design_entity: '_1978.ImportedFEComponent') -> '_6271.ImportedFEComponentAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ImportedFEComponent)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ImportedFEComponentAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6271.ImportedFEComponentAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_imported_fe_component_load_case(self, design_entity_analysis: '_6113.ImportedFEComponentLoadCase') -> '_6271.ImportedFEComponentAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ImportedFEComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ImportedFEComponentAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6271.ImportedFEComponentAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_mass_disc(self, design_entity: '_1981.MassDisc') -> '_6283.MassDiscAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.MassDiscAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6283.MassDiscAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_mass_disc_load_case(self, design_entity_analysis: '_6125.MassDiscLoadCase') -> '_6283.MassDiscAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MassDiscLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.MassDiscAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6283.MassDiscAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_measurement_component(self, design_entity: '_1982.MeasurementComponent') -> '_6284.MeasurementComponentAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.MeasurementComponentAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6284.MeasurementComponentAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_measurement_component_load_case(self, design_entity_analysis: '_6126.MeasurementComponentLoadCase') -> '_6284.MeasurementComponentAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MeasurementComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.MeasurementComponentAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6284.MeasurementComponentAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_mountable_component(self, design_entity: '_1983.MountableComponent') -> '_6285.MountableComponentAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.MountableComponentAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6285.MountableComponentAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_mountable_component_load_case(self, design_entity_analysis: '_6128.MountableComponentLoadCase') -> '_6285.MountableComponentAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MountableComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.MountableComponentAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6285.MountableComponentAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_oil_seal(self, design_entity: '_1985.OilSeal') -> '_6286.OilSealAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.OilSealAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6286.OilSealAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_oil_seal_load_case(self, design_entity_analysis: '_6130.OilSealLoadCase') -> '_6286.OilSealAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.OilSealLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.OilSealAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6286.OilSealAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_part(self, design_entity: '_1986.Part') -> '_6287.PartAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Part)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PartAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6287.PartAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_part_load_case(self, design_entity_analysis: '_6132.PartLoadCase') -> '_6287.PartAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PartAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6287.PartAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_planet_carrier(self, design_entity: '_1987.PlanetCarrier') -> '_6293.PlanetCarrierAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PlanetCarrierAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6293.PlanetCarrierAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_planet_carrier_load_case(self, design_entity_analysis: '_6139.PlanetCarrierLoadCase') -> '_6293.PlanetCarrierAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetCarrierLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PlanetCarrierAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6293.PlanetCarrierAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_point_load(self, design_entity: '_1989.PointLoad') -> '_6294.PointLoadAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PointLoadAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6294.PointLoadAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_point_load_load_case(self, design_entity_analysis: '_6142.PointLoadLoadCase') -> '_6294.PointLoadAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PointLoadLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PointLoadAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6294.PointLoadAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_power_load(self, design_entity: '_1990.PowerLoad') -> '_6295.PowerLoadAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PowerLoadAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6295.PowerLoadAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_power_load_load_case(self, design_entity_analysis: '_6143.PowerLoadLoadCase') -> '_6295.PowerLoadAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PowerLoadLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PowerLoadAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6295.PowerLoadAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_root_assembly(self, design_entity: '_1992.RootAssembly') -> '_6300.RootAssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.RootAssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6300.RootAssemblyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_root_assembly_load_case(self, design_entity_analysis: '_6149.RootAssemblyLoadCase') -> '_6300.RootAssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RootAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.RootAssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6300.RootAssemblyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_specialised_assembly(self, design_entity: '_1994.SpecialisedAssembly') -> '_6304.SpecialisedAssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpecialisedAssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6304.SpecialisedAssemblyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_specialised_assembly_load_case(self, design_entity_analysis: '_6153.SpecialisedAssemblyLoadCase') -> '_6304.SpecialisedAssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpecialisedAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpecialisedAssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6304.SpecialisedAssemblyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_unbalanced_mass(self, design_entity: '_1995.UnbalancedMass') -> '_6328.UnbalancedMassAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.UnbalancedMassAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6328.UnbalancedMassAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_unbalanced_mass_load_case(self, design_entity_analysis: '_6184.UnbalancedMassLoadCase') -> '_6328.UnbalancedMassAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.UnbalancedMassLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.UnbalancedMassAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6328.UnbalancedMassAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_virtual_component(self, design_entity: '_1996.VirtualComponent') -> '_6330.VirtualComponentAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.VirtualComponentAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6330.VirtualComponentAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_virtual_component_load_case(self, design_entity_analysis: '_6185.VirtualComponentLoadCase') -> '_6330.VirtualComponentAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.VirtualComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.VirtualComponentAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6330.VirtualComponentAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_shaft(self, design_entity: '_1999.Shaft') -> '_6301.ShaftAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ShaftAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6301.ShaftAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_shaft_load_case(self, design_entity_analysis: '_6151.ShaftLoadCase') -> '_6301.ShaftAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ShaftAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6301.ShaftAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_concept_gear(self, design_entity: '_2037.ConceptGear') -> '_6239.ConceptGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6239.ConceptGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_concept_gear_load_case(self, design_entity_analysis: '_6052.ConceptGearLoadCase') -> '_6239.ConceptGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6239.ConceptGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_concept_gear_set(self, design_entity: '_2038.ConceptGearSet') -> '_6241.ConceptGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6241.ConceptGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_concept_gear_set_load_case(self, design_entity_analysis: '_6054.ConceptGearSetLoadCase') -> '_6241.ConceptGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6241.ConceptGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_face_gear(self, design_entity: '_2044.FaceGear') -> '_6260.FaceGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.FaceGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6260.FaceGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_face_gear_load_case(self, design_entity_analysis: '_6090.FaceGearLoadCase') -> '_6260.FaceGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.FaceGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6260.FaceGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_face_gear_set(self, design_entity: '_2045.FaceGearSet') -> '_6262.FaceGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.FaceGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6262.FaceGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_face_gear_set_load_case(self, design_entity_analysis: '_6092.FaceGearSetLoadCase') -> '_6262.FaceGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.FaceGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6262.FaceGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear(self, design_entity: '_2029.AGMAGleasonConicalGear') -> '_6214.AGMAGleasonConicalGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AGMAGleasonConicalGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6214.AGMAGleasonConicalGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_load_case(self, design_entity_analysis: '_6026.AGMAGleasonConicalGearLoadCase') -> '_6214.AGMAGleasonConicalGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AGMAGleasonConicalGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6214.AGMAGleasonConicalGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_set(self, design_entity: '_2030.AGMAGleasonConicalGearSet') -> '_6216.AGMAGleasonConicalGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AGMAGleasonConicalGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6216.AGMAGleasonConicalGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_set_load_case(self, design_entity_analysis: '_6028.AGMAGleasonConicalGearSetLoadCase') -> '_6216.AGMAGleasonConicalGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AGMAGleasonConicalGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6216.AGMAGleasonConicalGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_differential_gear(self, design_entity: '_2031.BevelDifferentialGear') -> '_6221.BevelDifferentialGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelDifferentialGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6221.BevelDifferentialGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_differential_gear_load_case(self, design_entity_analysis: '_6034.BevelDifferentialGearLoadCase') -> '_6221.BevelDifferentialGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelDifferentialGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6221.BevelDifferentialGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_differential_gear_set(self, design_entity: '_2032.BevelDifferentialGearSet') -> '_6223.BevelDifferentialGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelDifferentialGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6223.BevelDifferentialGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_differential_gear_set_load_case(self, design_entity_analysis: '_6036.BevelDifferentialGearSetLoadCase') -> '_6223.BevelDifferentialGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelDifferentialGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6223.BevelDifferentialGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_differential_planet_gear(self, design_entity: '_2033.BevelDifferentialPlanetGear') -> '_6224.BevelDifferentialPlanetGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelDifferentialPlanetGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6224.BevelDifferentialPlanetGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_differential_planet_gear_load_case(self, design_entity_analysis: '_6037.BevelDifferentialPlanetGearLoadCase') -> '_6224.BevelDifferentialPlanetGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelDifferentialPlanetGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6224.BevelDifferentialPlanetGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_differential_sun_gear(self, design_entity: '_2034.BevelDifferentialSunGear') -> '_6225.BevelDifferentialSunGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelDifferentialSunGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6225.BevelDifferentialSunGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_differential_sun_gear_load_case(self, design_entity_analysis: '_6038.BevelDifferentialSunGearLoadCase') -> '_6225.BevelDifferentialSunGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialSunGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelDifferentialSunGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6225.BevelDifferentialSunGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_gear(self, design_entity: '_2035.BevelGear') -> '_6226.BevelGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6226.BevelGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_gear_load_case(self, design_entity_analysis: '_6039.BevelGearLoadCase') -> '_6226.BevelGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6226.BevelGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_gear_set(self, design_entity: '_2036.BevelGearSet') -> '_6228.BevelGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6228.BevelGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_gear_set_load_case(self, design_entity_analysis: '_6041.BevelGearSetLoadCase') -> '_6228.BevelGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6228.BevelGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_conical_gear(self, design_entity: '_2039.ConicalGear') -> '_6242.ConicalGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConicalGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6242.ConicalGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_conical_gear_load_case(self, design_entity_analysis: '_6055.ConicalGearLoadCase') -> '_6242.ConicalGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConicalGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6242.ConicalGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_conical_gear_set(self, design_entity: '_2040.ConicalGearSet') -> '_6244.ConicalGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConicalGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6244.ConicalGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_conical_gear_set_load_case(self, design_entity_analysis: '_6059.ConicalGearSetLoadCase') -> '_6244.ConicalGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConicalGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6244.ConicalGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_cylindrical_gear(self, design_entity: '_2041.CylindricalGear') -> '_6253.CylindricalGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CylindricalGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6253.CylindricalGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_cylindrical_gear_load_case(self, design_entity_analysis: '_6068.CylindricalGearLoadCase') -> '_6253.CylindricalGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CylindricalGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6253.CylindricalGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_cylindrical_gear_set(self, design_entity: '_2042.CylindricalGearSet') -> '_6255.CylindricalGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CylindricalGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6255.CylindricalGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_cylindrical_gear_set_load_case(self, design_entity_analysis: '_6072.CylindricalGearSetLoadCase') -> '_6255.CylindricalGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CylindricalGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6255.CylindricalGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_cylindrical_planet_gear(self, design_entity: '_2043.CylindricalPlanetGear') -> '_6257.CylindricalPlanetGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CylindricalPlanetGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6257.CylindricalPlanetGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_cylindrical_planet_gear_load_case(self, design_entity_analysis: '_6073.CylindricalPlanetGearLoadCase') -> '_6257.CylindricalPlanetGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CylindricalPlanetGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6257.CylindricalPlanetGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_gear(self, design_entity: '_2046.Gear') -> '_6264.GearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.GearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6264.GearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_gear_load_case(self, design_entity_analysis: '_6095.GearLoadCase') -> '_6264.GearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.GearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6264.GearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_gear_set(self, design_entity: '_2048.GearSet') -> '_6266.GearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.GearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6266.GearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_gear_set_load_case(self, design_entity_analysis: '_6100.GearSetLoadCase') -> '_6266.GearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.GearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6266.GearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_hypoid_gear(self, design_entity: '_2050.HypoidGear') -> '_6268.HypoidGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.HypoidGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6268.HypoidGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_hypoid_gear_load_case(self, design_entity_analysis: '_6110.HypoidGearLoadCase') -> '_6268.HypoidGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.HypoidGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6268.HypoidGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_hypoid_gear_set(self, design_entity: '_2051.HypoidGearSet') -> '_6270.HypoidGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.HypoidGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6270.HypoidGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_hypoid_gear_set_load_case(self, design_entity_analysis: '_6112.HypoidGearSetLoadCase') -> '_6270.HypoidGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.HypoidGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6270.HypoidGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear(self, design_entity: '_2052.KlingelnbergCycloPalloidConicalGear') -> '_6273.KlingelnbergCycloPalloidConicalGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidConicalGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6273.KlingelnbergCycloPalloidConicalGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_load_case(self, design_entity_analysis: '_6116.KlingelnbergCycloPalloidConicalGearLoadCase') -> '_6273.KlingelnbergCycloPalloidConicalGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidConicalGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6273.KlingelnbergCycloPalloidConicalGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set(self, design_entity: '_2053.KlingelnbergCycloPalloidConicalGearSet') -> '_6275.KlingelnbergCycloPalloidConicalGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidConicalGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6275.KlingelnbergCycloPalloidConicalGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set_load_case(self, design_entity_analysis: '_6118.KlingelnbergCycloPalloidConicalGearSetLoadCase') -> '_6275.KlingelnbergCycloPalloidConicalGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidConicalGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6275.KlingelnbergCycloPalloidConicalGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear(self, design_entity: '_2054.KlingelnbergCycloPalloidHypoidGear') -> '_6276.KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6276.KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_load_case(self, design_entity_analysis: '_6119.KlingelnbergCycloPalloidHypoidGearLoadCase') -> '_6276.KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6276.KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set(self, design_entity: '_2055.KlingelnbergCycloPalloidHypoidGearSet') -> '_6278.KlingelnbergCycloPalloidHypoidGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidHypoidGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6278.KlingelnbergCycloPalloidHypoidGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set_load_case(self, design_entity_analysis: '_6121.KlingelnbergCycloPalloidHypoidGearSetLoadCase') -> '_6278.KlingelnbergCycloPalloidHypoidGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidHypoidGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6278.KlingelnbergCycloPalloidHypoidGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, design_entity: '_2056.KlingelnbergCycloPalloidSpiralBevelGear') -> '_6279.KlingelnbergCycloPalloidSpiralBevelGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidSpiralBevelGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6279.KlingelnbergCycloPalloidSpiralBevelGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_load_case(self, design_entity_analysis: '_6122.KlingelnbergCycloPalloidSpiralBevelGearLoadCase') -> '_6279.KlingelnbergCycloPalloidSpiralBevelGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidSpiralBevelGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6279.KlingelnbergCycloPalloidSpiralBevelGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, design_entity: '_2057.KlingelnbergCycloPalloidSpiralBevelGearSet') -> '_6281.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6281.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_load_case(self, design_entity_analysis: '_6124.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase') -> '_6281.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6281.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_planetary_gear_set(self, design_entity: '_2058.PlanetaryGearSet') -> '_6292.PlanetaryGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PlanetaryGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6292.PlanetaryGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_planetary_gear_set_load_case(self, design_entity_analysis: '_6137.PlanetaryGearSetLoadCase') -> '_6292.PlanetaryGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetaryGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PlanetaryGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6292.PlanetaryGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_spiral_bevel_gear(self, design_entity: '_2059.SpiralBevelGear') -> '_6305.SpiralBevelGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpiralBevelGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6305.SpiralBevelGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_load_case(self, design_entity_analysis: '_6155.SpiralBevelGearLoadCase') -> '_6305.SpiralBevelGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpiralBevelGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6305.SpiralBevelGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_set(self, design_entity: '_2060.SpiralBevelGearSet') -> '_6307.SpiralBevelGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpiralBevelGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6307.SpiralBevelGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_set_load_case(self, design_entity_analysis: '_6157.SpiralBevelGearSetLoadCase') -> '_6307.SpiralBevelGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpiralBevelGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6307.SpiralBevelGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear(self, design_entity: '_2061.StraightBevelDiffGear') -> '_6311.StraightBevelDiffGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelDiffGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6311.StraightBevelDiffGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_load_case(self, design_entity_analysis: '_6162.StraightBevelDiffGearLoadCase') -> '_6311.StraightBevelDiffGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelDiffGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6311.StraightBevelDiffGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_set(self, design_entity: '_2062.StraightBevelDiffGearSet') -> '_6313.StraightBevelDiffGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelDiffGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6313.StraightBevelDiffGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_set_load_case(self, design_entity_analysis: '_6164.StraightBevelDiffGearSetLoadCase') -> '_6313.StraightBevelDiffGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelDiffGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6313.StraightBevelDiffGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_gear(self, design_entity: '_2063.StraightBevelGear') -> '_6314.StraightBevelGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6314.StraightBevelGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_gear_load_case(self, design_entity_analysis: '_6165.StraightBevelGearLoadCase') -> '_6314.StraightBevelGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6314.StraightBevelGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_gear_set(self, design_entity: '_2064.StraightBevelGearSet') -> '_6316.StraightBevelGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6316.StraightBevelGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_gear_set_load_case(self, design_entity_analysis: '_6167.StraightBevelGearSetLoadCase') -> '_6316.StraightBevelGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6316.StraightBevelGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_planet_gear(self, design_entity: '_2065.StraightBevelPlanetGear') -> '_6317.StraightBevelPlanetGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelPlanetGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6317.StraightBevelPlanetGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_planet_gear_load_case(self, design_entity_analysis: '_6168.StraightBevelPlanetGearLoadCase') -> '_6317.StraightBevelPlanetGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelPlanetGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6317.StraightBevelPlanetGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_sun_gear(self, design_entity: '_2066.StraightBevelSunGear') -> '_6318.StraightBevelSunGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelSunGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6318.StraightBevelSunGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_sun_gear_load_case(self, design_entity_analysis: '_6169.StraightBevelSunGearLoadCase') -> '_6318.StraightBevelSunGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelSunGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelSunGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6318.StraightBevelSunGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_worm_gear(self, design_entity: '_2067.WormGear') -> '_6331.WormGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.WormGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6331.WormGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_worm_gear_load_case(self, design_entity_analysis: '_6186.WormGearLoadCase') -> '_6331.WormGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.WormGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6331.WormGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_worm_gear_set(self, design_entity: '_2068.WormGearSet') -> '_6333.WormGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.WormGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6333.WormGearSetAdvancedSystemDeflection)(method_result) if method_result else None
