'''_943.py

GearMeshDesignAnalysis
'''


from mastapy.gears.analysis import (
    _939, _940, _941, _942,
    _937
)
from mastapy._internal import constructor
from mastapy.gears.manufacturing.cylindrical import _390, _394, _395
from mastapy._internal.cast_exception import CastException
from mastapy.gears.manufacturing.bevel import (
    _552, _553, _554, _555,
    _565, _566, _571
)
from mastapy.gears.ltca import _608
from mastapy.gears.ltca.cylindrical import _622
from mastapy.gears.ltca.conical import _633
from mastapy.gears.load_case import _639
from mastapy.gears.load_case.worm import _642
from mastapy.gears.load_case.face import _645
from mastapy.gears.load_case.cylindrical import _648
from mastapy.gears.load_case.conical import _651
from mastapy.gears.load_case.concept import _654
from mastapy.gears.load_case.bevel import _657
from mastapy.gears.gear_twod_fe_analysis import _662
from mastapy.gears.gear_designs.face import _748
from mastapy.gears.gear_designs.cylindrical.micro_geometry import _836, _837
from mastapy.gears.fe_model import _921
from mastapy.gears.fe_model.cylindrical import _925
from mastapy.gears.fe_model.conical import _928
from mastapy._internal.python_net import python_net_import

_GEAR_MESH_DESIGN_ANALYSIS = python_net_import('SMT.MastaAPI.Gears.Analysis', 'GearMeshDesignAnalysis')


__docformat__ = 'restructuredtext en'
__all__ = ('GearMeshDesignAnalysis',)


