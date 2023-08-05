'''_704.py

GearMeshDesign
'''


from mastapy._internal import constructor
from mastapy.gears.gear_designs import _702, _703
from mastapy.gears.gear_designs.zerol_bevel import _707
from mastapy._internal.cast_exception import CastException
from mastapy.gears.gear_designs.worm import _711, _712, _715
from mastapy.gears.gear_designs.straight_bevel_diff import _716
from mastapy.gears.gear_designs.straight_bevel import _720
from mastapy.gears.gear_designs.spiral_bevel import _724
from mastapy.gears.gear_designs.klingelnberg_spiral_bevel import _728
from mastapy.gears.gear_designs.klingelnberg_hypoid import _732
from mastapy.gears.gear_designs.klingelnberg_conical import _736
from mastapy.gears.gear_designs.hypoid import _740
from mastapy.gears.gear_designs.face import _744, _749, _752
from mastapy.gears.gear_designs.cylindrical import _766, _787
from mastapy.gears.gear_designs.conical import _878
from mastapy.gears.gear_designs.concept import _900
from mastapy.gears.gear_designs.bevel import _904
from mastapy.gears.gear_designs.agma_gleason_conical import _917
from mastapy._internal.python_net import python_net_import

_GEAR_MESH_DESIGN = python_net_import('SMT.MastaAPI.Gears.GearDesigns', 'GearMeshDesign')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMeshDesign',)


