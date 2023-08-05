'''_1991.py

Connector
'''


from typing import Optional

from mastapy.system_model.part_model.shaft_model import _2021
from mastapy.system_model.connections_and_sockets import _1835
from mastapy._internal import constructor
from mastapy.system_model.part_model import _1989, _2005
from mastapy._internal.python_net import python_net_import

_CONNECTOR = python_net_import('SMT.MastaAPI.SystemModel.PartModel', 'Connector')


__docformat__ = 'restructuredtext en'
__all__ = ('Connector',)


class Connector(_2005.MountableComponent):
    '''Connector

    This is a mastapy class.
    '''

    TYPE = _CONNECTOR

    __hash__ = None

    def __init__(self, instance_to_wrap: 'Connector.TYPE'):
        super().__init__(instance_to_wrap)

    def house_in(self, shaft: '_2021.Shaft', offset: Optional['float'] = float('nan')) -> '_1835.Connection':
        ''' 'HouseIn' is the original name of this method.

        Args:
            shaft (mastapy.system_model.part_model.shaft_model.Shaft)
            offset (float, optional)

        Returns:
            mastapy.system_model.connections_and_sockets.Connection
        '''

        offset = float(offset)
        method_result = self.wrapped.HouseIn(shaft.wrapped if shaft else None, offset if offset else 0.0)
        return constructor.new(_1835.Connection)(method_result) if method_result else None

    def try_house_in(self, shaft: '_2021.Shaft', offset: Optional['float'] = float('nan')) -> '_1989.ComponentsConnectedResult':
        ''' 'TryHouseIn' is the original name of this method.

        Args:
            shaft (mastapy.system_model.part_model.shaft_model.Shaft)
            offset (float, optional)

        Returns:
            mastapy.system_model.part_model.ComponentsConnectedResult
        '''

        offset = float(offset)
        method_result = self.wrapped.TryHouseIn(shaft.wrapped if shaft else None, offset if offset else 0.0)
        return constructor.new(_1989.ComponentsConnectedResult)(method_result) if method_result else None
