'''_1815.py

CylindricalGearOptimisationStrategy
'''


from mastapy.system_model.optimization import _1821, _1816
from mastapy._internal.python_net import python_net_import

_CYLINDRICAL_GEAR_OPTIMISATION_STRATEGY = python_net_import('SMT.MastaAPI.SystemModel.Optimization', 'CylindricalGearOptimisationStrategy')


__docformat__ = 'restructuredtext en'
__all__ = ('CylindricalGearOptimisationStrategy',)


class CylindricalGearOptimisationStrategy(_1821.OptimizationStrategy['_1816.CylindricalGearOptimizationStep']):
    '''CylindricalGearOptimisationStrategy

    This is a mastapy class.
    '''

    TYPE = _CYLINDRICAL_GEAR_OPTIMISATION_STRATEGY

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CylindricalGearOptimisationStrategy.TYPE'):
        super().__init__(instance_to_wrap)
