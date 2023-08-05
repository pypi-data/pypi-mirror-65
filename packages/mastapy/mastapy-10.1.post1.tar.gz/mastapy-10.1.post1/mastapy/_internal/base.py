'''base.py

This is a collection of empty base classes that get inserted by
_DummyBaseClassImporter to prevent errors when modifying __bases__.
'''


from typing import Generic, TypeVar


T = TypeVar('T')
T2 = TypeVar('T2')


class Base:
    '''Base

    Base class used by the dummy base class importer.
    '''


class GenericBase(Base, Generic[T]):
    '''GenericBase

    Generic Base class used by the dummy base class importer.
    '''


class GenericBase2(Base, Generic[T, T2]):
    '''GenericBase2

    Generic Base class with 2 generic parameters used by the
    dummy base class importer.
    '''
