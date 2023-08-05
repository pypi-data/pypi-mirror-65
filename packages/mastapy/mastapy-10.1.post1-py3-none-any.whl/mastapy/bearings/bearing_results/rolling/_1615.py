'''_1615.py

LoadedBallBearingResults
'''


from mastapy.bearings.bearing_results.rolling import _1686, _1643
from mastapy._internal import constructor
from mastapy._internal.python_net import python_net_import

_LOADED_BALL_BEARING_RESULTS = python_net_import('SMT.MastaAPI.Bearings.BearingResults.Rolling', 'LoadedBallBearingResults')


__docformat__ = 'restructuredtext en'
__all__ = ('LoadedBallBearingResults',)


class LoadedBallBearingResults(_1643.LoadedRollingBearingResults):
    '''LoadedBallBearingResults

    This is a mastapy class.
    '''

    TYPE = _LOADED_BALL_BEARING_RESULTS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'LoadedBallBearingResults.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def track_truncation(self) -> '_1686.TrackTruncationSafetyFactorResults':
        '''TrackTruncationSafetyFactorResults: 'TrackTruncation' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1686.TrackTruncationSafetyFactorResults)(self.wrapped.TrackTruncation) if self.wrapped.TrackTruncation else None
