'''_2035.py

BevelGear
'''


from mastapy.gears.gear_designs.bevel import _904
from mastapy._internal import constructor
from mastapy.gears.gear_designs.zerol_bevel import _707
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.straight_bevel_diff import _716
from mastapy.gears.gear_designs.straight_bevel import _720
from mastapy.gears.gear_designs.spiral_bevel import _724
from mastapy.system_model.part_model.gears import _2029
from mastapy._internal.python_net import python_net_import

_BEVEL_GEAR = python_net_import('SMT.MastaAPI.SystemModel.PartModel.Gears', 'BevelGear')


__docformat__ = 'restructuredtext en'
__all__ = ('BevelGear',)


class BevelGear(_2029.AGMAGleasonConicalGear):
    '''BevelGear

    This is a mastapy class.
    '''

    TYPE = _BEVEL_GEAR

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BevelGear.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def conical_gear_design(self) -> '_904.BevelGearDesign':
        '''BevelGearDesign: 'ConicalGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_904.BevelGearDesign)(self.wrapped.ConicalGearDesign) if self.wrapped.ConicalGearDesign else None

    @property
    def conical_gear_design_of_type_zerol_bevel_gear_design(self) -> '_707.ZerolBevelGearDesign':
        '''ZerolBevelGearDesign: 'ConicalGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _707.ZerolBevelGearDesign.TYPE not in self.wrapped.ConicalGearDesign.__class__.__mro__:
            raise CastException('Failed to cast conical_gear_design to ZerolBevelGearDesign. Expected: {}.'.format(self.wrapped.ConicalGearDesign.__class__.__qualname__))

        return constructor.new(_707.ZerolBevelGearDesign)(self.wrapped.ConicalGearDesign) if self.wrapped.ConicalGearDesign else None

    @property
    def conical_gear_design_of_type_straight_bevel_diff_gear_design(self) -> '_716.StraightBevelDiffGearDesign':
        '''StraightBevelDiffGearDesign: 'ConicalGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _716.StraightBevelDiffGearDesign.TYPE not in self.wrapped.ConicalGearDesign.__class__.__mro__:
            raise CastException('Failed to cast conical_gear_design to StraightBevelDiffGearDesign. Expected: {}.'.format(self.wrapped.ConicalGearDesign.__class__.__qualname__))

        return constructor.new(_716.StraightBevelDiffGearDesign)(self.wrapped.ConicalGearDesign) if self.wrapped.ConicalGearDesign else None

    @property
    def conical_gear_design_of_type_straight_bevel_gear_design(self) -> '_720.StraightBevelGearDesign':
        '''StraightBevelGearDesign: 'ConicalGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _720.StraightBevelGearDesign.TYPE not in self.wrapped.ConicalGearDesign.__class__.__mro__:
            raise CastException('Failed to cast conical_gear_design to StraightBevelGearDesign. Expected: {}.'.format(self.wrapped.ConicalGearDesign.__class__.__qualname__))

        return constructor.new(_720.StraightBevelGearDesign)(self.wrapped.ConicalGearDesign) if self.wrapped.ConicalGearDesign else None

    @property
    def conical_gear_design_of_type_spiral_bevel_gear_design(self) -> '_724.SpiralBevelGearDesign':
        '''SpiralBevelGearDesign: 'ConicalGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _724.SpiralBevelGearDesign.TYPE not in self.wrapped.ConicalGearDesign.__class__.__mro__:
            raise CastException('Failed to cast conical_gear_design to SpiralBevelGearDesign. Expected: {}.'.format(self.wrapped.ConicalGearDesign.__class__.__qualname__))

        return constructor.new(_724.SpiralBevelGearDesign)(self.wrapped.ConicalGearDesign) if self.wrapped.ConicalGearDesign else None

    @property
    def bevel_gear_design(self) -> '_904.BevelGearDesign':
        '''BevelGearDesign: 'BevelGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_904.BevelGearDesign)(self.wrapped.BevelGearDesign) if self.wrapped.BevelGearDesign else None

    @property
    def bevel_gear_design_of_type_zerol_bevel_gear_design(self) -> '_707.ZerolBevelGearDesign':
        '''ZerolBevelGearDesign: 'BevelGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _707.ZerolBevelGearDesign.TYPE not in self.wrapped.BevelGearDesign.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_design to ZerolBevelGearDesign. Expected: {}.'.format(self.wrapped.BevelGearDesign.__class__.__qualname__))

        return constructor.new(_707.ZerolBevelGearDesign)(self.wrapped.BevelGearDesign) if self.wrapped.BevelGearDesign else None

    @property
    def bevel_gear_design_of_type_straight_bevel_diff_gear_design(self) -> '_716.StraightBevelDiffGearDesign':
        '''StraightBevelDiffGearDesign: 'BevelGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _716.StraightBevelDiffGearDesign.TYPE not in self.wrapped.BevelGearDesign.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_design to StraightBevelDiffGearDesign. Expected: {}.'.format(self.wrapped.BevelGearDesign.__class__.__qualname__))

        return constructor.new(_716.StraightBevelDiffGearDesign)(self.wrapped.BevelGearDesign) if self.wrapped.BevelGearDesign else None

    @property
    def bevel_gear_design_of_type_straight_bevel_gear_design(self) -> '_720.StraightBevelGearDesign':
        '''StraightBevelGearDesign: 'BevelGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _720.StraightBevelGearDesign.TYPE not in self.wrapped.BevelGearDesign.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_design to StraightBevelGearDesign. Expected: {}.'.format(self.wrapped.BevelGearDesign.__class__.__qualname__))

        return constructor.new(_720.StraightBevelGearDesign)(self.wrapped.BevelGearDesign) if self.wrapped.BevelGearDesign else None

    @property
    def bevel_gear_design_of_type_spiral_bevel_gear_design(self) -> '_724.SpiralBevelGearDesign':
        '''SpiralBevelGearDesign: 'BevelGearDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _724.SpiralBevelGearDesign.TYPE not in self.wrapped.BevelGearDesign.__class__.__mro__:
            raise CastException('Failed to cast bevel_gear_design to SpiralBevelGearDesign. Expected: {}.'.format(self.wrapped.BevelGearDesign.__class__.__qualname__))

        return constructor.new(_724.SpiralBevelGearDesign)(self.wrapped.BevelGearDesign) if self.wrapped.BevelGearDesign else None
