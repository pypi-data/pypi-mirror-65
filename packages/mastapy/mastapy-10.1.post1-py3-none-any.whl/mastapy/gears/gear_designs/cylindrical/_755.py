'''_755.py

BaffleLoss
'''


from typing import List

from mastapy._internal import constructor
from mastapy.utility import _1120
from mastapy.gears.gear_designs.cylindrical import _819
from mastapy._internal.python_net import python_net_import

_BAFFLE_LOSS = python_net_import('SMT.MastaAPI.Gears.GearDesigns.Cylindrical', 'BaffleLoss')


__docformat__ = 'restructuredtext en'
__all__ = ('BaffleLoss',)


class BaffleLoss(_1120.IndependentReportablePropertiesBase['_819.TiffAnalysisSettings']):
    '''BaffleLoss

    This is a mastapy class.
    '''

    TYPE = _BAFFLE_LOSS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'BaffleLoss.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def baffle_loss_factor(self) -> 'float':
        '''float: 'BaffleLossFactor' is the original name of this property.'''

        return self.wrapped.BaffleLossFactor

    @baffle_loss_factor.setter
    def baffle_loss_factor(self, value: 'float'):
        self.wrapped.BaffleLossFactor = float(value) if value else 0.0

    @property
    def baffle_type(self) -> 'str':
        '''str: 'BaffleType' is the original name of this property.'''

        return self.wrapped.BaffleType

    @baffle_type.setter
    def baffle_type(self, value: 'str'):
        self.wrapped.BaffleType = str(value) if value else None

    @property
    def report_names(self) -> 'List[str]':
        '''List[str]: 'ReportNames' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return self.wrapped.ReportNames

    def output_default_report_to(self, file_path: 'str'):
        ''' 'OutputDefaultReportTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputDefaultReportTo(file_path if file_path else None)

    def get_default_report_with_encoded_images(self) -> 'str':
        ''' 'GetDefaultReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        '''

        method_result = self.wrapped.GetDefaultReportWithEncodedImages()
        return method_result

    def output_active_report_to(self, file_path: 'str'):
        ''' 'OutputActiveReportTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputActiveReportTo(file_path if file_path else None)

    def output_active_report_as_text_to(self, file_path: 'str'):
        ''' 'OutputActiveReportAsTextTo' is the original name of this method.

        Args:
            file_path (str)
        '''

        file_path = str(file_path)
        self.wrapped.OutputActiveReportAsTextTo(file_path if file_path else None)

    def get_active_report_with_encoded_images(self) -> 'str':
        ''' 'GetActiveReportWithEncodedImages' is the original name of this method.

        Returns:
            str
        '''

        method_result = self.wrapped.GetActiveReportWithEncodedImages()
        return method_result

    def output_named_report_to(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportTo(report_name if report_name else None, file_path if file_path else None)

    def output_named_report_as_masta_report(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportAsMastaReport' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsMastaReport(report_name if report_name else None, file_path if file_path else None)

    def output_named_report_as_text_to(self, report_name: 'str', file_path: 'str'):
        ''' 'OutputNamedReportAsTextTo' is the original name of this method.

        Args:
            report_name (str)
            file_path (str)
        '''

        report_name = str(report_name)
        file_path = str(file_path)
        self.wrapped.OutputNamedReportAsTextTo(report_name if report_name else None, file_path if file_path else None)

    def get_named_report_with_encoded_images(self, report_name: 'str') -> 'str':
        ''' 'GetNamedReportWithEncodedImages' is the original name of this method.

        Args:
            report_name (str)

        Returns:
            str
        '''

        report_name = str(report_name)
        method_result = self.wrapped.GetNamedReportWithEncodedImages(report_name if report_name else None)
        return method_result
