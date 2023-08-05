'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._6501 import MeasurementType
    from ._6502 import MeasurementTypeExtensions
