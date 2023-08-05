'''_2125.py

BearingDetailConfiguration
'''


from mastapy.system_model.part_model.configurations import _2127, _2126
from mastapy.system_model.part_model import _1962
from mastapy.bearings.bearing_designs import _1708
from mastapy._internal.python_net import python_net_import

_BEARING_DETAIL_CONFIGURATION = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Configurations', 'BearingDetailConfiguration')


__docformat__ = 'restructuredtext en'
__all__ = ('BearingDetailConfiguration',)


class BearingDetailConfiguration(_2127.PartDetailConfiguration['_2126.BearingDetailSelection', '_1962.Bearing', '_1708.BearingDesign']):
    '''BearingDetailConfiguration

    This is a mastapy class.
    '''

    TYPE = _BEARING_DETAIL_CONFIGURATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BearingDetailConfiguration.TYPE'):
        super().__init__(instance_to_wrap)
