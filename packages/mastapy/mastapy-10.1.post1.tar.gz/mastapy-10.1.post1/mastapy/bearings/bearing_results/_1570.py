'''_1570.py

LoadedBearingResults
'''


from typing import List

from mastapy._internal import constructor, enum_with_selected_value_runtime, conversion
from mastapy.bearings.bearing_results import _1581
from mastapy.math_utility.measured_vectors import _1118
from mastapy.bearings.bearing_designs import (
    _1729, _1730, _1731, _1732,
    _1733
)
from mastapy._internal.cast_exception import CastException
from mastapy.bearings.bearing_designs.rolling import (
    _1734, _1735, _1736, _1737,
    _1738, _1739, _1741, _1746,
    _1747, _1749, _1751, _1752,
    _1753, _1754, _1757, _1758,
    _1760, _1761, _1762, _1763,
    _1764, _1765
)
from mastapy.bearings.bearing_designs.fluid_film import (
    _1778, _1780, _1782, _1784,
    _1785, _1786
)
from mastapy.bearings.bearing_designs.concept import _1788, _1789, _1790
from mastapy.bearings.bearing_results.rolling import _1680
from mastapy.bearings import _1509
from mastapy._internal.python_net import python_net_import

_LOADED_BEARING_RESULTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults', 'LoadedBearingResults')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedBearingResults',)


