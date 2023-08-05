'''_2121.py

PartToPartShearCoupling
'''


from mastapy.system_model.part_model.couplings import _2117
from mastapy._internal.python_net import python_net_import

_PART_TO_PART_SHEAR_COUPLING = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Couplings', 'PartToPartShearCoupling')


__docformat__ = 'restructuredtext en'
__all__ = ('PartToPartShearCoupling',)


class PartToPartShearCoupling(_2117.Coupling):
    '''PartToPartShearCoupling

    This is a mastapy class.
    '''

    TYPE = _PART_TO_PART_SHEAR_COUPLING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PartToPartShearCoupling.TYPE'):
        super().__init__(instance_to_wrap)
