'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._2093 import BoostPressureInputOptions
    from ._2094 import InputPowerInputOptions
    from ._2095 import PressureRatioInputOptions
    from ._2096 import RotorSetDataInputFileOptions
    from ._2097 import RotorSetMeasuredPoint
    from ._2098 import RotorSpeedInputOptions
    from ._2099 import SuperchargerMap
    from ._2100 import SuperchargerMaps
    from ._2101 import SuperchargerRotorSet
    from ._2102 import SuperchargerRotorSetDatabase
    from ._2103 import YVariableForImportedData
