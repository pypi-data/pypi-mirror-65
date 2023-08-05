'''_1521.py

RaceDetail
'''


from mastapy.bearings.tolerances import _1516
from mastapy._internal.python_net import python_net_import

_RACE_DETAIL = python_net_import('SMT.MastaAPI.Bearings.Tolerances', 'RaceDetail')


__docformat__ = 'restructuredtext en'
__all__ = ('RaceDetail',)


class RaceDetail(_1516.InterferenceDetail):
    '''RaceDetail

    This is a mastapy class.
    '''

    TYPE = _RACE_DETAIL

    __hash__ = None

    def __init__(self, instance_to_wrap: 'RaceDetail.TYPE'):
        super().__init__(instance_to_wrap)
