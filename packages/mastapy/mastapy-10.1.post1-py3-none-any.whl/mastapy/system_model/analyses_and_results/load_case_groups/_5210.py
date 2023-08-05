'''_5210.py

AbstractLoadCaseGroup
'''


from typing import List

from mastapy._internal import constructor, conversion
from mastapy.system_model import _1770
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3526
from mastapy.system_model.analyses_and_results.static_loads import _6149, _6022, _6029
from mastapy.system_model.analyses_and_results import (
    _2182, _2177, _2162, _2169,
    _2176, _2179, _2180, _2181,
    _2174, _2164, _2173, _2172,
    _2170, _2171, _2183, _2178,
    _2163, _2167, _2166, _2165,
    _2168, _2175, _2129
)
from mastapy import _6478, _0
from mastapy._internal.python_net import python_net_import

_ABSTRACT_LOAD_CASE_GROUP = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.LoadCaseGroups', 'AbstractLoadCaseGroup')


__docformat__ = 'restructuredtext en'
__all__ = ('AbstractLoadCaseGroup',)


class AbstractLoadCaseGroup(_0.APIBase):
    '''AbstractLoadCaseGroup

    This is a mastapy class.
    '''

    TYPE = _ABSTRACT_LOAD_CASE_GROUP

    __hash__ = None

    def __init__(self, instance_to_wrap: 'AbstractLoadCaseGroup.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.'''

        return self.wrapped.Name

    @name.setter
    def name(self, value: 'str'):
        self.wrapped.Name = str(value) if value else None

    @property
    def total_duration(self) -> 'float':
        '''float: 'TotalDuration' is the original name of this property.'''

        return self.wrapped.TotalDuration

    @total_duration.setter
    def total_duration(self, value: 'float'):
        self.wrapped.TotalDuration = float(value) if value else 0.0

    @property
    def model(self) -> '_1770.Design':
        '''Design: 'Model' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1770.Design)(self.wrapped.Model) if self.wrapped.Model else None

    @property
    def parametric_analysis_options(self) -> '_3526.ParametricStudyToolOptions':
        '''ParametricStudyToolOptions: 'ParametricAnalysisOptions' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_3526.ParametricStudyToolOptions)(self.wrapped.ParametricAnalysisOptions) if self.wrapped.ParametricAnalysisOptions else None

    @property
    def load_case_root_assemblies(self) -> 'List[_6149.RootAssemblyLoadCase]':
        '''List[RootAssemblyLoadCase]: 'LoadCaseRootAssemblies' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.LoadCaseRootAssemblies, constructor.new(_6149.RootAssemblyLoadCase))
        return value

    @property
    def report_names(self) -> 'List[str]':
        '''List[str]: 'ReportNames' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ReportNames

    @property
    def compound_system_deflection(self) -> '_2182.CompoundSystemDeflectionAnalysis':
        '''CompoundSystemDeflectionAnalysis: 'CompoundSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2182.CompoundSystemDeflectionAnalysis)(self.wrapped.CompoundSystemDeflection) if self.wrapped.CompoundSystemDeflection else None

    @property
    def compound_power_flow(self) -> '_2177.CompoundPowerFlowAnalysis':
        '''CompoundPowerFlowAnalysis: 'CompoundPowerFlow' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2177.CompoundPowerFlowAnalysis)(self.wrapped.CompoundPowerFlow) if self.wrapped.CompoundPowerFlow else None

    @property
    def compound_advanced_system_deflection(self) -> '_2162.CompoundAdvancedSystemDeflectionAnalysis':
        '''CompoundAdvancedSystemDeflectionAnalysis: 'CompoundAdvancedSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2162.CompoundAdvancedSystemDeflectionAnalysis)(self.wrapped.CompoundAdvancedSystemDeflection) if self.wrapped.CompoundAdvancedSystemDeflection else None

    @property
    def compound_gear_whine_analysis(self) -> '_2169.CompoundGearWhineAnalysisAnalysis':
        '''CompoundGearWhineAnalysisAnalysis: 'CompoundGearWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2169.CompoundGearWhineAnalysisAnalysis)(self.wrapped.CompoundGearWhineAnalysis) if self.wrapped.CompoundGearWhineAnalysis else None

    @property
    def compound_multibody_dynamics(self) -> '_2176.CompoundMultibodyDynamicsAnalysis':
        '''CompoundMultibodyDynamicsAnalysis: 'CompoundMultibodyDynamics' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2176.CompoundMultibodyDynamicsAnalysis)(self.wrapped.CompoundMultibodyDynamics) if self.wrapped.CompoundMultibodyDynamics else None

    @property
    def compound_steady_state_synchronous_response(self) -> '_2179.CompoundSteadyStateSynchronousResponseAnalysis':
        '''CompoundSteadyStateSynchronousResponseAnalysis: 'CompoundSteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2179.CompoundSteadyStateSynchronousResponseAnalysis)(self.wrapped.CompoundSteadyStateSynchronousResponse) if self.wrapped.CompoundSteadyStateSynchronousResponse else None

    @property
    def compound_steady_state_synchronous_responseata_speed(self) -> '_2180.CompoundSteadyStateSynchronousResponseataSpeedAnalysis':
        '''CompoundSteadyStateSynchronousResponseataSpeedAnalysis: 'CompoundSteadyStateSynchronousResponseataSpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2180.CompoundSteadyStateSynchronousResponseataSpeedAnalysis)(self.wrapped.CompoundSteadyStateSynchronousResponseataSpeed) if self.wrapped.CompoundSteadyStateSynchronousResponseataSpeed else None

    @property
    def compound_steady_state_synchronous_responseona_shaft(self) -> '_2181.CompoundSteadyStateSynchronousResponseonaShaftAnalysis':
        '''CompoundSteadyStateSynchronousResponseonaShaftAnalysis: 'CompoundSteadyStateSynchronousResponseonaShaft' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2181.CompoundSteadyStateSynchronousResponseonaShaftAnalysis)(self.wrapped.CompoundSteadyStateSynchronousResponseonaShaft) if self.wrapped.CompoundSteadyStateSynchronousResponseonaShaft else None

    @property
    def compound_modal_analysis(self) -> '_2174.CompoundModalAnalysisAnalysis':
        '''CompoundModalAnalysisAnalysis: 'CompoundModalAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2174.CompoundModalAnalysisAnalysis)(self.wrapped.CompoundModalAnalysis) if self.wrapped.CompoundModalAnalysis else None

    @property
    def compound_dynamic_analysis(self) -> '_2164.CompoundDynamicAnalysisAnalysis':
        '''CompoundDynamicAnalysisAnalysis: 'CompoundDynamicAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2164.CompoundDynamicAnalysisAnalysis)(self.wrapped.CompoundDynamicAnalysis) if self.wrapped.CompoundDynamicAnalysis else None

    @property
    def compound_modal_analysesat_stiffnesses(self) -> '_2173.CompoundModalAnalysesatStiffnessesAnalysis':
        '''CompoundModalAnalysesatStiffnessesAnalysis: 'CompoundModalAnalysesatStiffnesses' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2173.CompoundModalAnalysesatStiffnessesAnalysis)(self.wrapped.CompoundModalAnalysesatStiffnesses) if self.wrapped.CompoundModalAnalysesatStiffnesses else None

    @property
    def compound_modal_analysesat_speeds(self) -> '_2172.CompoundModalAnalysesatSpeedsAnalysis':
        '''CompoundModalAnalysesatSpeedsAnalysis: 'CompoundModalAnalysesatSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2172.CompoundModalAnalysesatSpeedsAnalysis)(self.wrapped.CompoundModalAnalysesatSpeeds) if self.wrapped.CompoundModalAnalysesatSpeeds else None

    @property
    def compound_modal_analysesata_speed(self) -> '_2170.CompoundModalAnalysesataSpeedAnalysis':
        '''CompoundModalAnalysesataSpeedAnalysis: 'CompoundModalAnalysesataSpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2170.CompoundModalAnalysesataSpeedAnalysis)(self.wrapped.CompoundModalAnalysesataSpeed) if self.wrapped.CompoundModalAnalysesataSpeed else None

    @property
    def compound_modal_analysesata_stiffness(self) -> '_2171.CompoundModalAnalysesataStiffnessAnalysis':
        '''CompoundModalAnalysesataStiffnessAnalysis: 'CompoundModalAnalysesataStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2171.CompoundModalAnalysesataStiffnessAnalysis)(self.wrapped.CompoundModalAnalysesataStiffness) if self.wrapped.CompoundModalAnalysesataStiffness else None

    @property
    def compound_torsional_system_deflection(self) -> '_2183.CompoundTorsionalSystemDeflectionAnalysis':
        '''CompoundTorsionalSystemDeflectionAnalysis: 'CompoundTorsionalSystemDeflection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2183.CompoundTorsionalSystemDeflectionAnalysis)(self.wrapped.CompoundTorsionalSystemDeflection) if self.wrapped.CompoundTorsionalSystemDeflection else None

    @property
    def compound_single_mesh_whine_analysis(self) -> '_2178.CompoundSingleMeshWhineAnalysisAnalysis':
        '''CompoundSingleMeshWhineAnalysisAnalysis: 'CompoundSingleMeshWhineAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2178.CompoundSingleMeshWhineAnalysisAnalysis)(self.wrapped.CompoundSingleMeshWhineAnalysis) if self.wrapped.CompoundSingleMeshWhineAnalysis else None

    @property
    def compound_advanced_system_deflection_sub_analysis(self) -> '_2163.CompoundAdvancedSystemDeflectionSubAnalysisAnalysis':
        '''CompoundAdvancedSystemDeflectionSubAnalysisAnalysis: 'CompoundAdvancedSystemDeflectionSubAnalysis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2163.CompoundAdvancedSystemDeflectionSubAnalysisAnalysis)(self.wrapped.CompoundAdvancedSystemDeflectionSubAnalysis) if self.wrapped.CompoundAdvancedSystemDeflectionSubAnalysis else None

    @property
    def compound_dynamic_modelfor_gear_whine(self) -> '_2167.CompoundDynamicModelforGearWhineAnalysis':
        '''CompoundDynamicModelforGearWhineAnalysis: 'CompoundDynamicModelforGearWhine' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2167.CompoundDynamicModelforGearWhineAnalysis)(self.wrapped.CompoundDynamicModelforGearWhine) if self.wrapped.CompoundDynamicModelforGearWhine else None

    @property
    def compound_dynamic_modelforat_speeds(self) -> '_2166.CompoundDynamicModelforatSpeedsAnalysis':
        '''CompoundDynamicModelforatSpeedsAnalysis: 'CompoundDynamicModelforatSpeeds' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2166.CompoundDynamicModelforatSpeedsAnalysis)(self.wrapped.CompoundDynamicModelforatSpeeds) if self.wrapped.CompoundDynamicModelforatSpeeds else None

    @property
    def compound_dynamic_modelata_stiffness(self) -> '_2165.CompoundDynamicModelataStiffnessAnalysis':
        '''CompoundDynamicModelataStiffnessAnalysis: 'CompoundDynamicModelataStiffness' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2165.CompoundDynamicModelataStiffnessAnalysis)(self.wrapped.CompoundDynamicModelataStiffness) if self.wrapped.CompoundDynamicModelataStiffness else None

    @property
    def compound_dynamic_modelfor_steady_state_synchronous_response(self) -> '_2168.CompoundDynamicModelforSteadyStateSynchronousResponseAnalysis':
        '''CompoundDynamicModelforSteadyStateSynchronousResponseAnalysis: 'CompoundDynamicModelforSteadyStateSynchronousResponse' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2168.CompoundDynamicModelforSteadyStateSynchronousResponseAnalysis)(self.wrapped.CompoundDynamicModelforSteadyStateSynchronousResponse) if self.wrapped.CompoundDynamicModelforSteadyStateSynchronousResponse else None

    @property
    def compound_modal_analysisfor_whine(self) -> '_2175.CompoundModalAnalysisforWhineAnalysis':
        '''CompoundModalAnalysisforWhineAnalysis: 'CompoundModalAnalysisforWhine' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2175.CompoundModalAnalysisforWhineAnalysis)(self.wrapped.CompoundModalAnalysisforWhine) if self.wrapped.CompoundModalAnalysisforWhine else None

    def create_load_cases(self, number_of_load_cases: 'int', token: '_6478.TaskProgress') -> 'List[_6022.LoadCase]':
        ''' 'CreateLoadCases' is the original name of this method.

        Args:
            number_of_load_cases (int)
            token (mastapy.TaskProgress)

        Returns:
            List[mastapy.system_model.analyses_and_results.static_loads.LoadCase]
        '''

        number_of_load_cases = int(number_of_load_cases)
        return conversion.pn_to_mp_objects_in_list(self.wrapped.CreateLoadCases(number_of_load_cases if number_of_load_cases else 0, token.wrapped if token else None), constructor.new(_6022.LoadCase))

    def output_default_report_to(self, file_path: 'str'):
        ''' 'OutputDefaultReportTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputDefaultReportTo(file_path if file_path else None)

    def get_default_report_with_encoded_images(self) -> 'str':
        ''' 'GetDefaultReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        '''

        method_result = self.wrapped.GetDefaultReportWithEncodedImages()
        return method_result

    def output_active_report_to(self, file_path: 'str'):
        ''' 'OutputActiveReportTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputActiveReportTo(file_path if file_path else None)

    def output_active_report_as_text_to(self, file_path: 'str'):
        ''' 'OutputActiveReportAsTextTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputActiveReportAsTextTo(file_path if file_path else None)

    def get_active_report_with_encoded_images(self) -> 'str':
        ''' 'GetActiveReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        '''

        method_result = self.wrapped.GetActiveReportWithEncodedImages()
        return method_result

    def output_named_report_to(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportTo(report_name if report_name else None, file_path if file_path else None)

    def output_named_report_as_masta_report(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportAsMastaReport' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsMastaReport(report_name if report_name else None, file_path if file_path else None)

    def output_named_report_as_text_to(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportAsTextTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsTextTo(report_name if report_name else None, file_path if file_path else None)

    def get_named_report_with_encoded_images(self, report_name: 'str') -> 'str':
        ''' 'GetNamedReportWithEncodedImages' is the original name of this method.

        Args:
            report_name (str)

        Returns:
            str
        '''

        report_name = str(report_name)
        method_result = self.wrapped.GetNamedReportWithEncodedImages(report_name if report_name else None)
        return method_result

    def analysis_of(self, analysis_type: '_6029.AnalysisType') -> '_2129.CompoundAnalysis':
        ''' 'AnalysisOf' is the original name of this method.

        Args:
            analysis_type (mastapy.system_model.analyses_and_results.static_loads.AnalysisType)

        Returns:
            mastapy.system_model.analyses_and_results.CompoundAnalysis
        '''

        analysis_type = conversion.mp_to_pn_enum(analysis_type)
        method_result = self.wrapped.AnalysisOf(analysis_type)
        return constructor.new(_2129.CompoundAnalysis)(method_result) if method_result else None
