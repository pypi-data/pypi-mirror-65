'''_708.py

DesignConstraintCollectionDatabase
'''


from mastapy.utility.databases import _1339
from mastapy.gears.gear_designs import _709
from mastapy._internal.python_net import python_net_import

_DESIGN_CONSTRAINT_COLLECTION_DATABASE = python_net_import('SMT.MastaAPI.Gears.GearDesigns', 'DesignConstraintCollectionDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('DesignConstraintCollectionDatabase',)


class DesignConstraintCollectionDatabase(_1339.NamedDatabase['_709.DesignConstraintsCollection']):
    '''DesignConstraintCollectionDatabase

    This is a mastapy class.
    '''

    TYPE = _DESIGN_CONSTRAINT_COLLECTION_DATABASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DesignConstraintCollectionDatabase.TYPE'):
        super().__init__(instance_to_wrap)
