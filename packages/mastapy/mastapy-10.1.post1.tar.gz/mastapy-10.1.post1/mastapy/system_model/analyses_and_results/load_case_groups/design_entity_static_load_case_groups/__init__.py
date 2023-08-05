'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._5245 import AbstractAssemblyStaticLoadCaseGroup
    from ._5246 import ComponentStaticLoadCaseGroup
    from ._5247 import ConnectionStaticLoadCaseGroup
    from ._5248 import DesignEntityStaticLoadCaseGroup
    from ._5249 import GearSetStaticLoadCaseGroup
    from ._5250 import PartStaticLoadCaseGroup
