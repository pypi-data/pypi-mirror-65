'''_3582.py

StraightBevelSunGearParametricStudyTool
'''


from mastapy.system_model.part_model.gears import _2088
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.parametric_study_tools import _3576
from mastapy._internal.python_net import python_net_import

_STRAIGHT_BEVEL_SUN_GEAR_PARAMETRIC_STUDY_TOOL = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.ParametricStudyTools', 'StraightBevelSunGearParametricStudyTool')


__docformat__ = 'restructuredtext en'
__all__ = ('StraightBevelSunGearParametricStudyTool',)


class StraightBevelSunGearParametricStudyTool(_3576.StraightBevelDiffGearParametricStudyTool):
    '''StraightBevelSunGearParametricStudyTool

    This is a mastapy class.
    '''

    TYPE = _STRAIGHT_BEVEL_SUN_GEAR_PARAMETRIC_STUDY_TOOL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'StraightBevelSunGearParametricStudyTool.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2088.StraightBevelSunGear':
        '''StraightBevelSunGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2088.StraightBevelSunGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
