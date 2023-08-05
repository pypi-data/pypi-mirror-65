'''_2153.py

AdvancedSystemDeflectionAnalysis
'''


from mastapy.system_model.analyses_and_results.static_loads import (
    _6210, _6211, _6213, _6157,
    _6156, _6055, _6068, _6067,
    _6073, _6072, _6086, _6085,
    _6088, _6089, _6166, _6172,
    _6170, _6168, _6182, _6181,
    _6193, _6192, _6194, _6195,
    _6199, _6200, _6201, _6087,
    _6054, _6069, _6082, _6137,
    _6158, _6169, _6174, _6057,
    _6075, _6113, _6185, _6062,
    _6079, _6049, _6092, _6133,
    _6139, _6142, _6145, _6178,
    _6188, _6209, _6212, _6119,
    _6155, _6066, _6071, _6084,
    _6180, _6198, _6045, _6046,
    _6053, _6065, _6064, _6070,
    _6083, _6098, _6111, _6115,
    _6052, _6123, _6135, _6147,
    _6148, _6150, _6152, _6154,
    _6161, _6164, _6165, _6171,
    _6175, _6206, _6207, _6173,
    _6074, _6076, _6112, _6114,
    _6048, _6050, _6056, _6058,
    _6059, _6060, _6061, _6063,
    _6077, _6081, _6090, _6094,
    _6095, _6117, _6122, _6132,
    _6134, _6138, _6140, _6141,
    _6143, _6144, _6146, _6159,
    _6177, _6179, _6184, _6186,
    _6187, _6189, _6190, _6191,
    _6208
)
from mastapy.system_model.analyses_and_results.advanced_system_deflections import (
    _6355, _6356, _6358, _6310,
    _6312, _6242, _6253, _6255,
    _6258, _6260, _6269, _6271,
    _6272, _6274, _6318, _6324,
    _6319, _6320, _6330, _6332,
    _6341, _6342, _6343, _6344,
    _6345, _6347, _6348, _6273,
    _6241, _6256, _6267, _6294,
    _6313, _6321, _6325, _6244,
    _6262, _6283, _6334, _6249,
    _6265, _6237, _6276, _6291,
    _6296, _6299, _6302, _6328,
    _6337, _6354, _6357, _6287,
    _6311, _6254, _6259, _6270,
    _6331, _6346, _6231, _6232,
    _6240, _6251, _6252, _6257,
    _6268, _6280, _6281, _6285,
    _6239, _6289, _6293, _6305,
    _6306, _6307, _6308, _6309,
    _6315, _6316, _6317, _6322,
    _6326, _6350, _6352, _6323,
    _6261, _6263, _6282, _6284,
    _6236, _6238, _6243, _6245,
    _6246, _6247, _6248, _6250,
    _6264, _6266, _6275, _6277,
    _6279, _6286, _6288, _6290,
    _6292, _6295, _6297, _6298,
    _6300, _6301, _6303, _6314,
    _6327, _6329, _6333, _6335,
    _6336, _6338, _6339, _6340,
    _6353
)
from mastapy._internal import constructor
from mastapy.system_model.part_model.gears import (
    _2091, _2092, _2059, _2060,
    _2066, _2067, _2051, _2052,
    _2053, _2054, _2055, _2056,
    _2057, _2058, _2061, _2062,
    _2063, _2064, _2065, _2068,
    _2070, _2072, _2073, _2074,
    _2075, _2076, _2077, _2078,
    _2079, _2080, _2081, _2082,
    _2083, _2084, _2085, _2086,
    _2087, _2088, _2089, _2090
)
from mastapy.system_model.part_model.couplings import (
    _2121, _2122, _2110, _2112,
    _2113, _2115, _2116, _2117,
    _2118, _2119, _2120, _2123,
    _2131, _2129, _2130, _2132,
    _2133, _2134, _2136, _2137,
    _2138, _2139, _2140, _2142
)
from mastapy.system_model.connections_and_sockets import (
    _1836, _1831, _1832, _1835,
    _1844, _1847, _1851, _1855
)
from mastapy.system_model.connections_and_sockets.gears import (
    _1861, _1865, _1871, _1885,
    _1863, _1867, _1859, _1869,
    _1875, _1878, _1879, _1880,
    _1883, _1887, _1889, _1891,
    _1873
)
from mastapy.system_model.connections_and_sockets.couplings import (
    _1899, _1893, _1895, _1897,
    _1901, _1903
)
from mastapy.system_model.part_model import (
    _1980, _1981, _1984, _1986,
    _1987, _1988, _1991, _1992,
    _1995, _1996, _1979, _1997,
    _2000, _2003, _2004, _2005,
    _2007, _2008, _2009, _2011,
    _2012, _2014, _2016, _2017,
    _2018
)
from mastapy.system_model.part_model.shaft_model import _2021
from mastapy.system_model.analyses_and_results import _2152
from mastapy._internal.python_net import python_net_import

_ADVANCED_SYSTEM_DEFLECTION_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'AdvancedSystemDeflectionAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('AdvancedSystemDeflectionAnalysis',)


