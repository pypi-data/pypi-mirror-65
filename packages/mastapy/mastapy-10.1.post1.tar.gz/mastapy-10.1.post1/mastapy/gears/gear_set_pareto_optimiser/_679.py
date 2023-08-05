'''_679.py

GearSetOptimiserCandidate
'''


from typing import Callable

from mastapy._internal import constructor
from mastapy.gears.rating import _158, _165, _166
from mastapy._internal.cast_exception import CastException
from mastapy.gears.rating.zerol_bevel import _174
from mastapy.gears.rating.worm import _178, _179
from mastapy.gears.rating.straight_bevel_diff import _200
from mastapy.gears.rating.straight_bevel import _204
from mastapy.gears.rating.spiral_bevel import _207
from mastapy.gears.rating.klingelnberg_spiral_bevel import _210
from mastapy.gears.rating.klingelnberg_hypoid import _213
from mastapy.gears.rating.klingelnberg_conical import _216
from mastapy.gears.rating.hypoid import _243
from mastapy.gears.rating.face import _252, _253
from mastapy.gears.rating.cylindrical import _264, _265
from mastapy.gears.rating.conical import _327, _328
from mastapy.gears.rating.concept import _338, _339
from mastapy.gears.rating.bevel import _342
from mastapy.gears.rating.agma_gleason_conical import _353
from mastapy.gears.gear_set_pareto_optimiser import _675
from mastapy._internal.python_net import python_net_import

_GEAR_SET_OPTIMISER_CANDIDATE = python_net_import('SMT.MastaAPI.Gears.GearSetParetoOptimiser', 'GearSetOptimiserCandidate')


__docformat__ = 'restructuredtext en'
__all__ = ('GearSetOptimiserCandidate',)