class GearMeshDesign(_703.GearDesignComponent):
    '''GearMeshDesign

    This is a mastapy class.
    '''

    TYPE = _GEAR_MESH_DESIGN

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearMeshDesign.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def name(self) -> 'str':
        '''str: 'Name' is the original name of this property.'''

        return self.wrapped.Name

    @name.setter
    def name(self, value: 'str'):
        self.wrapped.Name = str(value) if value else None

    @property
    def speed_ratio_a_to_b(self) -> 'float':
        '''float: 'SpeedRatioAToB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SpeedRatioAToB

    @property
    def torque_ratio_a_to_b(self) -> 'float':
        '''float: 'TorqueRatioAToB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TorqueRatioAToB

    @property
    def highest_common_factor_of_teeth_numbers(self) -> 'int':
        '''int: 'HighestCommonFactorOfTeethNumbers' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HighestCommonFactorOfTeethNumbers

    @property
    def has_hunting_ratio(self) -> 'bool':
        '''bool: 'HasHuntingRatio' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HasHuntingRatio

    @property
    def hunting_tooth_factor(self) -> 'float':
        '''float: 'HuntingToothFactor' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.HuntingToothFactor

    @property
    def axial_contact_ratio_rating_for_nvh(self) -> 'float':
        '''float: 'AxialContactRatioRatingForNVH' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AxialContactRatioRatingForNVH

    @property
    def transverse_contact_ratio_rating_for_nvh(self) -> 'float':
        '''float: 'TransverseContactRatioRatingForNVH' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TransverseContactRatioRatingForNVH

    @property
    def transverse_and_axial_contact_ratio_rating_for_nvh(self) -> 'float':
        '''float: 'TransverseAndAxialContactRatioRatingForNVH' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.TransverseAndAxialContactRatioRatingForNVH

    @property
    def gear_a(self) -> '_702.GearDesign':
        '''GearDesign: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_702.GearDesign)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_zerol_bevel_gear_design(self) -> '_707.ZerolBevelGearDesign':
        '''ZerolBevelGearDesign: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _707.ZerolBevelGearDesign.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ZerolBevelGearDesign. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_707.ZerolBevelGearDesign)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_worm_design(self) -> '_711.WormDesign':
        '''WormDesign: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _711.WormDesign.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to WormDesign. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_711.WormDesign)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_worm_gear_design(self) -> '_712.WormGearDesign':
        '''WormGearDesign: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _712.WormGearDesign.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to WormGearDesign. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_712.WormGearDesign)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_worm_wheel_design(self) -> '_715.WormWheelDesign':
        '''WormWheelDesign: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _715.WormWheelDesign.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to WormWheelDesign. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_715.WormWheelDesign)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_straight_bevel_diff_gear_design(self) -> '_716.StraightBevelDiffGearDesign':
        '''StraightBevelDiffGearDesign: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _716.StraightBevelDiffGearDesign.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to StraightBevelDiffGearDesign. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_716.StraightBevelDiffGearDesign)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_straight_bevel_gear_design(self) -> '_720.StraightBevelGearDesign':
        '''StraightBevelGearDesign: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _720.StraightBevelGearDesign.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to StraightBevelGearDesign. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_720.StraightBevelGearDesign)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_spiral_bevel_gear_design(self) -> '_724.SpiralBevelGearDesign':
        '''SpiralBevelGearDesign: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _724.SpiralBevelGearDesign.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to SpiralBevelGearDesign. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_724.SpiralBevelGearDesign)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_design(self) -> '_728.KlingelnbergCycloPalloidSpiralBevelGearDesign':
        '''KlingelnbergCycloPalloidSpiralBevelGearDesign: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _728.KlingelnbergCycloPalloidSpiralBevelGearDesign.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to KlingelnbergCycloPalloidSpiralBevelGearDesign. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_728.KlingelnbergCycloPalloidSpiralBevelGearDesign)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_klingelnberg_cyclo_palloid_hypoid_gear_design(self) -> '_732.KlingelnbergCycloPalloidHypoidGearDesign':
        '''KlingelnbergCycloPalloidHypoidGearDesign: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _732.KlingelnbergCycloPalloidHypoidGearDesign.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to KlingelnbergCycloPalloidHypoidGearDesign. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_732.KlingelnbergCycloPalloidHypoidGearDesign)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_klingelnberg_conical_gear_design(self) -> '_736.KlingelnbergConicalGearDesign':
        '''KlingelnbergConicalGearDesign: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _736.KlingelnbergConicalGearDesign.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to KlingelnbergConicalGearDesign. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_736.KlingelnbergConicalGearDesign)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_hypoid_gear_design(self) -> '_740.HypoidGearDesign':
        '''HypoidGearDesign: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _740.HypoidGearDesign.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to HypoidGearDesign. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_740.HypoidGearDesign)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_face_gear_design(self) -> '_744.FaceGearDesign':
        '''FaceGearDesign: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _744.FaceGearDesign.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to FaceGearDesign. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_744.FaceGearDesign)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_face_gear_pinion_design(self) -> '_749.FaceGearPinionDesign':
        '''FaceGearPinionDesign: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _749.FaceGearPinionDesign.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to FaceGearPinionDesign. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_749.FaceGearPinionDesign)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_face_gear_wheel_design(self) -> '_752.FaceGearWheelDesign':
        '''FaceGearWheelDesign: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _752.FaceGearWheelDesign.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to FaceGearWheelDesign. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_752.FaceGearWheelDesign)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_cylindrical_gear_design(self) -> '_766.CylindricalGearDesign':
        '''CylindricalGearDesign: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _766.CylindricalGearDesign.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to CylindricalGearDesign. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_766.CylindricalGearDesign)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_cylindrical_planet_gear_design(self) -> '_787.CylindricalPlanetGearDesign':
        '''CylindricalPlanetGearDesign: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _787.CylindricalPlanetGearDesign.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to CylindricalPlanetGearDesign. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_787.CylindricalPlanetGearDesign)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_conical_gear_design(self) -> '_878.ConicalGearDesign':
        '''ConicalGearDesign: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _878.ConicalGearDesign.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ConicalGearDesign. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_878.ConicalGearDesign)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_concept_gear_design(self) -> '_900.ConceptGearDesign':
        '''ConceptGearDesign: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _900.ConceptGearDesign.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ConceptGearDesign. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_900.ConceptGearDesign)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_bevel_gear_design(self) -> '_904.BevelGearDesign':
        '''BevelGearDesign: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _904.BevelGearDesign.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to BevelGearDesign. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_904.BevelGearDesign)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_agma_gleason_conical_gear_design(self) -> '_917.AGMAGleasonConicalGearDesign':
        '''AGMAGleasonConicalGearDesign: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _917.AGMAGleasonConicalGearDesign.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to AGMAGleasonConicalGearDesign. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_917.AGMAGleasonConicalGearDesign)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_b(self) -> '_702.GearDesign':
        '''GearDesign: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_702.GearDesign)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_zerol_bevel_gear_design(self) -> '_707.ZerolBevelGearDesign':
        '''ZerolBevelGearDesign: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _707.ZerolBevelGearDesign.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ZerolBevelGearDesign. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_707.ZerolBevelGearDesign)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_worm_design(self) -> '_711.WormDesign':
        '''WormDesign: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _711.WormDesign.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to WormDesign. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_711.WormDesign)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_worm_gear_design(self) -> '_712.WormGearDesign':
        '''WormGearDesign: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _712.WormGearDesign.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to WormGearDesign. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_712.WormGearDesign)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_worm_wheel_design(self) -> '_715.WormWheelDesign':
        '''WormWheelDesign: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _715.WormWheelDesign.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to WormWheelDesign. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_715.WormWheelDesign)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_straight_bevel_diff_gear_design(self) -> '_716.StraightBevelDiffGearDesign':
        '''StraightBevelDiffGearDesign: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _716.StraightBevelDiffGearDesign.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to StraightBevelDiffGearDesign. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_716.StraightBevelDiffGearDesign)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_straight_bevel_gear_design(self) -> '_720.StraightBevelGearDesign':
        '''StraightBevelGearDesign: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _720.StraightBevelGearDesign.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to StraightBevelGearDesign. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_720.StraightBevelGearDesign)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_spiral_bevel_gear_design(self) -> '_724.SpiralBevelGearDesign':
        '''SpiralBevelGearDesign: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _724.SpiralBevelGearDesign.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to SpiralBevelGearDesign. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_724.SpiralBevelGearDesign)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_design(self) -> '_728.KlingelnbergCycloPalloidSpiralBevelGearDesign':
        '''KlingelnbergCycloPalloidSpiralBevelGearDesign: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _728.KlingelnbergCycloPalloidSpiralBevelGearDesign.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to KlingelnbergCycloPalloidSpiralBevelGearDesign. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_728.KlingelnbergCycloPalloidSpiralBevelGearDesign)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_klingelnberg_cyclo_palloid_hypoid_gear_design(self) -> '_732.KlingelnbergCycloPalloidHypoidGearDesign':
        '''KlingelnbergCycloPalloidHypoidGearDesign: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _732.KlingelnbergCycloPalloidHypoidGearDesign.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to KlingelnbergCycloPalloidHypoidGearDesign. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_732.KlingelnbergCycloPalloidHypoidGearDesign)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_klingelnberg_conical_gear_design(self) -> '_736.KlingelnbergConicalGearDesign':
        '''KlingelnbergConicalGearDesign: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _736.KlingelnbergConicalGearDesign.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to KlingelnbergConicalGearDesign. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_736.KlingelnbergConicalGearDesign)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_hypoid_gear_design(self) -> '_740.HypoidGearDesign':
        '''HypoidGearDesign: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _740.HypoidGearDesign.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to HypoidGearDesign. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_740.HypoidGearDesign)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_face_gear_design(self) -> '_744.FaceGearDesign':
        '''FaceGearDesign: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _744.FaceGearDesign.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to FaceGearDesign. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_744.FaceGearDesign)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_face_gear_pinion_design(self) -> '_749.FaceGearPinionDesign':
        '''FaceGearPinionDesign: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _749.FaceGearPinionDesign.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to FaceGearPinionDesign. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_749.FaceGearPinionDesign)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_face_gear_wheel_design(self) -> '_752.FaceGearWheelDesign':
        '''FaceGearWheelDesign: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _752.FaceGearWheelDesign.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to FaceGearWheelDesign. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_752.FaceGearWheelDesign)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_cylindrical_gear_design(self) -> '_766.CylindricalGearDesign':
        '''CylindricalGearDesign: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _766.CylindricalGearDesign.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to CylindricalGearDesign. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_766.CylindricalGearDesign)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_cylindrical_planet_gear_design(self) -> '_787.CylindricalPlanetGearDesign':
        '''CylindricalPlanetGearDesign: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _787.CylindricalPlanetGearDesign.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to CylindricalPlanetGearDesign. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_787.CylindricalPlanetGearDesign)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_conical_gear_design(self) -> '_878.ConicalGearDesign':
        '''ConicalGearDesign: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _878.ConicalGearDesign.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ConicalGearDesign. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_878.ConicalGearDesign)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_concept_gear_design(self) -> '_900.ConceptGearDesign':
        '''ConceptGearDesign: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _900.ConceptGearDesign.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ConceptGearDesign. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_900.ConceptGearDesign)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_bevel_gear_design(self) -> '_904.BevelGearDesign':
        '''BevelGearDesign: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _904.BevelGearDesign.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to BevelGearDesign. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_904.BevelGearDesign)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_agma_gleason_conical_gear_design(self) -> '_917.AGMAGleasonConicalGearDesign':
        '''AGMAGleasonConicalGearDesign: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _917.AGMAGleasonConicalGearDesign.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to AGMAGleasonConicalGearDesign. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_917.AGMAGleasonConicalGearDesign)(self.wrapped.GearB) if self.wrapped.GearB else None