class AdvancedSystemDeflectionAnalysis(_2152.SingleAnalysis):
    '''AdvancedSystemDeflectionAnalysis

    This is a mastapy class.
    '''

    TYPE = _ADVANCED_SYSTEM_DEFLECTION_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AdvancedSystemDeflectionAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    def results_for_worm_gear_set_load_case(self, design_entity_analysis: '_6210.WormGearSetLoadCase') -> '_6355.WormGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.WormGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6355.WormGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_zerol_bevel_gear(self, design_entity: '_2091.ZerolBevelGear') -> '_6356.ZerolBevelGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ZerolBevelGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6356.ZerolBevelGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_load_case(self, design_entity_analysis: '_6211.ZerolBevelGearLoadCase') -> '_6356.ZerolBevelGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ZerolBevelGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6356.ZerolBevelGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_set(self, design_entity: '_2092.ZerolBevelGearSet') -> '_6358.ZerolBevelGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ZerolBevelGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6358.ZerolBevelGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_set_load_case(self, design_entity_analysis: '_6213.ZerolBevelGearSetLoadCase') -> '_6358.ZerolBevelGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ZerolBevelGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6358.ZerolBevelGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling(self, design_entity: '_2121.PartToPartShearCoupling') -> '_6310.PartToPartShearCouplingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCoupling)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PartToPartShearCouplingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6310.PartToPartShearCouplingAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_load_case(self, design_entity_analysis: '_6157.PartToPartShearCouplingLoadCase') -> '_6310.PartToPartShearCouplingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PartToPartShearCouplingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6310.PartToPartShearCouplingAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_half(self, design_entity: '_2122.PartToPartShearCouplingHalf') -> '_6312.PartToPartShearCouplingHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PartToPartShearCouplingHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6312.PartToPartShearCouplingHalfAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_half_load_case(self, design_entity_analysis: '_6156.PartToPartShearCouplingHalfLoadCase') -> '_6312.PartToPartShearCouplingHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PartToPartShearCouplingHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6312.PartToPartShearCouplingHalfAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_belt_drive(self, design_entity: '_2110.BeltDrive') -> '_6242.BeltDriveAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BeltDriveAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6242.BeltDriveAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_belt_drive_load_case(self, design_entity_analysis: '_6055.BeltDriveLoadCase') -> '_6242.BeltDriveAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BeltDriveLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BeltDriveAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6242.BeltDriveAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_clutch(self, design_entity: '_2112.Clutch') -> '_6253.ClutchAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ClutchAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6253.ClutchAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_clutch_load_case(self, design_entity_analysis: '_6068.ClutchLoadCase') -> '_6253.ClutchAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ClutchAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6253.ClutchAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_clutch_half(self, design_entity: '_2113.ClutchHalf') -> '_6255.ClutchHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ClutchHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6255.ClutchHalfAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_clutch_half_load_case(self, design_entity_analysis: '_6067.ClutchHalfLoadCase') -> '_6255.ClutchHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ClutchHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6255.ClutchHalfAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_concept_coupling(self, design_entity: '_2115.ConceptCoupling') -> '_6258.ConceptCouplingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptCouplingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6258.ConceptCouplingAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_concept_coupling_load_case(self, design_entity_analysis: '_6073.ConceptCouplingLoadCase') -> '_6258.ConceptCouplingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptCouplingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6258.ConceptCouplingAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_concept_coupling_half(self, design_entity: '_2116.ConceptCouplingHalf') -> '_6260.ConceptCouplingHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptCouplingHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6260.ConceptCouplingHalfAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_concept_coupling_half_load_case(self, design_entity_analysis: '_6072.ConceptCouplingHalfLoadCase') -> '_6260.ConceptCouplingHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptCouplingHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6260.ConceptCouplingHalfAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_coupling(self, design_entity: '_2117.Coupling') -> '_6269.CouplingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CouplingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6269.CouplingAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_coupling_load_case(self, design_entity_analysis: '_6086.CouplingLoadCase') -> '_6269.CouplingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CouplingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6269.CouplingAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_coupling_half(self, design_entity: '_2118.CouplingHalf') -> '_6271.CouplingHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CouplingHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6271.CouplingHalfAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_coupling_half_load_case(self, design_entity_analysis: '_6085.CouplingHalfLoadCase') -> '_6271.CouplingHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CouplingHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6271.CouplingHalfAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_cvt(self, design_entity: '_2119.CVT') -> '_6272.CVTAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CVTAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6272.CVTAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_cvt_load_case(self, design_entity_analysis: '_6088.CVTLoadCase') -> '_6272.CVTAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CVTAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6272.CVTAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_cvt_pulley(self, design_entity: '_2120.CVTPulley') -> '_6274.CVTPulleyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CVTPulleyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6274.CVTPulleyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_cvt_pulley_load_case(self, design_entity_analysis: '_6089.CVTPulleyLoadCase') -> '_6274.CVTPulleyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTPulleyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CVTPulleyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6274.CVTPulleyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_pulley(self, design_entity: '_2123.Pulley') -> '_6318.PulleyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PulleyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6318.PulleyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_pulley_load_case(self, design_entity_analysis: '_6166.PulleyLoadCase') -> '_6318.PulleyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PulleyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PulleyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6318.PulleyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_shaft_hub_connection(self, design_entity: '_2131.ShaftHubConnection') -> '_6324.ShaftHubConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ShaftHubConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6324.ShaftHubConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_shaft_hub_connection_load_case(self, design_entity_analysis: '_6172.ShaftHubConnectionLoadCase') -> '_6324.ShaftHubConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftHubConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ShaftHubConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6324.ShaftHubConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_rolling_ring(self, design_entity: '_2129.RollingRing') -> '_6319.RollingRingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.RollingRingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6319.RollingRingAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_rolling_ring_load_case(self, design_entity_analysis: '_6170.RollingRingLoadCase') -> '_6319.RollingRingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.RollingRingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6319.RollingRingAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_rolling_ring_assembly(self, design_entity: '_2130.RollingRingAssembly') -> '_6320.RollingRingAssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.RollingRingAssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6320.RollingRingAssemblyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_rolling_ring_assembly_load_case(self, design_entity_analysis: '_6168.RollingRingAssemblyLoadCase') -> '_6320.RollingRingAssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.RollingRingAssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6320.RollingRingAssemblyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_spring_damper(self, design_entity: '_2132.SpringDamper') -> '_6330.SpringDamperAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpringDamperAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6330.SpringDamperAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_spring_damper_load_case(self, design_entity_analysis: '_6182.SpringDamperLoadCase') -> '_6330.SpringDamperAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpringDamperAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6330.SpringDamperAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_spring_damper_half(self, design_entity: '_2133.SpringDamperHalf') -> '_6332.SpringDamperHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpringDamperHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6332.SpringDamperHalfAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_spring_damper_half_load_case(self, design_entity_analysis: '_6181.SpringDamperHalfLoadCase') -> '_6332.SpringDamperHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpringDamperHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6332.SpringDamperHalfAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_synchroniser(self, design_entity: '_2134.Synchroniser') -> '_6341.SynchroniserAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SynchroniserAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6341.SynchroniserAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_synchroniser_load_case(self, design_entity_analysis: '_6193.SynchroniserLoadCase') -> '_6341.SynchroniserAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SynchroniserAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6341.SynchroniserAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_synchroniser_half(self, design_entity: '_2136.SynchroniserHalf') -> '_6342.SynchroniserHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SynchroniserHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6342.SynchroniserHalfAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_synchroniser_half_load_case(self, design_entity_analysis: '_6192.SynchroniserHalfLoadCase') -> '_6342.SynchroniserHalfAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserHalfLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SynchroniserHalfAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6342.SynchroniserHalfAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_synchroniser_part(self, design_entity: '_2137.SynchroniserPart') -> '_6343.SynchroniserPartAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SynchroniserPartAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6343.SynchroniserPartAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_synchroniser_part_load_case(self, design_entity_analysis: '_6194.SynchroniserPartLoadCase') -> '_6343.SynchroniserPartAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserPartLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SynchroniserPartAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6343.SynchroniserPartAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_synchroniser_sleeve(self, design_entity: '_2138.SynchroniserSleeve') -> '_6344.SynchroniserSleeveAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SynchroniserSleeveAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6344.SynchroniserSleeveAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_synchroniser_sleeve_load_case(self, design_entity_analysis: '_6195.SynchroniserSleeveLoadCase') -> '_6344.SynchroniserSleeveAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SynchroniserSleeveLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SynchroniserSleeveAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6344.SynchroniserSleeveAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_torque_converter(self, design_entity: '_2139.TorqueConverter') -> '_6345.TorqueConverterAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.TorqueConverterAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6345.TorqueConverterAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_torque_converter_load_case(self, design_entity_analysis: '_6199.TorqueConverterLoadCase') -> '_6345.TorqueConverterAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.TorqueConverterAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6345.TorqueConverterAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_torque_converter_pump(self, design_entity: '_2140.TorqueConverterPump') -> '_6347.TorqueConverterPumpAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.TorqueConverterPumpAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6347.TorqueConverterPumpAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_torque_converter_pump_load_case(self, design_entity_analysis: '_6200.TorqueConverterPumpLoadCase') -> '_6347.TorqueConverterPumpAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterPumpLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.TorqueConverterPumpAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6347.TorqueConverterPumpAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_torque_converter_turbine(self, design_entity: '_2142.TorqueConverterTurbine') -> '_6348.TorqueConverterTurbineAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.TorqueConverterTurbineAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6348.TorqueConverterTurbineAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_torque_converter_turbine_load_case(self, design_entity_analysis: '_6201.TorqueConverterTurbineLoadCase') -> '_6348.TorqueConverterTurbineAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterTurbineLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.TorqueConverterTurbineAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6348.TorqueConverterTurbineAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_cvt_belt_connection(self, design_entity: '_1836.CVTBeltConnection') -> '_6273.CVTBeltConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CVTBeltConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6273.CVTBeltConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_cvt_belt_connection_load_case(self, design_entity_analysis: '_6087.CVTBeltConnectionLoadCase') -> '_6273.CVTBeltConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CVTBeltConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CVTBeltConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6273.CVTBeltConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_belt_connection(self, design_entity: '_1831.BeltConnection') -> '_6241.BeltConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BeltConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6241.BeltConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_belt_connection_load_case(self, design_entity_analysis: '_6054.BeltConnectionLoadCase') -> '_6241.BeltConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BeltConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BeltConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6241.BeltConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_coaxial_connection(self, design_entity: '_1832.CoaxialConnection') -> '_6256.CoaxialConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CoaxialConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6256.CoaxialConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_coaxial_connection_load_case(self, design_entity_analysis: '_6069.CoaxialConnectionLoadCase') -> '_6256.CoaxialConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CoaxialConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CoaxialConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6256.CoaxialConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_connection(self, design_entity: '_1835.Connection') -> '_6267.ConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6267.ConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_connection_load_case(self, design_entity_analysis: '_6082.ConnectionLoadCase') -> '_6267.ConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6267.ConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_inter_mountable_component_connection(self, design_entity: '_1844.InterMountableComponentConnection') -> '_6294.InterMountableComponentConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.InterMountableComponentConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6294.InterMountableComponentConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_inter_mountable_component_connection_load_case(self, design_entity_analysis: '_6137.InterMountableComponentConnectionLoadCase') -> '_6294.InterMountableComponentConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.InterMountableComponentConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.InterMountableComponentConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6294.InterMountableComponentConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_planetary_connection(self, design_entity: '_1847.PlanetaryConnection') -> '_6313.PlanetaryConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PlanetaryConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6313.PlanetaryConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_planetary_connection_load_case(self, design_entity_analysis: '_6158.PlanetaryConnectionLoadCase') -> '_6313.PlanetaryConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetaryConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PlanetaryConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6313.PlanetaryConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_rolling_ring_connection(self, design_entity: '_1851.RollingRingConnection') -> '_6321.RollingRingConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.RollingRingConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6321.RollingRingConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_rolling_ring_connection_load_case(self, design_entity_analysis: '_6169.RollingRingConnectionLoadCase') -> '_6321.RollingRingConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RollingRingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.RollingRingConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6321.RollingRingConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_shaft_to_mountable_component_connection(self, design_entity: '_1855.ShaftToMountableComponentConnection') -> '_6325.ShaftToMountableComponentConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ShaftToMountableComponentConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6325.ShaftToMountableComponentConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_shaft_to_mountable_component_connection_load_case(self, design_entity_analysis: '_6174.ShaftToMountableComponentConnectionLoadCase') -> '_6325.ShaftToMountableComponentConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftToMountableComponentConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ShaftToMountableComponentConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6325.ShaftToMountableComponentConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_differential_gear_mesh(self, design_entity: '_1861.BevelDifferentialGearMesh') -> '_6244.BevelDifferentialGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelDifferentialGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6244.BevelDifferentialGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_differential_gear_mesh_load_case(self, design_entity_analysis: '_6057.BevelDifferentialGearMeshLoadCase') -> '_6244.BevelDifferentialGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelDifferentialGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6244.BevelDifferentialGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_concept_gear_mesh(self, design_entity: '_1865.ConceptGearMesh') -> '_6262.ConceptGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6262.ConceptGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_concept_gear_mesh_load_case(self, design_entity_analysis: '_6075.ConceptGearMeshLoadCase') -> '_6262.ConceptGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6262.ConceptGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_face_gear_mesh(self, design_entity: '_1871.FaceGearMesh') -> '_6283.FaceGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.FaceGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6283.FaceGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_face_gear_mesh_load_case(self, design_entity_analysis: '_6113.FaceGearMeshLoadCase') -> '_6283.FaceGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.FaceGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6283.FaceGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_mesh(self, design_entity: '_1885.StraightBevelDiffGearMesh') -> '_6334.StraightBevelDiffGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelDiffGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6334.StraightBevelDiffGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_mesh_load_case(self, design_entity_analysis: '_6185.StraightBevelDiffGearMeshLoadCase') -> '_6334.StraightBevelDiffGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelDiffGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6334.StraightBevelDiffGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_gear_mesh(self, design_entity: '_1863.BevelGearMesh') -> '_6249.BevelGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6249.BevelGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6062.BevelGearMeshLoadCase') -> '_6249.BevelGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6249.BevelGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_conical_gear_mesh(self, design_entity: '_1867.ConicalGearMesh') -> '_6265.ConicalGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConicalGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6265.ConicalGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_conical_gear_mesh_load_case(self, design_entity_analysis: '_6079.ConicalGearMeshLoadCase') -> '_6265.ConicalGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConicalGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6265.ConicalGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_mesh(self, design_entity: '_1859.AGMAGleasonConicalGearMesh') -> '_6237.AGMAGleasonConicalGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AGMAGleasonConicalGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6237.AGMAGleasonConicalGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_mesh_load_case(self, design_entity_analysis: '_6049.AGMAGleasonConicalGearMeshLoadCase') -> '_6237.AGMAGleasonConicalGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AGMAGleasonConicalGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6237.AGMAGleasonConicalGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_cylindrical_gear_mesh(self, design_entity: '_1869.CylindricalGearMesh') -> '_6276.CylindricalGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CylindricalGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6276.CylindricalGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_cylindrical_gear_mesh_load_case(self, design_entity_analysis: '_6092.CylindricalGearMeshLoadCase') -> '_6276.CylindricalGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CylindricalGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6276.CylindricalGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_hypoid_gear_mesh(self, design_entity: '_1875.HypoidGearMesh') -> '_6291.HypoidGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.HypoidGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6291.HypoidGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_hypoid_gear_mesh_load_case(self, design_entity_analysis: '_6133.HypoidGearMeshLoadCase') -> '_6291.HypoidGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.HypoidGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6291.HypoidGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh(self, design_entity: '_1878.KlingelnbergCycloPalloidConicalGearMesh') -> '_6296.KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6296.KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh_load_case(self, design_entity_analysis: '_6139.KlingelnbergCycloPalloidConicalGearMeshLoadCase') -> '_6296.KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6296.KlingelnbergCycloPalloidConicalGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, design_entity: '_1879.KlingelnbergCycloPalloidHypoidGearMesh') -> '_6299.KlingelnbergCycloPalloidHypoidGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidHypoidGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6299.KlingelnbergCycloPalloidHypoidGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh_load_case(self, design_entity_analysis: '_6142.KlingelnbergCycloPalloidHypoidGearMeshLoadCase') -> '_6299.KlingelnbergCycloPalloidHypoidGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidHypoidGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6299.KlingelnbergCycloPalloidHypoidGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, design_entity: '_1880.KlingelnbergCycloPalloidSpiralBevelGearMesh') -> '_6302.KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6302.KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6145.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase') -> '_6302.KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6302.KlingelnbergCycloPalloidSpiralBevelGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_mesh(self, design_entity: '_1883.SpiralBevelGearMesh') -> '_6328.SpiralBevelGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpiralBevelGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6328.SpiralBevelGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6178.SpiralBevelGearMeshLoadCase') -> '_6328.SpiralBevelGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpiralBevelGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6328.SpiralBevelGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_gear_mesh(self, design_entity: '_1887.StraightBevelGearMesh') -> '_6337.StraightBevelGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6337.StraightBevelGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6188.StraightBevelGearMeshLoadCase') -> '_6337.StraightBevelGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6337.StraightBevelGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_worm_gear_mesh(self, design_entity: '_1889.WormGearMesh') -> '_6354.WormGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.WormGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6354.WormGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_worm_gear_mesh_load_case(self, design_entity_analysis: '_6209.WormGearMeshLoadCase') -> '_6354.WormGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.WormGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6354.WormGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_mesh(self, design_entity: '_1891.ZerolBevelGearMesh') -> '_6357.ZerolBevelGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ZerolBevelGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6357.ZerolBevelGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_zerol_bevel_gear_mesh_load_case(self, design_entity_analysis: '_6212.ZerolBevelGearMeshLoadCase') -> '_6357.ZerolBevelGearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ZerolBevelGearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ZerolBevelGearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6357.ZerolBevelGearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_gear_mesh(self, design_entity: '_1873.GearMesh') -> '_6287.GearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.GearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6287.GearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_gear_mesh_load_case(self, design_entity_analysis: '_6119.GearMeshLoadCase') -> '_6287.GearMeshAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearMeshLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.GearMeshAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6287.GearMeshAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_connection(self, design_entity: '_1899.PartToPartShearCouplingConnection') -> '_6311.PartToPartShearCouplingConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PartToPartShearCouplingConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6311.PartToPartShearCouplingConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_part_to_part_shear_coupling_connection_load_case(self, design_entity_analysis: '_6155.PartToPartShearCouplingConnectionLoadCase') -> '_6311.PartToPartShearCouplingConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartToPartShearCouplingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PartToPartShearCouplingConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6311.PartToPartShearCouplingConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_clutch_connection(self, design_entity: '_1893.ClutchConnection') -> '_6254.ClutchConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ClutchConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6254.ClutchConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_clutch_connection_load_case(self, design_entity_analysis: '_6066.ClutchConnectionLoadCase') -> '_6254.ClutchConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ClutchConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ClutchConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6254.ClutchConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_concept_coupling_connection(self, design_entity: '_1895.ConceptCouplingConnection') -> '_6259.ConceptCouplingConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptCouplingConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6259.ConceptCouplingConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_concept_coupling_connection_load_case(self, design_entity_analysis: '_6071.ConceptCouplingConnectionLoadCase') -> '_6259.ConceptCouplingConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptCouplingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptCouplingConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6259.ConceptCouplingConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_coupling_connection(self, design_entity: '_1897.CouplingConnection') -> '_6270.CouplingConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CouplingConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6270.CouplingConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_coupling_connection_load_case(self, design_entity_analysis: '_6084.CouplingConnectionLoadCase') -> '_6270.CouplingConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CouplingConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CouplingConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6270.CouplingConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_spring_damper_connection(self, design_entity: '_1901.SpringDamperConnection') -> '_6331.SpringDamperConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpringDamperConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6331.SpringDamperConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_spring_damper_connection_load_case(self, design_entity_analysis: '_6180.SpringDamperConnectionLoadCase') -> '_6331.SpringDamperConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpringDamperConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpringDamperConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6331.SpringDamperConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_torque_converter_connection(self, design_entity: '_1903.TorqueConverterConnection') -> '_6346.TorqueConverterConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.TorqueConverterConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6346.TorqueConverterConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_torque_converter_connection_load_case(self, design_entity_analysis: '_6198.TorqueConverterConnectionLoadCase') -> '_6346.TorqueConverterConnectionAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.TorqueConverterConnectionLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.TorqueConverterConnectionAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6346.TorqueConverterConnectionAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_abstract_assembly(self, design_entity: '_1980.AbstractAssembly') -> '_6231.AbstractAssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AbstractAssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6231.AbstractAssemblyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_abstract_assembly_load_case(self, design_entity_analysis: '_6045.AbstractAssemblyLoadCase') -> '_6231.AbstractAssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AbstractAssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6231.AbstractAssemblyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_abstract_shaft_or_housing(self, design_entity: '_1981.AbstractShaftOrHousing') -> '_6232.AbstractShaftOrHousingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AbstractShaftOrHousingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6232.AbstractShaftOrHousingAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_abstract_shaft_or_housing_load_case(self, design_entity_analysis: '_6046.AbstractShaftOrHousingLoadCase') -> '_6232.AbstractShaftOrHousingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AbstractShaftOrHousingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AbstractShaftOrHousingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6232.AbstractShaftOrHousingAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bearing(self, design_entity: '_1984.Bearing') -> '_6240.BearingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BearingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6240.BearingAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bearing_load_case(self, design_entity_analysis: '_6053.BearingLoadCase') -> '_6240.BearingAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BearingLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BearingAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6240.BearingAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bolt(self, design_entity: '_1986.Bolt') -> '_6251.BoltAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BoltAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6251.BoltAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bolt_load_case(self, design_entity_analysis: '_6065.BoltLoadCase') -> '_6251.BoltAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BoltLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BoltAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6251.BoltAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bolted_joint(self, design_entity: '_1987.BoltedJoint') -> '_6252.BoltedJointAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BoltedJointAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6252.BoltedJointAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bolted_joint_load_case(self, design_entity_analysis: '_6064.BoltedJointLoadCase') -> '_6252.BoltedJointAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BoltedJointLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BoltedJointAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6252.BoltedJointAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_component(self, design_entity: '_1988.Component') -> '_6257.ComponentAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Component)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ComponentAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6257.ComponentAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_component_load_case(self, design_entity_analysis: '_6070.ComponentLoadCase') -> '_6257.ComponentAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ComponentAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6257.ComponentAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_connector(self, design_entity: '_1991.Connector') -> '_6268.ConnectorAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Connector)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConnectorAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6268.ConnectorAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_connector_load_case(self, design_entity_analysis: '_6083.ConnectorLoadCase') -> '_6268.ConnectorAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConnectorLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConnectorAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6268.ConnectorAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_datum(self, design_entity: '_1992.Datum') -> '_6280.DatumAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Datum)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.DatumAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6280.DatumAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_datum_load_case(self, design_entity_analysis: '_6098.DatumLoadCase') -> '_6280.DatumAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.DatumLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.DatumAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6280.DatumAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_external_cad_model(self, design_entity: '_1995.ExternalCADModel') -> '_6281.ExternalCADModelAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ExternalCADModelAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6281.ExternalCADModelAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_external_cad_model_load_case(self, design_entity_analysis: '_6111.ExternalCADModelLoadCase') -> '_6281.ExternalCADModelAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ExternalCADModelLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ExternalCADModelAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6281.ExternalCADModelAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_flexible_pin_assembly(self, design_entity: '_1996.FlexiblePinAssembly') -> '_6285.FlexiblePinAssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.FlexiblePinAssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6285.FlexiblePinAssemblyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_flexible_pin_assembly_load_case(self, design_entity_analysis: '_6115.FlexiblePinAssemblyLoadCase') -> '_6285.FlexiblePinAssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FlexiblePinAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.FlexiblePinAssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6285.FlexiblePinAssemblyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_assembly(self, design_entity: '_1979.Assembly') -> '_6239.AssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6239.AssemblyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_assembly_load_case(self, design_entity_analysis: '_6052.AssemblyLoadCase') -> '_6239.AssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6239.AssemblyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_guide_dxf_model(self, design_entity: '_1997.GuideDxfModel') -> '_6289.GuideDxfModelAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.GuideDxfModelAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6289.GuideDxfModelAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_guide_dxf_model_load_case(self, design_entity_analysis: '_6123.GuideDxfModelLoadCase') -> '_6289.GuideDxfModelAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GuideDxfModelLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.GuideDxfModelAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6289.GuideDxfModelAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_imported_fe_component(self, design_entity: '_2000.ImportedFEComponent') -> '_6293.ImportedFEComponentAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ImportedFEComponent)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ImportedFEComponentAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6293.ImportedFEComponentAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_imported_fe_component_load_case(self, design_entity_analysis: '_6135.ImportedFEComponentLoadCase') -> '_6293.ImportedFEComponentAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ImportedFEComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ImportedFEComponentAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6293.ImportedFEComponentAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_mass_disc(self, design_entity: '_2003.MassDisc') -> '_6305.MassDiscAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.MassDiscAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6305.MassDiscAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_mass_disc_load_case(self, design_entity_analysis: '_6147.MassDiscLoadCase') -> '_6305.MassDiscAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MassDiscLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.MassDiscAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6305.MassDiscAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_measurement_component(self, design_entity: '_2004.MeasurementComponent') -> '_6306.MeasurementComponentAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.MeasurementComponentAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6306.MeasurementComponentAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_measurement_component_load_case(self, design_entity_analysis: '_6148.MeasurementComponentLoadCase') -> '_6306.MeasurementComponentAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MeasurementComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.MeasurementComponentAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6306.MeasurementComponentAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_mountable_component(self, design_entity: '_2005.MountableComponent') -> '_6307.MountableComponentAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.MountableComponentAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6307.MountableComponentAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_mountable_component_load_case(self, design_entity_analysis: '_6150.MountableComponentLoadCase') -> '_6307.MountableComponentAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.MountableComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.MountableComponentAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6307.MountableComponentAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_oil_seal(self, design_entity: '_2007.OilSeal') -> '_6308.OilSealAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.OilSealAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6308.OilSealAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_oil_seal_load_case(self, design_entity_analysis: '_6152.OilSealLoadCase') -> '_6308.OilSealAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.OilSealLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.OilSealAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6308.OilSealAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_part(self, design_entity: '_2008.Part') -> '_6309.PartAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Part)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PartAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6309.PartAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_part_load_case(self, design_entity_analysis: '_6154.PartLoadCase') -> '_6309.PartAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PartLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PartAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6309.PartAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_planet_carrier(self, design_entity: '_2009.PlanetCarrier') -> '_6315.PlanetCarrierAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PlanetCarrierAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6315.PlanetCarrierAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_planet_carrier_load_case(self, design_entity_analysis: '_6161.PlanetCarrierLoadCase') -> '_6315.PlanetCarrierAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetCarrierLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PlanetCarrierAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6315.PlanetCarrierAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_point_load(self, design_entity: '_2011.PointLoad') -> '_6316.PointLoadAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PointLoadAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6316.PointLoadAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_point_load_load_case(self, design_entity_analysis: '_6164.PointLoadLoadCase') -> '_6316.PointLoadAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PointLoadLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PointLoadAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6316.PointLoadAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_power_load(self, design_entity: '_2012.PowerLoad') -> '_6317.PowerLoadAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PowerLoadAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6317.PowerLoadAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_power_load_load_case(self, design_entity_analysis: '_6165.PowerLoadLoadCase') -> '_6317.PowerLoadAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PowerLoadLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PowerLoadAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6317.PowerLoadAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_root_assembly(self, design_entity: '_2014.RootAssembly') -> '_6322.RootAssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.RootAssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6322.RootAssemblyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_root_assembly_load_case(self, design_entity_analysis: '_6171.RootAssemblyLoadCase') -> '_6322.RootAssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.RootAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.RootAssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6322.RootAssemblyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_specialised_assembly(self, design_entity: '_2016.SpecialisedAssembly') -> '_6326.SpecialisedAssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpecialisedAssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6326.SpecialisedAssemblyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_specialised_assembly_load_case(self, design_entity_analysis: '_6175.SpecialisedAssemblyLoadCase') -> '_6326.SpecialisedAssemblyAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpecialisedAssemblyLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpecialisedAssemblyAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6326.SpecialisedAssemblyAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_unbalanced_mass(self, design_entity: '_2017.UnbalancedMass') -> '_6350.UnbalancedMassAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.UnbalancedMassAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6350.UnbalancedMassAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_unbalanced_mass_load_case(self, design_entity_analysis: '_6206.UnbalancedMassLoadCase') -> '_6350.UnbalancedMassAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.UnbalancedMassLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.UnbalancedMassAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6350.UnbalancedMassAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_virtual_component(self, design_entity: '_2018.VirtualComponent') -> '_6352.VirtualComponentAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.VirtualComponentAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6352.VirtualComponentAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_virtual_component_load_case(self, design_entity_analysis: '_6207.VirtualComponentLoadCase') -> '_6352.VirtualComponentAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.VirtualComponentLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.VirtualComponentAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6352.VirtualComponentAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_shaft(self, design_entity: '_2021.Shaft') -> '_6323.ShaftAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ShaftAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6323.ShaftAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_shaft_load_case(self, design_entity_analysis: '_6173.ShaftLoadCase') -> '_6323.ShaftAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ShaftLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ShaftAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6323.ShaftAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_concept_gear(self, design_entity: '_2059.ConceptGear') -> '_6261.ConceptGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6261.ConceptGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_concept_gear_load_case(self, design_entity_analysis: '_6074.ConceptGearLoadCase') -> '_6261.ConceptGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6261.ConceptGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_concept_gear_set(self, design_entity: '_2060.ConceptGearSet') -> '_6263.ConceptGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6263.ConceptGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_concept_gear_set_load_case(self, design_entity_analysis: '_6076.ConceptGearSetLoadCase') -> '_6263.ConceptGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConceptGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConceptGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6263.ConceptGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_face_gear(self, design_entity: '_2066.FaceGear') -> '_6282.FaceGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.FaceGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6282.FaceGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_face_gear_load_case(self, design_entity_analysis: '_6112.FaceGearLoadCase') -> '_6282.FaceGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.FaceGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6282.FaceGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_face_gear_set(self, design_entity: '_2067.FaceGearSet') -> '_6284.FaceGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.FaceGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6284.FaceGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_face_gear_set_load_case(self, design_entity_analysis: '_6114.FaceGearSetLoadCase') -> '_6284.FaceGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.FaceGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.FaceGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6284.FaceGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear(self, design_entity: '_2051.AGMAGleasonConicalGear') -> '_6236.AGMAGleasonConicalGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AGMAGleasonConicalGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6236.AGMAGleasonConicalGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_load_case(self, design_entity_analysis: '_6048.AGMAGleasonConicalGearLoadCase') -> '_6236.AGMAGleasonConicalGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AGMAGleasonConicalGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6236.AGMAGleasonConicalGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_set(self, design_entity: '_2052.AGMAGleasonConicalGearSet') -> '_6238.AGMAGleasonConicalGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AGMAGleasonConicalGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6238.AGMAGleasonConicalGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_agma_gleason_conical_gear_set_load_case(self, design_entity_analysis: '_6050.AGMAGleasonConicalGearSetLoadCase') -> '_6238.AGMAGleasonConicalGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.AGMAGleasonConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.AGMAGleasonConicalGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6238.AGMAGleasonConicalGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_differential_gear(self, design_entity: '_2053.BevelDifferentialGear') -> '_6243.BevelDifferentialGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelDifferentialGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6243.BevelDifferentialGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_differential_gear_load_case(self, design_entity_analysis: '_6056.BevelDifferentialGearLoadCase') -> '_6243.BevelDifferentialGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelDifferentialGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6243.BevelDifferentialGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_differential_gear_set(self, design_entity: '_2054.BevelDifferentialGearSet') -> '_6245.BevelDifferentialGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelDifferentialGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6245.BevelDifferentialGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_differential_gear_set_load_case(self, design_entity_analysis: '_6058.BevelDifferentialGearSetLoadCase') -> '_6245.BevelDifferentialGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelDifferentialGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6245.BevelDifferentialGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_differential_planet_gear(self, design_entity: '_2055.BevelDifferentialPlanetGear') -> '_6246.BevelDifferentialPlanetGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelDifferentialPlanetGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6246.BevelDifferentialPlanetGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_differential_planet_gear_load_case(self, design_entity_analysis: '_6059.BevelDifferentialPlanetGearLoadCase') -> '_6246.BevelDifferentialPlanetGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelDifferentialPlanetGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6246.BevelDifferentialPlanetGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_differential_sun_gear(self, design_entity: '_2056.BevelDifferentialSunGear') -> '_6247.BevelDifferentialSunGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelDifferentialSunGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6247.BevelDifferentialSunGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_differential_sun_gear_load_case(self, design_entity_analysis: '_6060.BevelDifferentialSunGearLoadCase') -> '_6247.BevelDifferentialSunGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelDifferentialSunGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelDifferentialSunGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6247.BevelDifferentialSunGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_gear(self, design_entity: '_2057.BevelGear') -> '_6248.BevelGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6248.BevelGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_gear_load_case(self, design_entity_analysis: '_6061.BevelGearLoadCase') -> '_6248.BevelGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6248.BevelGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_gear_set(self, design_entity: '_2058.BevelGearSet') -> '_6250.BevelGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6250.BevelGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_bevel_gear_set_load_case(self, design_entity_analysis: '_6063.BevelGearSetLoadCase') -> '_6250.BevelGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.BevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.BevelGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6250.BevelGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_conical_gear(self, design_entity: '_2061.ConicalGear') -> '_6264.ConicalGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConicalGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6264.ConicalGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_conical_gear_load_case(self, design_entity_analysis: '_6077.ConicalGearLoadCase') -> '_6264.ConicalGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConicalGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6264.ConicalGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_conical_gear_set(self, design_entity: '_2062.ConicalGearSet') -> '_6266.ConicalGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConicalGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6266.ConicalGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_conical_gear_set_load_case(self, design_entity_analysis: '_6081.ConicalGearSetLoadCase') -> '_6266.ConicalGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.ConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.ConicalGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6266.ConicalGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_cylindrical_gear(self, design_entity: '_2063.CylindricalGear') -> '_6275.CylindricalGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CylindricalGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6275.CylindricalGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_cylindrical_gear_load_case(self, design_entity_analysis: '_6090.CylindricalGearLoadCase') -> '_6275.CylindricalGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CylindricalGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6275.CylindricalGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_cylindrical_gear_set(self, design_entity: '_2064.CylindricalGearSet') -> '_6277.CylindricalGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CylindricalGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6277.CylindricalGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_cylindrical_gear_set_load_case(self, design_entity_analysis: '_6094.CylindricalGearSetLoadCase') -> '_6277.CylindricalGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CylindricalGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6277.CylindricalGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_cylindrical_planet_gear(self, design_entity: '_2065.CylindricalPlanetGear') -> '_6279.CylindricalPlanetGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CylindricalPlanetGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6279.CylindricalPlanetGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_cylindrical_planet_gear_load_case(self, design_entity_analysis: '_6095.CylindricalPlanetGearLoadCase') -> '_6279.CylindricalPlanetGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.CylindricalPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.CylindricalPlanetGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6279.CylindricalPlanetGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_gear(self, design_entity: '_2068.Gear') -> '_6286.GearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.GearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6286.GearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_gear_load_case(self, design_entity_analysis: '_6117.GearLoadCase') -> '_6286.GearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.GearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6286.GearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_gear_set(self, design_entity: '_2070.GearSet') -> '_6288.GearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.GearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6288.GearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_gear_set_load_case(self, design_entity_analysis: '_6122.GearSetLoadCase') -> '_6288.GearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.GearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.GearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6288.GearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_hypoid_gear(self, design_entity: '_2072.HypoidGear') -> '_6290.HypoidGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.HypoidGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6290.HypoidGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_hypoid_gear_load_case(self, design_entity_analysis: '_6132.HypoidGearLoadCase') -> '_6290.HypoidGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.HypoidGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6290.HypoidGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_hypoid_gear_set(self, design_entity: '_2073.HypoidGearSet') -> '_6292.HypoidGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.HypoidGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6292.HypoidGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_hypoid_gear_set_load_case(self, design_entity_analysis: '_6134.HypoidGearSetLoadCase') -> '_6292.HypoidGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.HypoidGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.HypoidGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6292.HypoidGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear(self, design_entity: '_2074.KlingelnbergCycloPalloidConicalGear') -> '_6295.KlingelnbergCycloPalloidConicalGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidConicalGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6295.KlingelnbergCycloPalloidConicalGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_load_case(self, design_entity_analysis: '_6138.KlingelnbergCycloPalloidConicalGearLoadCase') -> '_6295.KlingelnbergCycloPalloidConicalGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidConicalGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6295.KlingelnbergCycloPalloidConicalGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set(self, design_entity: '_2075.KlingelnbergCycloPalloidConicalGearSet') -> '_6297.KlingelnbergCycloPalloidConicalGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidConicalGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6297.KlingelnbergCycloPalloidConicalGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set_load_case(self, design_entity_analysis: '_6140.KlingelnbergCycloPalloidConicalGearSetLoadCase') -> '_6297.KlingelnbergCycloPalloidConicalGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidConicalGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidConicalGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6297.KlingelnbergCycloPalloidConicalGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear(self, design_entity: '_2076.KlingelnbergCycloPalloidHypoidGear') -> '_6298.KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6298.KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_load_case(self, design_entity_analysis: '_6141.KlingelnbergCycloPalloidHypoidGearLoadCase') -> '_6298.KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6298.KlingelnbergCycloPalloidHypoidGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set(self, design_entity: '_2077.KlingelnbergCycloPalloidHypoidGearSet') -> '_6300.KlingelnbergCycloPalloidHypoidGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidHypoidGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6300.KlingelnbergCycloPalloidHypoidGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set_load_case(self, design_entity_analysis: '_6143.KlingelnbergCycloPalloidHypoidGearSetLoadCase') -> '_6300.KlingelnbergCycloPalloidHypoidGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidHypoidGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidHypoidGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6300.KlingelnbergCycloPalloidHypoidGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, design_entity: '_2078.KlingelnbergCycloPalloidSpiralBevelGear') -> '_6301.KlingelnbergCycloPalloidSpiralBevelGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidSpiralBevelGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6301.KlingelnbergCycloPalloidSpiralBevelGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_load_case(self, design_entity_analysis: '_6144.KlingelnbergCycloPalloidSpiralBevelGearLoadCase') -> '_6301.KlingelnbergCycloPalloidSpiralBevelGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidSpiralBevelGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6301.KlingelnbergCycloPalloidSpiralBevelGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, design_entity: '_2079.KlingelnbergCycloPalloidSpiralBevelGearSet') -> '_6303.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6303.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_load_case(self, design_entity_analysis: '_6146.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase') -> '_6303.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.KlingelnbergCycloPalloidSpiralBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6303.KlingelnbergCycloPalloidSpiralBevelGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_planetary_gear_set(self, design_entity: '_2080.PlanetaryGearSet') -> '_6314.PlanetaryGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PlanetaryGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6314.PlanetaryGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_planetary_gear_set_load_case(self, design_entity_analysis: '_6159.PlanetaryGearSetLoadCase') -> '_6314.PlanetaryGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.PlanetaryGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.PlanetaryGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6314.PlanetaryGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_spiral_bevel_gear(self, design_entity: '_2081.SpiralBevelGear') -> '_6327.SpiralBevelGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpiralBevelGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6327.SpiralBevelGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_load_case(self, design_entity_analysis: '_6177.SpiralBevelGearLoadCase') -> '_6327.SpiralBevelGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpiralBevelGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6327.SpiralBevelGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_set(self, design_entity: '_2082.SpiralBevelGearSet') -> '_6329.SpiralBevelGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpiralBevelGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6329.SpiralBevelGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_spiral_bevel_gear_set_load_case(self, design_entity_analysis: '_6179.SpiralBevelGearSetLoadCase') -> '_6329.SpiralBevelGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.SpiralBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.SpiralBevelGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6329.SpiralBevelGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear(self, design_entity: '_2083.StraightBevelDiffGear') -> '_6333.StraightBevelDiffGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelDiffGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6333.StraightBevelDiffGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_load_case(self, design_entity_analysis: '_6184.StraightBevelDiffGearLoadCase') -> '_6333.StraightBevelDiffGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelDiffGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6333.StraightBevelDiffGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_set(self, design_entity: '_2084.StraightBevelDiffGearSet') -> '_6335.StraightBevelDiffGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelDiffGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6335.StraightBevelDiffGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_diff_gear_set_load_case(self, design_entity_analysis: '_6186.StraightBevelDiffGearSetLoadCase') -> '_6335.StraightBevelDiffGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelDiffGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelDiffGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6335.StraightBevelDiffGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_gear(self, design_entity: '_2085.StraightBevelGear') -> '_6336.StraightBevelGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6336.StraightBevelGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_gear_load_case(self, design_entity_analysis: '_6187.StraightBevelGearLoadCase') -> '_6336.StraightBevelGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6336.StraightBevelGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_gear_set(self, design_entity: '_2086.StraightBevelGearSet') -> '_6338.StraightBevelGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6338.StraightBevelGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_gear_set_load_case(self, design_entity_analysis: '_6189.StraightBevelGearSetLoadCase') -> '_6338.StraightBevelGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelGearSetLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6338.StraightBevelGearSetAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_planet_gear(self, design_entity: '_2087.StraightBevelPlanetGear') -> '_6339.StraightBevelPlanetGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelPlanetGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6339.StraightBevelPlanetGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_planet_gear_load_case(self, design_entity_analysis: '_6190.StraightBevelPlanetGearLoadCase') -> '_6339.StraightBevelPlanetGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelPlanetGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelPlanetGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6339.StraightBevelPlanetGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_sun_gear(self, design_entity: '_2088.StraightBevelSunGear') -> '_6340.StraightBevelSunGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelSunGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6340.StraightBevelSunGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_straight_bevel_sun_gear_load_case(self, design_entity_analysis: '_6191.StraightBevelSunGearLoadCase') -> '_6340.StraightBevelSunGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.StraightBevelSunGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.StraightBevelSunGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6340.StraightBevelSunGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_worm_gear(self, design_entity: '_2089.WormGear') -> '_6353.WormGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.WormGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6353.WormGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_worm_gear_load_case(self, design_entity_analysis: '_6208.WormGearLoadCase') -> '_6353.WormGearAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity_analysis (mastapy.system_model.analyses_and_results.static_loads.WormGearLoadCase)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.WormGearAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity_analysis.wrapped if design_entity_analysis else None)
        return constructor.new(_6353.WormGearAdvancedSystemDeflection)(method_result) if method_result else None

    def results_for_worm_gear_set(self, design_entity: '_2090.WormGearSet') -> '_6355.WormGearSetAdvancedSystemDeflection':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)

        Returns:
            mastapy.system_model.analyses_and_results.advanced_system_deflections.WormGearSetAdvancedSystemDeflection
        '''

        method_result = self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None)
        return constructor.new(_6355.WormGearSetAdvancedSystemDeflection)(method_result) if method_result else None