class GearSetOptimiserCandidate(_675.DesignSpaceSearchCandidateBase['_158.AbstractGearSetRating', 'GearSetOptimiserCandidate']):
    '''GearSetOptimiserCandidate

    This is a mastapy class.
    '''

    TYPE = _GEAR_SET_OPTIMISER_CANDIDATE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearSetOptimiserCandidate.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def add_design(self) -> 'Callable[[], None]':
        '''Callable[[], None]: 'AddDesign' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AddDesign

    @property
    def candidate(self) -> '_158.AbstractGearSetRating':
        '''AbstractGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_158.AbstractGearSetRating)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_gear_set_duty_cycle_rating(self) -> '_165.GearSetDutyCycleRating':
        '''GearSetDutyCycleRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _165.GearSetDutyCycleRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to GearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new(_165.GearSetDutyCycleRating)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_gear_set_rating(self) -> '_166.GearSetRating':
        '''GearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _166.GearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to GearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new(_166.GearSetRating)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_zerol_bevel_gear_set_rating(self) -> '_174.ZerolBevelGearSetRating':
        '''ZerolBevelGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _174.ZerolBevelGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to ZerolBevelGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new(_174.ZerolBevelGearSetRating)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_worm_gear_set_duty_cycle_rating(self) -> '_178.WormGearSetDutyCycleRating':
        '''WormGearSetDutyCycleRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _178.WormGearSetDutyCycleRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to WormGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new(_178.WormGearSetDutyCycleRating)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_worm_gear_set_rating(self) -> '_179.WormGearSetRating':
        '''WormGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _179.WormGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to WormGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new(_179.WormGearSetRating)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_straight_bevel_diff_gear_set_rating(self) -> '_200.StraightBevelDiffGearSetRating':
        '''StraightBevelDiffGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _200.StraightBevelDiffGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to StraightBevelDiffGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new(_200.StraightBevelDiffGearSetRating)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_straight_bevel_gear_set_rating(self) -> '_204.StraightBevelGearSetRating':
        '''StraightBevelGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _204.StraightBevelGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to StraightBevelGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new(_204.StraightBevelGearSetRating)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_spiral_bevel_gear_set_rating(self) -> '_207.SpiralBevelGearSetRating':
        '''SpiralBevelGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _207.SpiralBevelGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to SpiralBevelGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new(_207.SpiralBevelGearSetRating)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_klingelnberg_cyclo_palloid_spiral_bevel_gear_set_rating(self) -> '_210.KlingelnbergCycloPalloidSpiralBevelGearSetRating':
        '''KlingelnbergCycloPalloidSpiralBevelGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _210.KlingelnbergCycloPalloidSpiralBevelGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to KlingelnbergCycloPalloidSpiralBevelGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new(_210.KlingelnbergCycloPalloidSpiralBevelGearSetRating)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_klingelnberg_cyclo_palloid_hypoid_gear_set_rating(self) -> '_213.KlingelnbergCycloPalloidHypoidGearSetRating':
        '''KlingelnbergCycloPalloidHypoidGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _213.KlingelnbergCycloPalloidHypoidGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to KlingelnbergCycloPalloidHypoidGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new(_213.KlingelnbergCycloPalloidHypoidGearSetRating)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_klingelnberg_cyclo_palloid_conical_gear_set_rating(self) -> '_216.KlingelnbergCycloPalloidConicalGearSetRating':
        '''KlingelnbergCycloPalloidConicalGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _216.KlingelnbergCycloPalloidConicalGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to KlingelnbergCycloPalloidConicalGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new(_216.KlingelnbergCycloPalloidConicalGearSetRating)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_hypoid_gear_set_rating(self) -> '_243.HypoidGearSetRating':
        '''HypoidGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _243.HypoidGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to HypoidGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new(_243.HypoidGearSetRating)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_face_gear_set_duty_cycle_rating(self) -> '_252.FaceGearSetDutyCycleRating':
        '''FaceGearSetDutyCycleRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _252.FaceGearSetDutyCycleRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to FaceGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new(_252.FaceGearSetDutyCycleRating)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_face_gear_set_rating(self) -> '_253.FaceGearSetRating':
        '''FaceGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _253.FaceGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to FaceGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new(_253.FaceGearSetRating)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_cylindrical_gear_set_duty_cycle_rating(self) -> '_264.CylindricalGearSetDutyCycleRating':
        '''CylindricalGearSetDutyCycleRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _264.CylindricalGearSetDutyCycleRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to CylindricalGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new(_264.CylindricalGearSetDutyCycleRating)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_cylindrical_gear_set_rating(self) -> '_265.CylindricalGearSetRating':
        '''CylindricalGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _265.CylindricalGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to CylindricalGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new(_265.CylindricalGearSetRating)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_conical_gear_set_duty_cycle_rating(self) -> '_327.ConicalGearSetDutyCycleRating':
        '''ConicalGearSetDutyCycleRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _327.ConicalGearSetDutyCycleRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to ConicalGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new(_327.ConicalGearSetDutyCycleRating)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_conical_gear_set_rating(self) -> '_328.ConicalGearSetRating':
        '''ConicalGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _328.ConicalGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to ConicalGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new(_328.ConicalGearSetRating)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_concept_gear_set_duty_cycle_rating(self) -> '_338.ConceptGearSetDutyCycleRating':
        '''ConceptGearSetDutyCycleRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _338.ConceptGearSetDutyCycleRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to ConceptGearSetDutyCycleRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new(_338.ConceptGearSetDutyCycleRating)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_concept_gear_set_rating(self) -> '_339.ConceptGearSetRating':
        '''ConceptGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _339.ConceptGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to ConceptGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new(_339.ConceptGearSetRating)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_bevel_gear_set_rating(self) -> '_342.BevelGearSetRating':
        '''BevelGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _342.BevelGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to BevelGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new(_342.BevelGearSetRating)(self.wrapped.Candidate) if self.wrapped.Candidate else None

    @property
    def candidate_of_type_agma_gleason_conical_gear_set_rating(self) -> '_353.AGMAGleasonConicalGearSetRating':
        '''AGMAGleasonConicalGearSetRating: 'Candidate' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _353.AGMAGleasonConicalGearSetRating.TYPE not in self.wrapped.Candidate.__class__.__mro__:
            raise CastException('Failed to cast candidate to AGMAGleasonConicalGearSetRating. Expected: {}.'.format(self.wrapped.Candidate.__class__.__qualname__))

        return constructor.new(_353.AGMAGleasonConicalGearSetRating)(self.wrapped.Candidate) if self.wrapped.Candidate else None
