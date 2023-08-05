'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._205 import SpiralBevelGearMeshRating
    from ._206 import SpiralBevelGearRating
    from ._207 import SpiralBevelGearSetRating