class LoadedBearingResults(_1509.BearingLoadCaseResultsLightweight):
    '''LoadedBearingResults

    This is a mastapy class.
    '''

    TYPE = _LOADED_BEARING_RESULTS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadedBearingResults.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def angle_of_gravity_from_z_axis(self) -> 'float':
        '''float: 'AngleOfGravityFromZAxis' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.AngleOfGravityFromZAxis

    @property
    def signed_relative_speed(self) -> 'float':
        '''float: 'SignedRelativeSpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.SignedRelativeSpeed

    @property
    def relative_speed(self) -> 'float':
        '''float: 'RelativeSpeed' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RelativeSpeed

    @property
    def inner_race_speed(self) -> 'float':
        '''float: 'InnerRaceSpeed' is the original name of this property.'''

        return self.wrapped.InnerRaceSpeed

    @inner_race_speed.setter
    def inner_race_speed(self, value: 'float'):
        self.wrapped.InnerRaceSpeed = float(value) if value else 0.0

    @property
    def outer_race_speed(self) -> 'float':
        '''float: 'OuterRaceSpeed' is the original name of this property.'''

        return self.wrapped.OuterRaceSpeed

    @outer_race_speed.setter
    def outer_race_speed(self, value: 'float'):
        self.wrapped.OuterRaceSpeed = float(value) if value else 0.0

    @property
    def duration(self) -> 'float':
        '''float: 'Duration' is the original name of this property.'''

        return self.wrapped.Duration

    @duration.setter
    def duration(self, value: 'float'):
        self.wrapped.Duration = float(value) if value else 0.0

    @property
    def orientation(self) -> '_1581.Orientations':
        '''Orientations: 'Orientation' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.Orientation)
        return constructor.new(_1581.Orientations)(value) if value else None

    @orientation.setter
    def orientation(self, value: '_1581.Orientations'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.Orientation = value

    @property
    def specified_radial_internal_clearance(self) -> 'float':
        '''float: 'SpecifiedRadialInternalClearance' is the original name of this property.'''

        return self.wrapped.SpecifiedRadialInternalClearance

    @specified_radial_internal_clearance.setter
    def specified_radial_internal_clearance(self, value: 'float'):
        self.wrapped.SpecifiedRadialInternalClearance = float(value) if value else 0.0

    @property
    def specified_axial_internal_clearance(self) -> 'float':
        '''float: 'SpecifiedAxialInternalClearance' is the original name of this property.'''

        return self.wrapped.SpecifiedAxialInternalClearance

    @specified_axial_internal_clearance.setter
    def specified_axial_internal_clearance(self, value: 'float'):
        self.wrapped.SpecifiedAxialInternalClearance = float(value) if value else 0.0

    @property
    def axial_displacement_preload(self) -> 'float':
        '''float: 'AxialDisplacementPreload' is the original name of this property.'''

        return self.wrapped.AxialDisplacementPreload

    @axial_displacement_preload.setter
    def axial_displacement_preload(self, value: 'float'):
        self.wrapped.AxialDisplacementPreload = float(value) if value else 0.0

    @property
    def pre_assembly_axial_force_preload(self) -> 'float':
        '''float: 'PreAssemblyAxialForcePreload' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.PreAssemblyAxialForcePreload

    @property
    def relative_displacement_x(self) -> 'float':
        '''float: 'RelativeDisplacementX' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RelativeDisplacementX

    @property
    def relative_displacement_y(self) -> 'float':
        '''float: 'RelativeDisplacementY' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RelativeDisplacementY

    @property
    def relative_displacement_z(self) -> 'float':
        '''float: 'RelativeDisplacementZ' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RelativeDisplacementZ

    @property
    def relative_displacement_about_x(self) -> 'float':
        '''float: 'RelativeDisplacementAboutX' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RelativeDisplacementAboutX

    @property
    def relative_displacement_about_y(self) -> 'float':
        '''float: 'RelativeDisplacementAboutY' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RelativeDisplacementAboutY

    @property
    def relative_axial_displacement(self) -> 'float':
        '''float: 'RelativeAxialDisplacement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RelativeAxialDisplacement

    @property
    def relative_radial_displacement(self) -> 'float':
        '''float: 'RelativeRadialDisplacement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RelativeRadialDisplacement

    @property
    def relative_misalignment(self) -> 'float':
        '''float: 'RelativeMisalignment' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.RelativeMisalignment

    @property
    def magnitude_of_misalignment_normal_to_load_direction(self) -> 'float':
        '''float: 'MagnitudeOfMisalignmentNormalToLoadDirection' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.MagnitudeOfMisalignmentNormalToLoadDirection

    @property
    def force_results_are_overridden(self) -> 'bool':
        '''bool: 'ForceResultsAreOverridden' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ForceResultsAreOverridden

    @property
    def force_on_inner_race(self) -> '_1118.VectorWithLinearAndAngularComponents':
        '''VectorWithLinearAndAngularComponents: 'ForceOnInnerRace' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1118.VectorWithLinearAndAngularComponents)(self.wrapped.ForceOnInnerRace) if self.wrapped.ForceOnInnerRace else None

    @property
    def bearing(self) -> '_1729.BearingDesign':
        '''BearingDesign: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1729.BearingDesign)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_detailed_bearing(self) -> '_1730.DetailedBearing':
        '''DetailedBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1730.DetailedBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to DetailedBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new(_1730.DetailedBearing)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_dummy_rolling_bearing(self) -> '_1731.DummyRollingBearing':
        '''DummyRollingBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1731.DummyRollingBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to DummyRollingBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new(_1731.DummyRollingBearing)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_linear_bearing(self) -> '_1732.LinearBearing':
        '''LinearBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1732.LinearBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to LinearBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new(_1732.LinearBearing)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_non_linear_bearing(self) -> '_1733.NonLinearBearing':
        '''NonLinearBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1733.NonLinearBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to NonLinearBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new(_1733.NonLinearBearing)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_angular_contact_ball_bearing(self) -> '_1734.AngularContactBallBearing':
        '''AngularContactBallBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1734.AngularContactBallBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to AngularContactBallBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new(_1734.AngularContactBallBearing)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_angular_contact_thrust_ball_bearing(self) -> '_1735.AngularContactThrustBallBearing':
        '''AngularContactThrustBallBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1735.AngularContactThrustBallBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to AngularContactThrustBallBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new(_1735.AngularContactThrustBallBearing)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_asymmetric_spherical_roller_bearing(self) -> '_1736.AsymmetricSphericalRollerBearing':
        '''AsymmetricSphericalRollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1736.AsymmetricSphericalRollerBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to AsymmetricSphericalRollerBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new(_1736.AsymmetricSphericalRollerBearing)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_axial_thrust_cylindrical_roller_bearing(self) -> '_1737.AxialThrustCylindricalRollerBearing':
        '''AxialThrustCylindricalRollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1737.AxialThrustCylindricalRollerBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to AxialThrustCylindricalRollerBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new(_1737.AxialThrustCylindricalRollerBearing)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_axial_thrust_needle_roller_bearing(self) -> '_1738.AxialThrustNeedleRollerBearing':
        '''AxialThrustNeedleRollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1738.AxialThrustNeedleRollerBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to AxialThrustNeedleRollerBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new(_1738.AxialThrustNeedleRollerBearing)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_ball_bearing(self) -> '_1739.BallBearing':
        '''BallBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1739.BallBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to BallBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new(_1739.BallBearing)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_barrel_roller_bearing(self) -> '_1741.BarrelRollerBearing':
        '''BarrelRollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1741.BarrelRollerBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to BarrelRollerBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new(_1741.BarrelRollerBearing)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_cylindrical_roller_bearing(self) -> '_1746.CylindricalRollerBearing':
        '''CylindricalRollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1746.CylindricalRollerBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to CylindricalRollerBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new(_1746.CylindricalRollerBearing)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_deep_groove_ball_bearing(self) -> '_1747.DeepGrooveBallBearing':
        '''DeepGrooveBallBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1747.DeepGrooveBallBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to DeepGrooveBallBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new(_1747.DeepGrooveBallBearing)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_four_point_contact_ball_bearing(self) -> '_1749.FourPointContactBallBearing':
        '''FourPointContactBallBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1749.FourPointContactBallBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to FourPointContactBallBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new(_1749.FourPointContactBallBearing)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_multi_point_contact_ball_bearing(self) -> '_1751.MultiPointContactBallBearing':
        '''MultiPointContactBallBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1751.MultiPointContactBallBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to MultiPointContactBallBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new(_1751.MultiPointContactBallBearing)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_needle_roller_bearing(self) -> '_1752.NeedleRollerBearing':
        '''NeedleRollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1752.NeedleRollerBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to NeedleRollerBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new(_1752.NeedleRollerBearing)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_non_barrel_roller_bearing(self) -> '_1753.NonBarrelRollerBearing':
        '''NonBarrelRollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1753.NonBarrelRollerBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to NonBarrelRollerBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new(_1753.NonBarrelRollerBearing)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_roller_bearing(self) -> '_1754.RollerBearing':
        '''RollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1754.RollerBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to RollerBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new(_1754.RollerBearing)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_rolling_bearing(self) -> '_1757.RollingBearing':
        '''RollingBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1757.RollingBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to RollingBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new(_1757.RollingBearing)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_self_aligning_ball_bearing(self) -> '_1758.SelfAligningBallBearing':
        '''SelfAligningBallBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1758.SelfAligningBallBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to SelfAligningBallBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new(_1758.SelfAligningBallBearing)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_spherical_roller_bearing(self) -> '_1760.SphericalRollerBearing':
        '''SphericalRollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1760.SphericalRollerBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to SphericalRollerBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new(_1760.SphericalRollerBearing)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_spherical_roller_thrust_bearing(self) -> '_1761.SphericalRollerThrustBearing':
        '''SphericalRollerThrustBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1761.SphericalRollerThrustBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to SphericalRollerThrustBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new(_1761.SphericalRollerThrustBearing)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_taper_roller_bearing(self) -> '_1762.TaperRollerBearing':
        '''TaperRollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1762.TaperRollerBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to TaperRollerBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new(_1762.TaperRollerBearing)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_three_point_contact_ball_bearing(self) -> '_1763.ThreePointContactBallBearing':
        '''ThreePointContactBallBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1763.ThreePointContactBallBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to ThreePointContactBallBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new(_1763.ThreePointContactBallBearing)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_thrust_ball_bearing(self) -> '_1764.ThrustBallBearing':
        '''ThrustBallBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1764.ThrustBallBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to ThrustBallBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new(_1764.ThrustBallBearing)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_toroidal_roller_bearing(self) -> '_1765.ToroidalRollerBearing':
        '''ToroidalRollerBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1765.ToroidalRollerBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to ToroidalRollerBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new(_1765.ToroidalRollerBearing)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_pad_fluid_film_bearing(self) -> '_1778.PadFluidFilmBearing':
        '''PadFluidFilmBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1778.PadFluidFilmBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to PadFluidFilmBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new(_1778.PadFluidFilmBearing)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_plain_grease_filled_journal_bearing(self) -> '_1780.PlainGreaseFilledJournalBearing':
        '''PlainGreaseFilledJournalBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1780.PlainGreaseFilledJournalBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to PlainGreaseFilledJournalBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new(_1780.PlainGreaseFilledJournalBearing)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_plain_journal_bearing(self) -> '_1782.PlainJournalBearing':
        '''PlainJournalBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1782.PlainJournalBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to PlainJournalBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new(_1782.PlainJournalBearing)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_plain_oil_fed_journal_bearing(self) -> '_1784.PlainOilFedJournalBearing':
        '''PlainOilFedJournalBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1784.PlainOilFedJournalBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to PlainOilFedJournalBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new(_1784.PlainOilFedJournalBearing)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_tilting_pad_journal_bearing(self) -> '_1785.TiltingPadJournalBearing':
        '''TiltingPadJournalBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1785.TiltingPadJournalBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to TiltingPadJournalBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new(_1785.TiltingPadJournalBearing)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_tilting_pad_thrust_bearing(self) -> '_1786.TiltingPadThrustBearing':
        '''TiltingPadThrustBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1786.TiltingPadThrustBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to TiltingPadThrustBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new(_1786.TiltingPadThrustBearing)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_concept_axial_clearance_bearing(self) -> '_1788.ConceptAxialClearanceBearing':
        '''ConceptAxialClearanceBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1788.ConceptAxialClearanceBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to ConceptAxialClearanceBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new(_1788.ConceptAxialClearanceBearing)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_concept_clearance_bearing(self) -> '_1789.ConceptClearanceBearing':
        '''ConceptClearanceBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1789.ConceptClearanceBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to ConceptClearanceBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new(_1789.ConceptClearanceBearing)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def bearing_of_type_concept_radial_clearance_bearing(self) -> '_1790.ConceptRadialClearanceBearing':
        '''ConceptRadialClearanceBearing: 'Bearing' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1790.ConceptRadialClearanceBearing.TYPE not in self.wrapped.Bearing.__class__.__mro__:
            raise CastException('Failed to cast bearing to ConceptRadialClearanceBearing. Expected: {}.'.format(self.wrapped.Bearing.__class__.__qualname__))

        return constructor.new(_1790.ConceptRadialClearanceBearing)(self.wrapped.Bearing) if self.wrapped.Bearing else None

    @property
    def ring_results(self) -> 'List[_1680.RingForceAndDisplacement]':
        '''List[RingForceAndDisplacement]: 'RingResults' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.RingResults, constructor.new(_1680.RingForceAndDisplacement))
        return value
