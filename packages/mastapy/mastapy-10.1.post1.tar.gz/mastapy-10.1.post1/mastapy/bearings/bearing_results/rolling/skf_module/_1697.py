'''_1697.py

GreaseLifeAndRelubricationInterval
'''


from mastapy._internal import constructor
from mastapy.bearings.bearing_results.rolling.skf_module import (
    _1696, _1699, _1698, _1704
)
from mastapy._internal.python_net import python_net_import

_GREASE_LIFE_AND_RELUBRICATION_INTERVAL = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling.SkfModule', 'GreaseLifeAndRelubricationInterval')


__docformat__ = 'restructuredtext en'
__all__ = ('GreaseLifeAndRelubricationInterval',)


class GreaseLifeAndRelubricationInterval(_1704.SKFCalculationResult):
    '''GreaseLifeAndRelubricationInterval

    This is a mastapy class.
    '''

    TYPE = _GREASE_LIFE_AND_RELUBRICATION_INTERVAL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GreaseLifeAndRelubricationInterval.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def speed_factor(self) -> 'float':
        '''float: 'SpeedFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SpeedFactor

    @property
    def grease(self) -> '_1696.Grease':
        '''Grease: 'Grease' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1696.Grease)(self.wrapped.Grease) if self.wrapped.Grease else None

    @property
    def initial_fill(self) -> '_1699.InitialFill':
        '''InitialFill: 'InitialFill' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1699.InitialFill)(self.wrapped.InitialFill) if self.wrapped.InitialFill else None

    @property
    def grease_quantity(self) -> '_1698.GreaseQuantity':
        '''GreaseQuantity: 'GreaseQuantity' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1698.GreaseQuantity)(self.wrapped.GreaseQuantity) if self.wrapped.GreaseQuantity else None
