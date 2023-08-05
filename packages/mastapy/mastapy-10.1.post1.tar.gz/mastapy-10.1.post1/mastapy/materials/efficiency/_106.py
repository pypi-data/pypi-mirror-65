'''_106.py

OilVolumeSpecification
'''


from mastapy.utility import _1134
from mastapy._internal.python_net import python_net_import

_OIL_VOLUME_SPECIFICATION = python_net_import('SMT.MastaAPI.Materials.Efficiency', 'OilVolumeSpecification')


__docformat__ = 'restructuredtext en'
__all__ = ('OilVolumeSpecification',)


class OilVolumeSpecification(_1134.IndependentReportablePropertiesBase['OilVolumeSpecification']):
    '''OilVolumeSpecification

    This is a mastapy class.
    '''

    TYPE = _OIL_VOLUME_SPECIFICATION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OilVolumeSpecification.TYPE'):
        super().__init__(instance_to_wrap)
