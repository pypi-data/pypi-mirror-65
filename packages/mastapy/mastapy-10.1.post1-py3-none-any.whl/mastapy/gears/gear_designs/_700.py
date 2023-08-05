'''_700.py

DesignConstraintCollectionDatabase
'''


from typing import Iterable

from mastapy.gears.gear_designs import _701
from mastapy._internal import constructor, conversion
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_DESIGN_CONSTRAINT_COLLECTION_DATABASE = python_net_import('SMT.MastaAPI.Gears.GearDesigns', 'DesignConstraintCollectionDatabase')


__docformat__ = 'restructuredtext en'
__all__ = ('DesignConstraintCollectionDatabase',)


class DesignConstraintCollectionDatabase(_0.APIBase):
    '''DesignConstraintCollectionDatabase

    This is a mastapy class.
    '''

    TYPE = _DESIGN_CONSTRAINT_COLLECTION_DATABASE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'DesignConstraintCollectionDatabase.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def item(self) -> '_701.DesignConstraintsCollection':
        '''DesignConstraintsCollection: 'Item' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_701.DesignConstraintsCollection)(self.wrapped.Item) if self.wrapped.Item else None

    def create(self, name: 'str') -> '_701.DesignConstraintsCollection':
        ''' 'Create' is the original name of this method.

        Args:
            name (str)

        Returns:
            mastapy.gears.gear_designs.DesignConstraintsCollection
        '''

        name = str(name)
        method_result = self.wrapped.Create(name if name else None)
        return constructor.new(_701.DesignConstraintsCollection)(method_result) if method_result else None

    def can_be_removed(self, design_constraints_collection: '_701.DesignConstraintsCollection') -> 'bool':
        ''' 'CanBeRemoved' is the original name of this method.

        Args:
            design_constraints_collection (mastapy.gears.gear_designs.DesignConstraintsCollection)

        Returns:
            bool
        '''

        method_result = self.wrapped.CanBeRemoved(design_constraints_collection.wrapped if design_constraints_collection else None)
        return method_result

    def rename(self, design_constraints_collection: '_701.DesignConstraintsCollection', new_name: 'str') -> 'bool':
        ''' 'Rename' is the original name of this method.

        Args:
            design_constraints_collection (mastapy.gears.gear_designs.DesignConstraintsCollection)
            new_name (str)

        Returns:
            bool
        '''

        new_name = str(new_name)
        method_result = self.wrapped.Rename(design_constraints_collection.wrapped if design_constraints_collection else None, new_name if new_name else None)
        return method_result

    def remove(self, design_constraints_collection: '_701.DesignConstraintsCollection'):
        ''' 'Remove' is the original name of this method.

        Args:
            design_constraints_collection (mastapy.gears.gear_designs.DesignConstraintsCollection)
        '''

        self.wrapped.Remove(design_constraints_collection.wrapped if design_constraints_collection else None)

    def get_all_items(self) -> 'Iterable[_701.DesignConstraintsCollection]':
        ''' 'GetAllItems' is the original name of this method.

        Returns:
            Iterable[mastapy.gears.gear_designs.DesignConstraintsCollection]
        '''

        return conversion.pn_to_mp_objects_in_iterable(self.wrapped.GetAllItems(), constructor.new(_701.DesignConstraintsCollection))

    def save_changes(self, design_constraints_collection: '_701.DesignConstraintsCollection'):
        ''' 'SaveChanges' is the original name of this method.

        Args:
            design_constraints_collection (mastapy.gears.gear_designs.DesignConstraintsCollection)
        '''

        self.wrapped.SaveChanges(design_constraints_collection.wrapped if design_constraints_collection else None)
