'''_2121.py

ActiveImportedFESelection
'''


from mastapy.system_model.part_model.configurations import _2128
from mastapy.system_model.part_model import _1978
from mastapy.system_model.imported_fes import _1912
from mastapy._internal.python_net import python_net_import

_ACTIVE_IMPORTED_FE_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Configurations', 'ActiveImportedFESelection')


__docformat__ = 'restructuredtext en'
__all__ = ('ActiveImportedFESelection',)


class ActiveImportedFESelection(_2128.PartDetailSelection['_1978.ImportedFEComponent', '_1912.ImportedFE']):
    '''ActiveImportedFESelection

    This is a mastapy class.
    '''

    TYPE = _ACTIVE_IMPORTED_FE_SELECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ActiveImportedFESelection.TYPE'):
        super().__init__(instance_to_wrap)