class GearMeshDesignAnalysis(_937.AbstractGearMeshAnalysis):
    '''GearMeshDesignAnalysis

    This is a mastapy class.
    '''

    TYPE = _GEAR_MESH_DESIGN_ANALYSIS

    __hash__ = None

    def __init__(self, instance_to_wrap: 'GearMeshDesignAnalysis.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def gear_a(self) -> '_939.GearDesignAnalysis':
        '''GearDesignAnalysis: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_939.GearDesignAnalysis)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_cylindrical_gear_manufacturing_config(self) -> '_390.CylindricalGearManufacturingConfig':
        '''CylindricalGearManufacturingConfig: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _390.CylindricalGearManufacturingConfig.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to CylindricalGearManufacturingConfig. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_390.CylindricalGearManufacturingConfig)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_cylindrical_manufactured_gear_duty_cycle(self) -> '_394.CylindricalManufacturedGearDutyCycle':
        '''CylindricalManufacturedGearDutyCycle: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _394.CylindricalManufacturedGearDutyCycle.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to CylindricalManufacturedGearDutyCycle. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_394.CylindricalManufacturedGearDutyCycle)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_cylindrical_manufactured_gear_load_case(self) -> '_395.CylindricalManufacturedGearLoadCase':
        '''CylindricalManufacturedGearLoadCase: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _395.CylindricalManufacturedGearLoadCase.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to CylindricalManufacturedGearLoadCase. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_395.CylindricalManufacturedGearLoadCase)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_conical_gear_manufacturing_analysis(self) -> '_552.ConicalGearManufacturingAnalysis':
        '''ConicalGearManufacturingAnalysis: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _552.ConicalGearManufacturingAnalysis.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ConicalGearManufacturingAnalysis. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_552.ConicalGearManufacturingAnalysis)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_conical_gear_manufacturing_config(self) -> '_553.ConicalGearManufacturingConfig':
        '''ConicalGearManufacturingConfig: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _553.ConicalGearManufacturingConfig.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ConicalGearManufacturingConfig. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_553.ConicalGearManufacturingConfig)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_conical_gear_micro_geometry_config(self) -> '_554.ConicalGearMicroGeometryConfig':
        '''ConicalGearMicroGeometryConfig: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _554.ConicalGearMicroGeometryConfig.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ConicalGearMicroGeometryConfig. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_554.ConicalGearMicroGeometryConfig)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_conical_gear_micro_geometry_config_base(self) -> '_555.ConicalGearMicroGeometryConfigBase':
        '''ConicalGearMicroGeometryConfigBase: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _555.ConicalGearMicroGeometryConfigBase.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ConicalGearMicroGeometryConfigBase. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_555.ConicalGearMicroGeometryConfigBase)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_conical_pinion_manufacturing_config(self) -> '_565.ConicalPinionManufacturingConfig':
        '''ConicalPinionManufacturingConfig: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _565.ConicalPinionManufacturingConfig.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ConicalPinionManufacturingConfig. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_565.ConicalPinionManufacturingConfig)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_conical_pinion_micro_geometry_config(self) -> '_566.ConicalPinionMicroGeometryConfig':
        '''ConicalPinionMicroGeometryConfig: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _566.ConicalPinionMicroGeometryConfig.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ConicalPinionMicroGeometryConfig. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_566.ConicalPinionMicroGeometryConfig)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_conical_wheel_manufacturing_config(self) -> '_571.ConicalWheelManufacturingConfig':
        '''ConicalWheelManufacturingConfig: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _571.ConicalWheelManufacturingConfig.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ConicalWheelManufacturingConfig. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_571.ConicalWheelManufacturingConfig)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_gear_load_distribution_analysis(self) -> '_608.GearLoadDistributionAnalysis':
        '''GearLoadDistributionAnalysis: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _608.GearLoadDistributionAnalysis.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to GearLoadDistributionAnalysis. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_608.GearLoadDistributionAnalysis)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_cylindrical_gear_load_distribution_analysis(self) -> '_622.CylindricalGearLoadDistributionAnalysis':
        '''CylindricalGearLoadDistributionAnalysis: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _622.CylindricalGearLoadDistributionAnalysis.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to CylindricalGearLoadDistributionAnalysis. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_622.CylindricalGearLoadDistributionAnalysis)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_conical_gear_load_distribution_analysis(self) -> '_633.ConicalGearLoadDistributionAnalysis':
        '''ConicalGearLoadDistributionAnalysis: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _633.ConicalGearLoadDistributionAnalysis.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ConicalGearLoadDistributionAnalysis. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_633.ConicalGearLoadDistributionAnalysis)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_gear_load_case_base(self) -> '_639.GearLoadCaseBase':
        '''GearLoadCaseBase: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _639.GearLoadCaseBase.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to GearLoadCaseBase. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_639.GearLoadCaseBase)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_worm_gear_load_case(self) -> '_642.WormGearLoadCase':
        '''WormGearLoadCase: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _642.WormGearLoadCase.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to WormGearLoadCase. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_642.WormGearLoadCase)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_face_gear_load_case(self) -> '_645.FaceGearLoadCase':
        '''FaceGearLoadCase: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _645.FaceGearLoadCase.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to FaceGearLoadCase. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_645.FaceGearLoadCase)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_cylindrical_gear_load_case(self) -> '_648.CylindricalGearLoadCase':
        '''CylindricalGearLoadCase: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _648.CylindricalGearLoadCase.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to CylindricalGearLoadCase. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_648.CylindricalGearLoadCase)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_conical_gear_load_case(self) -> '_651.ConicalGearLoadCase':
        '''ConicalGearLoadCase: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _651.ConicalGearLoadCase.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ConicalGearLoadCase. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_651.ConicalGearLoadCase)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_concept_gear_load_case(self) -> '_654.ConceptGearLoadCase':
        '''ConceptGearLoadCase: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _654.ConceptGearLoadCase.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ConceptGearLoadCase. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_654.ConceptGearLoadCase)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_bevel_load_case(self) -> '_657.BevelLoadCase':
        '''BevelLoadCase: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _657.BevelLoadCase.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to BevelLoadCase. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_657.BevelLoadCase)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_cylindrical_gear_tiff_analysis(self) -> '_662.CylindricalGearTIFFAnalysis':
        '''CylindricalGearTIFFAnalysis: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _662.CylindricalGearTIFFAnalysis.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to CylindricalGearTIFFAnalysis. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_662.CylindricalGearTIFFAnalysis)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_face_gear_micro_geometry(self) -> '_748.FaceGearMicroGeometry':
        '''FaceGearMicroGeometry: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _748.FaceGearMicroGeometry.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to FaceGearMicroGeometry. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_748.FaceGearMicroGeometry)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_cylindrical_gear_micro_geometry(self) -> '_836.CylindricalGearMicroGeometry':
        '''CylindricalGearMicroGeometry: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _836.CylindricalGearMicroGeometry.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to CylindricalGearMicroGeometry. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_836.CylindricalGearMicroGeometry)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_cylindrical_gear_micro_geometry_duty_cycle(self) -> '_837.CylindricalGearMicroGeometryDutyCycle':
        '''CylindricalGearMicroGeometryDutyCycle: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _837.CylindricalGearMicroGeometryDutyCycle.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to CylindricalGearMicroGeometryDutyCycle. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_837.CylindricalGearMicroGeometryDutyCycle)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_gear_fe_model(self) -> '_921.GearFEModel':
        '''GearFEModel: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _921.GearFEModel.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to GearFEModel. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_921.GearFEModel)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_cylindrical_gear_fe_model(self) -> '_925.CylindricalGearFEModel':
        '''CylindricalGearFEModel: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _925.CylindricalGearFEModel.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to CylindricalGearFEModel. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_925.CylindricalGearFEModel)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_conical_gear_fe_model(self) -> '_928.ConicalGearFEModel':
        '''ConicalGearFEModel: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _928.ConicalGearFEModel.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to ConicalGearFEModel. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_928.ConicalGearFEModel)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_gear_implementation_analysis(self) -> '_940.GearImplementationAnalysis':
        '''GearImplementationAnalysis: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _940.GearImplementationAnalysis.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to GearImplementationAnalysis. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_940.GearImplementationAnalysis)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_gear_implementation_analysis_duty_cycle(self) -> '_941.GearImplementationAnalysisDutyCycle':
        '''GearImplementationAnalysisDutyCycle: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _941.GearImplementationAnalysisDutyCycle.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to GearImplementationAnalysisDutyCycle. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_941.GearImplementationAnalysisDutyCycle)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_a_of_type_gear_implementation_detail(self) -> '_942.GearImplementationDetail':
        '''GearImplementationDetail: 'GearA' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _942.GearImplementationDetail.TYPE not in self.wrapped.GearA.__class__.__mro__:
            raise CastException('Failed to cast gear_a to GearImplementationDetail. Expected: {}.'.format(self.wrapped.GearA.__class__.__qualname__))

        return constructor.new(_942.GearImplementationDetail)(self.wrapped.GearA) if self.wrapped.GearA else None

    @property
    def gear_b(self) -> '_939.GearDesignAnalysis':
        '''GearDesignAnalysis: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_939.GearDesignAnalysis)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_cylindrical_gear_manufacturing_config(self) -> '_390.CylindricalGearManufacturingConfig':
        '''CylindricalGearManufacturingConfig: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _390.CylindricalGearManufacturingConfig.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to CylindricalGearManufacturingConfig. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_390.CylindricalGearManufacturingConfig)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_cylindrical_manufactured_gear_duty_cycle(self) -> '_394.CylindricalManufacturedGearDutyCycle':
        '''CylindricalManufacturedGearDutyCycle: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _394.CylindricalManufacturedGearDutyCycle.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to CylindricalManufacturedGearDutyCycle. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_394.CylindricalManufacturedGearDutyCycle)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_cylindrical_manufactured_gear_load_case(self) -> '_395.CylindricalManufacturedGearLoadCase':
        '''CylindricalManufacturedGearLoadCase: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _395.CylindricalManufacturedGearLoadCase.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to CylindricalManufacturedGearLoadCase. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_395.CylindricalManufacturedGearLoadCase)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_conical_gear_manufacturing_analysis(self) -> '_552.ConicalGearManufacturingAnalysis':
        '''ConicalGearManufacturingAnalysis: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _552.ConicalGearManufacturingAnalysis.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ConicalGearManufacturingAnalysis. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_552.ConicalGearManufacturingAnalysis)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_conical_gear_manufacturing_config(self) -> '_553.ConicalGearManufacturingConfig':
        '''ConicalGearManufacturingConfig: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _553.ConicalGearManufacturingConfig.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ConicalGearManufacturingConfig. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_553.ConicalGearManufacturingConfig)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_conical_gear_micro_geometry_config(self) -> '_554.ConicalGearMicroGeometryConfig':
        '''ConicalGearMicroGeometryConfig: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _554.ConicalGearMicroGeometryConfig.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ConicalGearMicroGeometryConfig. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_554.ConicalGearMicroGeometryConfig)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_conical_gear_micro_geometry_config_base(self) -> '_555.ConicalGearMicroGeometryConfigBase':
        '''ConicalGearMicroGeometryConfigBase: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _555.ConicalGearMicroGeometryConfigBase.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ConicalGearMicroGeometryConfigBase. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_555.ConicalGearMicroGeometryConfigBase)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_conical_pinion_manufacturing_config(self) -> '_565.ConicalPinionManufacturingConfig':
        '''ConicalPinionManufacturingConfig: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _565.ConicalPinionManufacturingConfig.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ConicalPinionManufacturingConfig. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_565.ConicalPinionManufacturingConfig)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_conical_pinion_micro_geometry_config(self) -> '_566.ConicalPinionMicroGeometryConfig':
        '''ConicalPinionMicroGeometryConfig: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _566.ConicalPinionMicroGeometryConfig.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ConicalPinionMicroGeometryConfig. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_566.ConicalPinionMicroGeometryConfig)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_conical_wheel_manufacturing_config(self) -> '_571.ConicalWheelManufacturingConfig':
        '''ConicalWheelManufacturingConfig: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _571.ConicalWheelManufacturingConfig.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ConicalWheelManufacturingConfig. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_571.ConicalWheelManufacturingConfig)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_gear_load_distribution_analysis(self) -> '_608.GearLoadDistributionAnalysis':
        '''GearLoadDistributionAnalysis: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _608.GearLoadDistributionAnalysis.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to GearLoadDistributionAnalysis. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_608.GearLoadDistributionAnalysis)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_cylindrical_gear_load_distribution_analysis(self) -> '_622.CylindricalGearLoadDistributionAnalysis':
        '''CylindricalGearLoadDistributionAnalysis: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _622.CylindricalGearLoadDistributionAnalysis.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to CylindricalGearLoadDistributionAnalysis. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_622.CylindricalGearLoadDistributionAnalysis)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_conical_gear_load_distribution_analysis(self) -> '_633.ConicalGearLoadDistributionAnalysis':
        '''ConicalGearLoadDistributionAnalysis: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _633.ConicalGearLoadDistributionAnalysis.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ConicalGearLoadDistributionAnalysis. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_633.ConicalGearLoadDistributionAnalysis)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_gear_load_case_base(self) -> '_639.GearLoadCaseBase':
        '''GearLoadCaseBase: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _639.GearLoadCaseBase.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to GearLoadCaseBase. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_639.GearLoadCaseBase)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_worm_gear_load_case(self) -> '_642.WormGearLoadCase':
        '''WormGearLoadCase: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _642.WormGearLoadCase.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to WormGearLoadCase. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_642.WormGearLoadCase)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_face_gear_load_case(self) -> '_645.FaceGearLoadCase':
        '''FaceGearLoadCase: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _645.FaceGearLoadCase.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to FaceGearLoadCase. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_645.FaceGearLoadCase)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_cylindrical_gear_load_case(self) -> '_648.CylindricalGearLoadCase':
        '''CylindricalGearLoadCase: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _648.CylindricalGearLoadCase.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to CylindricalGearLoadCase. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_648.CylindricalGearLoadCase)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_conical_gear_load_case(self) -> '_651.ConicalGearLoadCase':
        '''ConicalGearLoadCase: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _651.ConicalGearLoadCase.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ConicalGearLoadCase. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_651.ConicalGearLoadCase)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_concept_gear_load_case(self) -> '_654.ConceptGearLoadCase':
        '''ConceptGearLoadCase: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _654.ConceptGearLoadCase.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ConceptGearLoadCase. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_654.ConceptGearLoadCase)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_bevel_load_case(self) -> '_657.BevelLoadCase':
        '''BevelLoadCase: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _657.BevelLoadCase.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to BevelLoadCase. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_657.BevelLoadCase)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_cylindrical_gear_tiff_analysis(self) -> '_662.CylindricalGearTIFFAnalysis':
        '''CylindricalGearTIFFAnalysis: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _662.CylindricalGearTIFFAnalysis.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to CylindricalGearTIFFAnalysis. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_662.CylindricalGearTIFFAnalysis)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_face_gear_micro_geometry(self) -> '_748.FaceGearMicroGeometry':
        '''FaceGearMicroGeometry: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _748.FaceGearMicroGeometry.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to FaceGearMicroGeometry. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_748.FaceGearMicroGeometry)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_cylindrical_gear_micro_geometry(self) -> '_836.CylindricalGearMicroGeometry':
        '''CylindricalGearMicroGeometry: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _836.CylindricalGearMicroGeometry.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to CylindricalGearMicroGeometry. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_836.CylindricalGearMicroGeometry)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_cylindrical_gear_micro_geometry_duty_cycle(self) -> '_837.CylindricalGearMicroGeometryDutyCycle':
        '''CylindricalGearMicroGeometryDutyCycle: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _837.CylindricalGearMicroGeometryDutyCycle.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to CylindricalGearMicroGeometryDutyCycle. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_837.CylindricalGearMicroGeometryDutyCycle)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_gear_fe_model(self) -> '_921.GearFEModel':
        '''GearFEModel: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _921.GearFEModel.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to GearFEModel. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_921.GearFEModel)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_cylindrical_gear_fe_model(self) -> '_925.CylindricalGearFEModel':
        '''CylindricalGearFEModel: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _925.CylindricalGearFEModel.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to CylindricalGearFEModel. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_925.CylindricalGearFEModel)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_conical_gear_fe_model(self) -> '_928.ConicalGearFEModel':
        '''ConicalGearFEModel: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _928.ConicalGearFEModel.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to ConicalGearFEModel. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_928.ConicalGearFEModel)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_gear_implementation_analysis(self) -> '_940.GearImplementationAnalysis':
        '''GearImplementationAnalysis: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _940.GearImplementationAnalysis.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to GearImplementationAnalysis. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_940.GearImplementationAnalysis)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_gear_implementation_analysis_duty_cycle(self) -> '_941.GearImplementationAnalysisDutyCycle':
        '''GearImplementationAnalysisDutyCycle: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _941.GearImplementationAnalysisDutyCycle.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to GearImplementationAnalysisDutyCycle. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_941.GearImplementationAnalysisDutyCycle)(self.wrapped.GearB) if self.wrapped.GearB else None

    @property
    def gear_b_of_type_gear_implementation_detail(self) -> '_942.GearImplementationDetail':
        '''GearImplementationDetail: 'GearB' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _942.GearImplementationDetail.TYPE not in self.wrapped.GearB.__class__.__mro__:
            raise CastException('Failed to cast gear_b to GearImplementationDetail. Expected: {}.'.format(self.wrapped.GearB.__class__.__qualname__))

        return constructor.new(_942.GearImplementationDetail)(self.wrapped.GearB) if self.wrapped.GearB else None
