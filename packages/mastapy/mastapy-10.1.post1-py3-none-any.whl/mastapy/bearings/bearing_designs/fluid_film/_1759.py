'''_1759.py

PlainGreaseFilledJournalBearing
'''


from mastapy.bearings.bearing_designs.fluid_film import (
    _1760, _1762, _1755, _1756,
    _1758, _1761
)
from mastapy._internal import enum_with_selected_value_runtime, constructor, conversion
from mastapy._internal.cast_exception import CastException
from mastapy._internal.python_net import python_net_import

_PLAIN_GREASE_FILLED_JOURNAL_BEARING = python_net_import('SMT.MastaAPI.Bearings.BearingDesigns.FluidFilm', 'PlainGreaseFilledJournalBearing')


__docformat__ = 'restructuredtext en'
__all__ = ('PlainGreaseFilledJournalBearing',)


class PlainGreaseFilledJournalBearing(_1761.PlainJournalBearing):
    '''PlainGreaseFilledJournalBearing

    This is a mastapy class.
    '''

    TYPE = _PLAIN_GREASE_FILLED_JOURNAL_BEARING

    __hash__ = None

    def __init__(self, instance_to_wrap: 'PlainGreaseFilledJournalBearing.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def housing_type(self) -> '_1760.PlainGreaseFilledJournalBearingHousingType':
        '''PlainGreaseFilledJournalBearingHousingType: 'HousingType' is the original name of this property.'''

        value = conversion.pn_to_mp_enum(self.wrapped.HousingType)
        return constructor.new(_1760.PlainGreaseFilledJournalBearingHousingType)(value) if value else None

    @housing_type.setter
    def housing_type(self, value: '_1760.PlainGreaseFilledJournalBearingHousingType'):
        value = value if value else None
        value = conversion.mp_to_pn_enum(value)
        self.wrapped.HousingType = value

    @property
    def housing_detail(self) -> '_1762.PlainJournalHousing':
        '''PlainJournalHousing: 'HousingDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1762.PlainJournalHousing)(self.wrapped.HousingDetail) if self.wrapped.HousingDetail else None

    @property
    def housing_detail_of_type_cylindrical_housing_journal_bearing(self) -> '_1755.CylindricalHousingJournalBearing':
        '''CylindricalHousingJournalBearing: 'HousingDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1755.CylindricalHousingJournalBearing.TYPE not in self.wrapped.HousingDetail.__class__.__mro__:
            raise CastException('Failed to cast housing_detail to CylindricalHousingJournalBearing. Expected: {}.'.format(self.wrapped.HousingDetail.__class__.__qualname__))

        return constructor.new(_1755.CylindricalHousingJournalBearing)(self.wrapped.HousingDetail) if self.wrapped.HousingDetail else None

    @property
    def housing_detail_of_type_machinery_encased_journal_bearing(self) -> '_1756.MachineryEncasedJournalBearing':
        '''MachineryEncasedJournalBearing: 'HousingDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1756.MachineryEncasedJournalBearing.TYPE not in self.wrapped.HousingDetail.__class__.__mro__:
            raise CastException('Failed to cast housing_detail to MachineryEncasedJournalBearing. Expected: {}.'.format(self.wrapped.HousingDetail.__class__.__qualname__))

        return constructor.new(_1756.MachineryEncasedJournalBearing)(self.wrapped.HousingDetail) if self.wrapped.HousingDetail else None

    @property
    def housing_detail_of_type_pedestal_journal_bearing(self) -> '_1758.PedestalJournalBearing':
        '''PedestalJournalBearing: 'HousingDetail' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1758.PedestalJournalBearing.TYPE not in self.wrapped.HousingDetail.__class__.__mro__:
            raise CastException('Failed to cast housing_detail to PedestalJournalBearing. Expected: {}.'.format(self.wrapped.HousingDetail.__class__.__qualname__))

        return constructor.new(_1758.PedestalJournalBearing)(self.wrapped.HousingDetail) if self.wrapped.HousingDetail else None
