'''_4958.py

BevelDifferentialSunGearMultiBodyDynamicsAnalysis
'''


from mastapy.system_model.part_model.gears import _2034
from mastapy._internal import constructor
from mastapy.system_model.analyses_and_results.mbd_analyses import _4955
from mastapy._internal.python_net import python_net_import

_BEVEL_DIFFERENTIAL_SUN_GEAR_MULTI_BODY_DYNAMICS_ANALYSIS = python_net_import('SMT.MastaAPI.SystemModel.AnalysesAndResults.MBDAnalyses', 'BevelDifferentialSunGearMultiBodyDynamicsAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelDifferentialSunGearMultiBodyDynamicsAnalysis',)


class BevelDifferentialSunGearMultiBodyDynamicsAnalysis(_4955.BevelDifferentialGearMultiBodyDynamicsAnalysis):
    '''BevelDifferentialSunGearMultiBodyDynamicsAnalysis

    This is a mastapy class.
    '''

    TYPE = _BEVEL_DIFFERENTIAL_SUN_GEAR_MULTI_BODY_DYNAMICS_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelDifferentialSunGearMultiBodyDynamicsAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def component_design(self) -> '_2034.BevelDifferentialSunGear':
        '''BevelDifferentialSunGear: 'ComponentDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_2034.BevelDifferentialSunGear)(self.wrapped.ComponentDesign) if self.wrapped.ComponentDesign else None
