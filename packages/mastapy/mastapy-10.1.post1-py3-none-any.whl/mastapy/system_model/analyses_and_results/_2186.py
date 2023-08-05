'''_2186.py

CompoundDynamicAnalysisAnalysis
'''


from typing import Iterable

from mastapy.system_model.part_model import (
    _1980, _1981, _1984, _1986,
    _1987, _1988, _1991, _1992,
    _1995, _1996, _1979, _1997,
    _2000, _2003, _2004, _2005,
    _2007, _2008, _2009, _2011,
    _2012, _2014, _2016, _2017,
    _2018
)
from mastapy.system_model.analyses_and_results.dynamic_analyses.compound import (
    _5917, _5918, _5923, _5934,
    _5935, _5940, _5951, _5962,
    _5963, _5967, _5922, _5971,
    _5975, _5986, _5987, _5988,
    _5989, _5990, _5996, _5997,
    _5998, _6003, _6007, _6030,
    _6031, _6004, _5944, _5946,
    _5964, _5966, _5919, _5921,
    _5926, _5928, _5929, _5930,
    _5931, _5933, _5947, _5949,
    _5958, _5960, _5961, _5968,
    _5970, _5972, _5974, _5977,
    _5979, _5980, _5982, _5983,
    _5985, _5995, _6008, _6010,
    _6014, _6016, _6017, _6019,
    _6020, _6021, _6032, _6034,
    _6035, _6037, _5991, _5993,
    _5925, _5936, _5938, _5941,
    _5943, _5952, _5954, _5956,
    _5957, _5999, _6005, _6001,
    _6000, _6011, _6013, _6022,
    _6023, _6024, _6025, _6026,
    _6028, _6029, _5955, _5924,
    _5939, _5950, _5976, _5994,
    _6002, _6006, _5927, _5945,
    _5965, _6015, _5932, _5948,
    _5920, _5959, _5973, _5978,
    _5981, _5984, _6009, _6018,
    _6033, _6036, _5969, _5992,
    _5937, _5942, _5953, _6012,
    _6027
)
from mastapy._internal import constructor, conversion
from mastapy.system_model.part_model.shaft_model import _2021
from mastapy.system_model.part_model.gears import (
    _2059, _2060, _2066, _2067,
    _2051, _2052, _2053, _2054,
    _2055, _2056, _2057, _2058,
    _2061, _2062, _2063, _2064,
    _2065, _2068, _2070, _2072,
    _2073, _2074, _2075, _2076,
    _2077, _2078, _2079, _2080,
    _2081, _2082, _2083, _2084,
    _2085, _2086, _2087, _2088,
    _2089, _2090, _2091, _2092
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
from mastapy.system_model.analyses_and_results import _2151
from mastapy._internal.python_net import python_net_import

_COMPOUND_DYNAMIC_ANALYSIS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults', 'CompoundDynamicAnalysisAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('CompoundDynamicAnalysisAnalysis',)


class CompoundDynamicAnalysisAnalysis(_2151.CompoundAnalysis):
    '''CompoundDynamicAnalysisAnalysis

    This is a mastapy class.
    '''

    TYPE = _COMPOUND_DYNAMIC_ANALYSIS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CompoundDynamicAnalysisAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    def results_for_abstract_assembly(self, design_entity: '_1980.AbstractAssembly') -> 'Iterable[_5917.AbstractAssemblyCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.AbstractAssemblyCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5917.AbstractAssemblyCompoundDynamicAnalysis))

    def results_for_abstract_shaft_or_housing(self, design_entity: '_1981.AbstractShaftOrHousing') -> 'Iterable[_5918.AbstractShaftOrHousingCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.AbstractShaftOrHousing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.AbstractShaftOrHousingCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5918.AbstractShaftOrHousingCompoundDynamicAnalysis))

    def results_for_bearing(self, design_entity: '_1984.Bearing') -> 'Iterable[_5923.BearingCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bearing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BearingCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5923.BearingCompoundDynamicAnalysis))

    def results_for_bolt(self, design_entity: '_1986.Bolt') -> 'Iterable[_5934.BoltCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Bolt)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BoltCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5934.BoltCompoundDynamicAnalysis))

    def results_for_bolted_joint(self, design_entity: '_1987.BoltedJoint') -> 'Iterable[_5935.BoltedJointCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.BoltedJoint)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BoltedJointCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5935.BoltedJointCompoundDynamicAnalysis))

    def results_for_component(self, design_entity: '_1988.Component') -> 'Iterable[_5940.ComponentCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Component)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ComponentCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5940.ComponentCompoundDynamicAnalysis))

    def results_for_connector(self, design_entity: '_1991.Connector') -> 'Iterable[_5951.ConnectorCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Connector)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConnectorCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5951.ConnectorCompoundDynamicAnalysis))

    def results_for_datum(self, design_entity: '_1992.Datum') -> 'Iterable[_5962.DatumCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Datum)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.DatumCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5962.DatumCompoundDynamicAnalysis))

    def results_for_external_cad_model(self, design_entity: '_1995.ExternalCADModel') -> 'Iterable[_5963.ExternalCADModelCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ExternalCADModel)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ExternalCADModelCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5963.ExternalCADModelCompoundDynamicAnalysis))

    def results_for_flexible_pin_assembly(self, design_entity: '_1996.FlexiblePinAssembly') -> 'Iterable[_5967.FlexiblePinAssemblyCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.FlexiblePinAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.FlexiblePinAssemblyCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5967.FlexiblePinAssemblyCompoundDynamicAnalysis))

    def results_for_assembly(self, design_entity: '_1979.Assembly') -> 'Iterable[_5922.AssemblyCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Assembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.AssemblyCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5922.AssemblyCompoundDynamicAnalysis))

    def results_for_guide_dxf_model(self, design_entity: '_1997.GuideDxfModel') -> 'Iterable[_5971.GuideDxfModelCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.GuideDxfModel)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.GuideDxfModelCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5971.GuideDxfModelCompoundDynamicAnalysis))

    def results_for_imported_fe_component(self, design_entity: '_2000.ImportedFEComponent') -> 'Iterable[_5975.ImportedFEComponentCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.ImportedFEComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ImportedFEComponentCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5975.ImportedFEComponentCompoundDynamicAnalysis))

    def results_for_mass_disc(self, design_entity: '_2003.MassDisc') -> 'Iterable[_5986.MassDiscCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MassDisc)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.MassDiscCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5986.MassDiscCompoundDynamicAnalysis))

    def results_for_measurement_component(self, design_entity: '_2004.MeasurementComponent') -> 'Iterable[_5987.MeasurementComponentCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MeasurementComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.MeasurementComponentCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5987.MeasurementComponentCompoundDynamicAnalysis))

    def results_for_mountable_component(self, design_entity: '_2005.MountableComponent') -> 'Iterable[_5988.MountableComponentCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.MountableComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.MountableComponentCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5988.MountableComponentCompoundDynamicAnalysis))

    def results_for_oil_seal(self, design_entity: '_2007.OilSeal') -> 'Iterable[_5989.OilSealCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.OilSeal)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.OilSealCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5989.OilSealCompoundDynamicAnalysis))

    def results_for_part(self, design_entity: '_2008.Part') -> 'Iterable[_5990.PartCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.Part)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.PartCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5990.PartCompoundDynamicAnalysis))

    def results_for_planet_carrier(self, design_entity: '_2009.PlanetCarrier') -> 'Iterable[_5996.PlanetCarrierCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PlanetCarrier)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.PlanetCarrierCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5996.PlanetCarrierCompoundDynamicAnalysis))

    def results_for_point_load(self, design_entity: '_2011.PointLoad') -> 'Iterable[_5997.PointLoadCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PointLoad)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.PointLoadCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5997.PointLoadCompoundDynamicAnalysis))

    def results_for_power_load(self, design_entity: '_2012.PowerLoad') -> 'Iterable[_5998.PowerLoadCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.PowerLoad)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.PowerLoadCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5998.PowerLoadCompoundDynamicAnalysis))

    def results_for_root_assembly(self, design_entity: '_2014.RootAssembly') -> 'Iterable[_6003.RootAssemblyCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.RootAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.RootAssemblyCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6003.RootAssemblyCompoundDynamicAnalysis))

    def results_for_specialised_assembly(self, design_entity: '_2016.SpecialisedAssembly') -> 'Iterable[_6007.SpecialisedAssemblyCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.SpecialisedAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SpecialisedAssemblyCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6007.SpecialisedAssemblyCompoundDynamicAnalysis))

    def results_for_unbalanced_mass(self, design_entity: '_2017.UnbalancedMass') -> 'Iterable[_6030.UnbalancedMassCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.UnbalancedMass)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.UnbalancedMassCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6030.UnbalancedMassCompoundDynamicAnalysis))

    def results_for_virtual_component(self, design_entity: '_2018.VirtualComponent') -> 'Iterable[_6031.VirtualComponentCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.VirtualComponent)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.VirtualComponentCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6031.VirtualComponentCompoundDynamicAnalysis))

    def results_for_shaft(self, design_entity: '_2021.Shaft') -> 'Iterable[_6004.ShaftCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.shaft_model.Shaft)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ShaftCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6004.ShaftCompoundDynamicAnalysis))

    def results_for_concept_gear(self, design_entity: '_2059.ConceptGear') -> 'Iterable[_5944.ConceptGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConceptGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5944.ConceptGearCompoundDynamicAnalysis))

    def results_for_concept_gear_set(self, design_entity: '_2060.ConceptGearSet') -> 'Iterable[_5946.ConceptGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConceptGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConceptGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5946.ConceptGearSetCompoundDynamicAnalysis))

    def results_for_face_gear(self, design_entity: '_2066.FaceGear') -> 'Iterable[_5964.FaceGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.FaceGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5964.FaceGearCompoundDynamicAnalysis))

    def results_for_face_gear_set(self, design_entity: '_2067.FaceGearSet') -> 'Iterable[_5966.FaceGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.FaceGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.FaceGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5966.FaceGearSetCompoundDynamicAnalysis))

    def results_for_agma_gleason_conical_gear(self, design_entity: '_2051.AGMAGleasonConicalGear') -> 'Iterable[_5919.AGMAGleasonConicalGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.AGMAGleasonConicalGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5919.AGMAGleasonConicalGearCompoundDynamicAnalysis))

    def results_for_agma_gleason_conical_gear_set(self, design_entity: '_2052.AGMAGleasonConicalGearSet') -> 'Iterable[_5921.AGMAGleasonConicalGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.AGMAGleasonConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.AGMAGleasonConicalGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5921.AGMAGleasonConicalGearSetCompoundDynamicAnalysis))

    def results_for_bevel_differential_gear(self, design_entity: '_2053.BevelDifferentialGear') -> 'Iterable[_5926.BevelDifferentialGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BevelDifferentialGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5926.BevelDifferentialGearCompoundDynamicAnalysis))

    def results_for_bevel_differential_gear_set(self, design_entity: '_2054.BevelDifferentialGearSet') -> 'Iterable[_5928.BevelDifferentialGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BevelDifferentialGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5928.BevelDifferentialGearSetCompoundDynamicAnalysis))

    def results_for_bevel_differential_planet_gear(self, design_entity: '_2055.BevelDifferentialPlanetGear') -> 'Iterable[_5929.BevelDifferentialPlanetGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BevelDifferentialPlanetGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5929.BevelDifferentialPlanetGearCompoundDynamicAnalysis))

    def results_for_bevel_differential_sun_gear(self, design_entity: '_2056.BevelDifferentialSunGear') -> 'Iterable[_5930.BevelDifferentialSunGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelDifferentialSunGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BevelDifferentialSunGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5930.BevelDifferentialSunGearCompoundDynamicAnalysis))

    def results_for_bevel_gear(self, design_entity: '_2057.BevelGear') -> 'Iterable[_5931.BevelGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BevelGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5931.BevelGearCompoundDynamicAnalysis))

    def results_for_bevel_gear_set(self, design_entity: '_2058.BevelGearSet') -> 'Iterable[_5933.BevelGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.BevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BevelGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5933.BevelGearSetCompoundDynamicAnalysis))

    def results_for_conical_gear(self, design_entity: '_2061.ConicalGear') -> 'Iterable[_5947.ConicalGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConicalGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5947.ConicalGearCompoundDynamicAnalysis))

    def results_for_conical_gear_set(self, design_entity: '_2062.ConicalGearSet') -> 'Iterable[_5949.ConicalGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConicalGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5949.ConicalGearSetCompoundDynamicAnalysis))

    def results_for_cylindrical_gear(self, design_entity: '_2063.CylindricalGear') -> 'Iterable[_5958.CylindricalGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CylindricalGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5958.CylindricalGearCompoundDynamicAnalysis))

    def results_for_cylindrical_gear_set(self, design_entity: '_2064.CylindricalGearSet') -> 'Iterable[_5960.CylindricalGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CylindricalGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5960.CylindricalGearSetCompoundDynamicAnalysis))

    def results_for_cylindrical_planet_gear(self, design_entity: '_2065.CylindricalPlanetGear') -> 'Iterable[_5961.CylindricalPlanetGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.CylindricalPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CylindricalPlanetGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5961.CylindricalPlanetGearCompoundDynamicAnalysis))

    def results_for_gear(self, design_entity: '_2068.Gear') -> 'Iterable[_5968.GearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.Gear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.GearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5968.GearCompoundDynamicAnalysis))

    def results_for_gear_set(self, design_entity: '_2070.GearSet') -> 'Iterable[_5970.GearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.GearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.GearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5970.GearSetCompoundDynamicAnalysis))

    def results_for_hypoid_gear(self, design_entity: '_2072.HypoidGear') -> 'Iterable[_5972.HypoidGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.HypoidGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5972.HypoidGearCompoundDynamicAnalysis))

    def results_for_hypoid_gear_set(self, design_entity: '_2073.HypoidGearSet') -> 'Iterable[_5974.HypoidGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.HypoidGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.HypoidGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5974.HypoidGearSetCompoundDynamicAnalysis))

    def results_for_klingelnberg_cyclo_palloid_conical_gear(self, design_entity: '_2074.KlingelnbergCycloPalloidConicalGear') -> 'Iterable[_5977.KlingelnbergCycloPalloidConicalGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.KlingelnbergCycloPalloidConicalGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5977.KlingelnbergCycloPalloidConicalGearCompoundDynamicAnalysis))

    def results_for_klingelnberg_cyclo_palloid_conical_gear_set(self, design_entity: '_2075.KlingelnbergCycloPalloidConicalGearSet') -> 'Iterable[_5979.KlingelnbergCycloPalloidConicalGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidConicalGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.KlingelnbergCycloPalloidConicalGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5979.KlingelnbergCycloPalloidConicalGearSetCompoundDynamicAnalysis))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear(self, design_entity: '_2076.KlingelnbergCycloPalloidHypoidGear') -> 'Iterable[_5980.KlingelnbergCycloPalloidHypoidGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.KlingelnbergCycloPalloidHypoidGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5980.KlingelnbergCycloPalloidHypoidGearCompoundDynamicAnalysis))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_set(self, design_entity: '_2077.KlingelnbergCycloPalloidHypoidGearSet') -> 'Iterable[_5982.KlingelnbergCycloPalloidHypoidGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidHypoidGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.KlingelnbergCycloPalloidHypoidGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5982.KlingelnbergCycloPalloidHypoidGearSetCompoundDynamicAnalysis))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear(self, design_entity: '_2078.KlingelnbergCycloPalloidSpiralBevelGear') -> 'Iterable[_5983.KlingelnbergCycloPalloidSpiralBevelGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.KlingelnbergCycloPalloidSpiralBevelGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5983.KlingelnbergCycloPalloidSpiralBevelGearCompoundDynamicAnalysis))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_set(self, design_entity: '_2079.KlingelnbergCycloPalloidSpiralBevelGearSet') -> 'Iterable[_5985.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.KlingelnbergCycloPalloidSpiralBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5985.KlingelnbergCycloPalloidSpiralBevelGearSetCompoundDynamicAnalysis))

    def results_for_planetary_gear_set(self, design_entity: '_2080.PlanetaryGearSet') -> 'Iterable[_5995.PlanetaryGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.PlanetaryGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.PlanetaryGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5995.PlanetaryGearSetCompoundDynamicAnalysis))

    def results_for_spiral_bevel_gear(self, design_entity: '_2081.SpiralBevelGear') -> 'Iterable[_6008.SpiralBevelGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SpiralBevelGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6008.SpiralBevelGearCompoundDynamicAnalysis))

    def results_for_spiral_bevel_gear_set(self, design_entity: '_2082.SpiralBevelGearSet') -> 'Iterable[_6010.SpiralBevelGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.SpiralBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SpiralBevelGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6010.SpiralBevelGearSetCompoundDynamicAnalysis))

    def results_for_straight_bevel_diff_gear(self, design_entity: '_2083.StraightBevelDiffGear') -> 'Iterable[_6014.StraightBevelDiffGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.StraightBevelDiffGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6014.StraightBevelDiffGearCompoundDynamicAnalysis))

    def results_for_straight_bevel_diff_gear_set(self, design_entity: '_2084.StraightBevelDiffGearSet') -> 'Iterable[_6016.StraightBevelDiffGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelDiffGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.StraightBevelDiffGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6016.StraightBevelDiffGearSetCompoundDynamicAnalysis))

    def results_for_straight_bevel_gear(self, design_entity: '_2085.StraightBevelGear') -> 'Iterable[_6017.StraightBevelGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.StraightBevelGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6017.StraightBevelGearCompoundDynamicAnalysis))

    def results_for_straight_bevel_gear_set(self, design_entity: '_2086.StraightBevelGearSet') -> 'Iterable[_6019.StraightBevelGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.StraightBevelGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6019.StraightBevelGearSetCompoundDynamicAnalysis))

    def results_for_straight_bevel_planet_gear(self, design_entity: '_2087.StraightBevelPlanetGear') -> 'Iterable[_6020.StraightBevelPlanetGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelPlanetGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.StraightBevelPlanetGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6020.StraightBevelPlanetGearCompoundDynamicAnalysis))

    def results_for_straight_bevel_sun_gear(self, design_entity: '_2088.StraightBevelSunGear') -> 'Iterable[_6021.StraightBevelSunGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.StraightBevelSunGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.StraightBevelSunGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6021.StraightBevelSunGearCompoundDynamicAnalysis))

    def results_for_worm_gear(self, design_entity: '_2089.WormGear') -> 'Iterable[_6032.WormGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.WormGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6032.WormGearCompoundDynamicAnalysis))

    def results_for_worm_gear_set(self, design_entity: '_2090.WormGearSet') -> 'Iterable[_6034.WormGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.WormGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.WormGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6034.WormGearSetCompoundDynamicAnalysis))

    def results_for_zerol_bevel_gear(self, design_entity: '_2091.ZerolBevelGear') -> 'Iterable[_6035.ZerolBevelGearCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGear)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ZerolBevelGearCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6035.ZerolBevelGearCompoundDynamicAnalysis))

    def results_for_zerol_bevel_gear_set(self, design_entity: '_2092.ZerolBevelGearSet') -> 'Iterable[_6037.ZerolBevelGearSetCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.gears.ZerolBevelGearSet)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ZerolBevelGearSetCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6037.ZerolBevelGearSetCompoundDynamicAnalysis))

    def results_for_part_to_part_shear_coupling(self, design_entity: '_2121.PartToPartShearCoupling') -> 'Iterable[_5991.PartToPartShearCouplingCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCoupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.PartToPartShearCouplingCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5991.PartToPartShearCouplingCompoundDynamicAnalysis))

    def results_for_part_to_part_shear_coupling_half(self, design_entity: '_2122.PartToPartShearCouplingHalf') -> 'Iterable[_5993.PartToPartShearCouplingHalfCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.PartToPartShearCouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.PartToPartShearCouplingHalfCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5993.PartToPartShearCouplingHalfCompoundDynamicAnalysis))

    def results_for_belt_drive(self, design_entity: '_2110.BeltDrive') -> 'Iterable[_5925.BeltDriveCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.BeltDrive)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BeltDriveCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5925.BeltDriveCompoundDynamicAnalysis))

    def results_for_clutch(self, design_entity: '_2112.Clutch') -> 'Iterable[_5936.ClutchCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Clutch)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ClutchCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5936.ClutchCompoundDynamicAnalysis))

    def results_for_clutch_half(self, design_entity: '_2113.ClutchHalf') -> 'Iterable[_5938.ClutchHalfCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ClutchHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ClutchHalfCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5938.ClutchHalfCompoundDynamicAnalysis))

    def results_for_concept_coupling(self, design_entity: '_2115.ConceptCoupling') -> 'Iterable[_5941.ConceptCouplingCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCoupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConceptCouplingCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5941.ConceptCouplingCompoundDynamicAnalysis))

    def results_for_concept_coupling_half(self, design_entity: '_2116.ConceptCouplingHalf') -> 'Iterable[_5943.ConceptCouplingHalfCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ConceptCouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConceptCouplingHalfCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5943.ConceptCouplingHalfCompoundDynamicAnalysis))

    def results_for_coupling(self, design_entity: '_2117.Coupling') -> 'Iterable[_5952.CouplingCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Coupling)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CouplingCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5952.CouplingCompoundDynamicAnalysis))

    def results_for_coupling_half(self, design_entity: '_2118.CouplingHalf') -> 'Iterable[_5954.CouplingHalfCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CouplingHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CouplingHalfCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5954.CouplingHalfCompoundDynamicAnalysis))

    def results_for_cvt(self, design_entity: '_2119.CVT') -> 'Iterable[_5956.CVTCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVT)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CVTCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5956.CVTCompoundDynamicAnalysis))

    def results_for_cvt_pulley(self, design_entity: '_2120.CVTPulley') -> 'Iterable[_5957.CVTPulleyCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.CVTPulley)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CVTPulleyCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5957.CVTPulleyCompoundDynamicAnalysis))

    def results_for_pulley(self, design_entity: '_2123.Pulley') -> 'Iterable[_5999.PulleyCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Pulley)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.PulleyCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5999.PulleyCompoundDynamicAnalysis))

    def results_for_shaft_hub_connection(self, design_entity: '_2131.ShaftHubConnection') -> 'Iterable[_6005.ShaftHubConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.ShaftHubConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ShaftHubConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6005.ShaftHubConnectionCompoundDynamicAnalysis))

    def results_for_rolling_ring(self, design_entity: '_2129.RollingRing') -> 'Iterable[_6001.RollingRingCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRing)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.RollingRingCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6001.RollingRingCompoundDynamicAnalysis))

    def results_for_rolling_ring_assembly(self, design_entity: '_2130.RollingRingAssembly') -> 'Iterable[_6000.RollingRingAssemblyCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.RollingRingAssembly)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.RollingRingAssemblyCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6000.RollingRingAssemblyCompoundDynamicAnalysis))

    def results_for_spring_damper(self, design_entity: '_2132.SpringDamper') -> 'Iterable[_6011.SpringDamperCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamper)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SpringDamperCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6011.SpringDamperCompoundDynamicAnalysis))

    def results_for_spring_damper_half(self, design_entity: '_2133.SpringDamperHalf') -> 'Iterable[_6013.SpringDamperHalfCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SpringDamperHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SpringDamperHalfCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6013.SpringDamperHalfCompoundDynamicAnalysis))

    def results_for_synchroniser(self, design_entity: '_2134.Synchroniser') -> 'Iterable[_6022.SynchroniserCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.Synchroniser)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SynchroniserCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6022.SynchroniserCompoundDynamicAnalysis))

    def results_for_synchroniser_half(self, design_entity: '_2136.SynchroniserHalf') -> 'Iterable[_6023.SynchroniserHalfCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserHalf)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SynchroniserHalfCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6023.SynchroniserHalfCompoundDynamicAnalysis))

    def results_for_synchroniser_part(self, design_entity: '_2137.SynchroniserPart') -> 'Iterable[_6024.SynchroniserPartCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserPart)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SynchroniserPartCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6024.SynchroniserPartCompoundDynamicAnalysis))

    def results_for_synchroniser_sleeve(self, design_entity: '_2138.SynchroniserSleeve') -> 'Iterable[_6025.SynchroniserSleeveCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.SynchroniserSleeve)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SynchroniserSleeveCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6025.SynchroniserSleeveCompoundDynamicAnalysis))

    def results_for_torque_converter(self, design_entity: '_2139.TorqueConverter') -> 'Iterable[_6026.TorqueConverterCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverter)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.TorqueConverterCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6026.TorqueConverterCompoundDynamicAnalysis))

    def results_for_torque_converter_pump(self, design_entity: '_2140.TorqueConverterPump') -> 'Iterable[_6028.TorqueConverterPumpCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterPump)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.TorqueConverterPumpCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6028.TorqueConverterPumpCompoundDynamicAnalysis))

    def results_for_torque_converter_turbine(self, design_entity: '_2142.TorqueConverterTurbine') -> 'Iterable[_6029.TorqueConverterTurbineCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.part_model.couplings.TorqueConverterTurbine)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.TorqueConverterTurbineCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6029.TorqueConverterTurbineCompoundDynamicAnalysis))

    def results_for_cvt_belt_connection(self, design_entity: '_1836.CVTBeltConnection') -> 'Iterable[_5955.CVTBeltConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CVTBeltConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CVTBeltConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5955.CVTBeltConnectionCompoundDynamicAnalysis))

    def results_for_belt_connection(self, design_entity: '_1831.BeltConnection') -> 'Iterable[_5924.BeltConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.BeltConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BeltConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5924.BeltConnectionCompoundDynamicAnalysis))

    def results_for_coaxial_connection(self, design_entity: '_1832.CoaxialConnection') -> 'Iterable[_5939.CoaxialConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.CoaxialConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CoaxialConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5939.CoaxialConnectionCompoundDynamicAnalysis))

    def results_for_connection(self, design_entity: '_1835.Connection') -> 'Iterable[_5950.ConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.Connection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5950.ConnectionCompoundDynamicAnalysis))

    def results_for_inter_mountable_component_connection(self, design_entity: '_1844.InterMountableComponentConnection') -> 'Iterable[_5976.InterMountableComponentConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.InterMountableComponentConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.InterMountableComponentConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5976.InterMountableComponentConnectionCompoundDynamicAnalysis))

    def results_for_planetary_connection(self, design_entity: '_1847.PlanetaryConnection') -> 'Iterable[_5994.PlanetaryConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.PlanetaryConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.PlanetaryConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5994.PlanetaryConnectionCompoundDynamicAnalysis))

    def results_for_rolling_ring_connection(self, design_entity: '_1851.RollingRingConnection') -> 'Iterable[_6002.RollingRingConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.RollingRingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.RollingRingConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6002.RollingRingConnectionCompoundDynamicAnalysis))

    def results_for_shaft_to_mountable_component_connection(self, design_entity: '_1855.ShaftToMountableComponentConnection') -> 'Iterable[_6006.ShaftToMountableComponentConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.ShaftToMountableComponentConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ShaftToMountableComponentConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6006.ShaftToMountableComponentConnectionCompoundDynamicAnalysis))

    def results_for_bevel_differential_gear_mesh(self, design_entity: '_1861.BevelDifferentialGearMesh') -> 'Iterable[_5927.BevelDifferentialGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelDifferentialGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BevelDifferentialGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5927.BevelDifferentialGearMeshCompoundDynamicAnalysis))

    def results_for_concept_gear_mesh(self, design_entity: '_1865.ConceptGearMesh') -> 'Iterable[_5945.ConceptGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConceptGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConceptGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5945.ConceptGearMeshCompoundDynamicAnalysis))

    def results_for_face_gear_mesh(self, design_entity: '_1871.FaceGearMesh') -> 'Iterable[_5965.FaceGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.FaceGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.FaceGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5965.FaceGearMeshCompoundDynamicAnalysis))

    def results_for_straight_bevel_diff_gear_mesh(self, design_entity: '_1885.StraightBevelDiffGearMesh') -> 'Iterable[_6015.StraightBevelDiffGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelDiffGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.StraightBevelDiffGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6015.StraightBevelDiffGearMeshCompoundDynamicAnalysis))

    def results_for_bevel_gear_mesh(self, design_entity: '_1863.BevelGearMesh') -> 'Iterable[_5932.BevelGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.BevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.BevelGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5932.BevelGearMeshCompoundDynamicAnalysis))

    def results_for_conical_gear_mesh(self, design_entity: '_1867.ConicalGearMesh') -> 'Iterable[_5948.ConicalGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConicalGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5948.ConicalGearMeshCompoundDynamicAnalysis))

    def results_for_agma_gleason_conical_gear_mesh(self, design_entity: '_1859.AGMAGleasonConicalGearMesh') -> 'Iterable[_5920.AGMAGleasonConicalGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.AGMAGleasonConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.AGMAGleasonConicalGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5920.AGMAGleasonConicalGearMeshCompoundDynamicAnalysis))

    def results_for_cylindrical_gear_mesh(self, design_entity: '_1869.CylindricalGearMesh') -> 'Iterable[_5959.CylindricalGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.CylindricalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CylindricalGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5959.CylindricalGearMeshCompoundDynamicAnalysis))

    def results_for_hypoid_gear_mesh(self, design_entity: '_1875.HypoidGearMesh') -> 'Iterable[_5973.HypoidGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.HypoidGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.HypoidGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5973.HypoidGearMeshCompoundDynamicAnalysis))

    def results_for_klingelnberg_cyclo_palloid_conical_gear_mesh(self, design_entity: '_1878.KlingelnbergCycloPalloidConicalGearMesh') -> 'Iterable[_5978.KlingelnbergCycloPalloidConicalGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidConicalGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.KlingelnbergCycloPalloidConicalGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5978.KlingelnbergCycloPalloidConicalGearMeshCompoundDynamicAnalysis))

    def results_for_klingelnberg_cyclo_palloid_hypoid_gear_mesh(self, design_entity: '_1879.KlingelnbergCycloPalloidHypoidGearMesh') -> 'Iterable[_5981.KlingelnbergCycloPalloidHypoidGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidHypoidGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.KlingelnbergCycloPalloidHypoidGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5981.KlingelnbergCycloPalloidHypoidGearMeshCompoundDynamicAnalysis))

    def results_for_klingelnberg_cyclo_palloid_spiral_bevel_gear_mesh(self, design_entity: '_1880.KlingelnbergCycloPalloidSpiralBevelGearMesh') -> 'Iterable[_5984.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.KlingelnbergCycloPalloidSpiralBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5984.KlingelnbergCycloPalloidSpiralBevelGearMeshCompoundDynamicAnalysis))

    def results_for_spiral_bevel_gear_mesh(self, design_entity: '_1883.SpiralBevelGearMesh') -> 'Iterable[_6009.SpiralBevelGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.SpiralBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SpiralBevelGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6009.SpiralBevelGearMeshCompoundDynamicAnalysis))

    def results_for_straight_bevel_gear_mesh(self, design_entity: '_1887.StraightBevelGearMesh') -> 'Iterable[_6018.StraightBevelGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.StraightBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.StraightBevelGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6018.StraightBevelGearMeshCompoundDynamicAnalysis))

    def results_for_worm_gear_mesh(self, design_entity: '_1889.WormGearMesh') -> 'Iterable[_6033.WormGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.WormGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.WormGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6033.WormGearMeshCompoundDynamicAnalysis))

    def results_for_zerol_bevel_gear_mesh(self, design_entity: '_1891.ZerolBevelGearMesh') -> 'Iterable[_6036.ZerolBevelGearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.ZerolBevelGearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ZerolBevelGearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6036.ZerolBevelGearMeshCompoundDynamicAnalysis))

    def results_for_gear_mesh(self, design_entity: '_1873.GearMesh') -> 'Iterable[_5969.GearMeshCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.gears.GearMesh)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.GearMeshCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5969.GearMeshCompoundDynamicAnalysis))

    def results_for_part_to_part_shear_coupling_connection(self, design_entity: '_1899.PartToPartShearCouplingConnection') -> 'Iterable[_5992.PartToPartShearCouplingConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.PartToPartShearCouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.PartToPartShearCouplingConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5992.PartToPartShearCouplingConnectionCompoundDynamicAnalysis))

    def results_for_clutch_connection(self, design_entity: '_1893.ClutchConnection') -> 'Iterable[_5937.ClutchConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ClutchConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ClutchConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5937.ClutchConnectionCompoundDynamicAnalysis))

    def results_for_concept_coupling_connection(self, design_entity: '_1895.ConceptCouplingConnection') -> 'Iterable[_5942.ConceptCouplingConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.ConceptCouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.ConceptCouplingConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5942.ConceptCouplingConnectionCompoundDynamicAnalysis))

    def results_for_coupling_connection(self, design_entity: '_1897.CouplingConnection') -> 'Iterable[_5953.CouplingConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.CouplingConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.CouplingConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_5953.CouplingConnectionCompoundDynamicAnalysis))

    def results_for_spring_damper_connection(self, design_entity: '_1901.SpringDamperConnection') -> 'Iterable[_6012.SpringDamperConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.SpringDamperConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.SpringDamperConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6012.SpringDamperConnectionCompoundDynamicAnalysis))

    def results_for_torque_converter_connection(self, design_entity: '_1903.TorqueConverterConnection') -> 'Iterable[_6027.TorqueConverterConnectionCompoundDynamicAnalysis]':
        ''' 'ResultsFor' is the original name of this method.

        Args:
            design_entity (mastapy.system_model.connections_and_sockets.couplings.TorqueConverterConnection)

        Returns:
            Iterable[mastapy.system_model.analyses_and_results.dynamic_analyses.compound.TorqueConverterConnectionCompoundDynamicAnalysis]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.ResultsFor(design_entity.wrapped if design_entity else None), constructor.new(_6027.TorqueConverterConnectionCompoundDynamicAnalysis))
