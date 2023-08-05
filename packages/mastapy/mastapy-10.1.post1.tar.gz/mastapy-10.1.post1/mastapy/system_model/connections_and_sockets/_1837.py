'''_1837.py

CVTPulleySocket
'''


from mastapy.system_model.connections_and_sockets import _1849
from mastapy._internal.python_net import python_net_import

_CVT_PULLEY_SOCKET = python_net_import('SMT.MastaAPI.SystemModel.ConnectionsAndSockets', 'CVTPulleySocket')


__docformat__ = 'restructuredtext en'
__all__ = ('CVTPulleySocket',)


class CVTPulleySocket(_1849.PulleySocket):
    '''CVTPulleySocket

    This is a mastapy class.
    '''

    TYPE = _CVT_PULLEY_SOCKET

    __hash__ = None

    def __init__(self, instance_to_wrap: 'CVTPulleySocket.TYPE'):
        super().__init__(instance_to_wrap)
