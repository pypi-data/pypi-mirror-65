'''__init__.py'''


from mastapy._internal.dummy_base_class_importer import _DummyBaseClassImport


with _DummyBaseClassImport():
    from ._1893 import ClutchConnection
    from ._1894 import ClutchSocket
    from ._1895 import ConceptCouplingConnection
    from ._1896 import ConceptCouplingSocket
    from ._1897 import CouplingConnection
    from ._1898 import CouplingSocket
    from ._1899 import PartToPartShearCouplingConnection
    from ._1900 import PartToPartShearCouplingSocket
    from ._1901 import SpringDamperConnection
    from ._1902 import SpringDamperSocket
    from ._1903 import TorqueConverterConnection
    from ._1904 import TorqueConverterPumpSocket
    from ._1905 import TorqueConverterTurbineSocket
