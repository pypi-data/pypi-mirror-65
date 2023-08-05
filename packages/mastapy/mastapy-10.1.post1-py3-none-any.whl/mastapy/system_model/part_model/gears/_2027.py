'''_2027.py

ActiveGearSetDesignSelection
'''


from mastapy.system_model.part_model.configurations import _2128
from mastapy.system_model.part_model.gears import _2048
from mastapy.gears.gear_designs import _705
from mastapy._internal.python_net import python_net_import

_ACTIVE_GEAR_SET_DESIGN_SELECTION = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'ActiveGearSetDesignSelection')


__docformat__ = 'restructuredtext en'
__all__ = ('ActiveGearSetDesignSelection',)


class ActiveGearSetDesignSelection(_2128.PartDetailSelection['_2048.GearSet', '_705.GearSetDesign']):
    '''ActiveGearSetDesignSelection

    This is a mastapy class.
    '''

    TYPE = _ACTIVE_GEAR_SET_DESIGN_SELECTION

    __hash__ = None

    def __init__(self, instance_to_wrap: 'ActiveGearSetDesignSelection.TYPE'):
        super().__init__(instance_to_wrap)
