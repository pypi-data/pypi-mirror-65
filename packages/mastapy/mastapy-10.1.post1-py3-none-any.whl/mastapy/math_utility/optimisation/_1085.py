'''_1085.py

OptimizationVariable
'''


from typing import List

from mastapy.utility.units_and_measurements import _1136
from mastapy._internal import constructor, conversion
from mastapy.utility.units_and_measurements.measurements import (
    _1143, _1144, _1145, _1146,
    _1147, _1148, _1149, _1150,
    _1151, _1152, _1153, _1154,
    _1155, _1156, _1157, _1158,
    _1159, _1160, _1161, _1162,
    _1163, _1164, _1165, _1166,
    _1167, _1168, _1169, _1170,
    _1171, _1172, _1173, _1174,
    _1175, _1176, _1177, _1178,
    _1179, _1180, _1181, _1182,
    _1183, _1184, _1185, _1186,
    _1187, _1188, _1189, _1190,
    _1191, _1192, _1193, _1194,
    _1195, _1196, _1197, _1198,
    _1199, _1200, _1201, _1202,
    _1203, _1204, _1205, _1206,
    _1207, _1208, _1209, _1210,
    _1211, _1212, _1213, _1214,
    _1215, _1216, _1217, _1218,
    _1219, _1220, _1221, _1222,
    _1223, _1224, _1225, _1226,
    _1227, _1228, _1229, _1230,
    _1231, _1232, _1233, _1234,
    _1235, _1236, _1237, _1238,
    _1239, _1240, _1241, _1242,
    _1243, _1244, _1245, _1246,
    _1247, _1248, _1249
)
from mastapy._internal.cast_exception import CastException
from mastapy import _0
from mastapy._internal.python_net import python_net_import

_OPTIMIZATION_VARIABLE = python_net_import('SMT.MastaAPI.MathUtility.Optimisation', 'OptimizationVariable')


__docformat__ = 'restructuredtext en'
__all__ = ('OptimizationVariable',)


class OptimizationVariable(_0.APIBase):
    '''OptimizationVariable

    This is a mastapy class.
    '''

    TYPE = _OPTIMIZATION_VARIABLE

    __hash__ = None

    def __init__(self, instance_to_wrap: 'OptimizationVariable.TYPE'):
        super().__init__(instance_to_wrap)

    @property
    def measurement(self) -> '_1136.MeasurementBase':
        '''MeasurementBase: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        return constructor.new(_1136.MeasurementBase)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_acceleration(self) -> '_1143.Acceleration':
        '''Acceleration: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1143.Acceleration.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Acceleration. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1143.Acceleration)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_angle(self) -> '_1144.Angle':
        '''Angle: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1144.Angle.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Angle. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1144.Angle)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_angle_per_unit_temperature(self) -> '_1145.AnglePerUnitTemperature':
        '''AnglePerUnitTemperature: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1145.AnglePerUnitTemperature.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to AnglePerUnitTemperature. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1145.AnglePerUnitTemperature)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_angle_small(self) -> '_1146.AngleSmall':
        '''AngleSmall: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1146.AngleSmall.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to AngleSmall. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1146.AngleSmall)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_angle_very_small(self) -> '_1147.AngleVerySmall':
        '''AngleVerySmall: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1147.AngleVerySmall.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to AngleVerySmall. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1147.AngleVerySmall)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_angular_acceleration(self) -> '_1148.AngularAcceleration':
        '''AngularAcceleration: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1148.AngularAcceleration.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to AngularAcceleration. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1148.AngularAcceleration)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_angular_compliance(self) -> '_1149.AngularCompliance':
        '''AngularCompliance: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1149.AngularCompliance.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to AngularCompliance. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1149.AngularCompliance)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_angular_jerk(self) -> '_1150.AngularJerk':
        '''AngularJerk: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1150.AngularJerk.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to AngularJerk. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1150.AngularJerk)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_angular_stiffness(self) -> '_1151.AngularStiffness':
        '''AngularStiffness: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1151.AngularStiffness.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to AngularStiffness. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1151.AngularStiffness)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_angular_velocity(self) -> '_1152.AngularVelocity':
        '''AngularVelocity: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1152.AngularVelocity.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to AngularVelocity. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1152.AngularVelocity)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_area(self) -> '_1153.Area':
        '''Area: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1153.Area.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Area. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1153.Area)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_area_small(self) -> '_1154.AreaSmall':
        '''AreaSmall: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1154.AreaSmall.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to AreaSmall. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1154.AreaSmall)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_cycles(self) -> '_1155.Cycles':
        '''Cycles: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1155.Cycles.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Cycles. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1155.Cycles)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_damage(self) -> '_1156.Damage':
        '''Damage: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1156.Damage.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Damage. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1156.Damage)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_damage_rate(self) -> '_1157.DamageRate':
        '''DamageRate: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1157.DamageRate.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to DamageRate. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1157.DamageRate)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_decibel(self) -> '_1158.Decibel':
        '''Decibel: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1158.Decibel.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Decibel. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1158.Decibel)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_density(self) -> '_1159.Density':
        '''Density: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1159.Density.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Density. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1159.Density)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_energy(self) -> '_1160.Energy':
        '''Energy: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1160.Energy.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Energy. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1160.Energy)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_energy_per_unit_area(self) -> '_1161.EnergyPerUnitArea':
        '''EnergyPerUnitArea: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1161.EnergyPerUnitArea.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to EnergyPerUnitArea. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1161.EnergyPerUnitArea)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_energy_per_unit_area_small(self) -> '_1162.EnergyPerUnitAreaSmall':
        '''EnergyPerUnitAreaSmall: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1162.EnergyPerUnitAreaSmall.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to EnergyPerUnitAreaSmall. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1162.EnergyPerUnitAreaSmall)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_energy_small(self) -> '_1163.EnergySmall':
        '''EnergySmall: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1163.EnergySmall.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to EnergySmall. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1163.EnergySmall)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_enum(self) -> '_1164.Enum':
        '''Enum: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1164.Enum.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Enum. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1164.Enum)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_flow_rate(self) -> '_1165.FlowRate':
        '''FlowRate: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1165.FlowRate.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to FlowRate. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1165.FlowRate)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_force(self) -> '_1166.Force':
        '''Force: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1166.Force.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Force. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1166.Force)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_force_per_unit_length(self) -> '_1167.ForcePerUnitLength':
        '''ForcePerUnitLength: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1167.ForcePerUnitLength.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to ForcePerUnitLength. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1167.ForcePerUnitLength)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_force_per_unit_pressure(self) -> '_1168.ForcePerUnitPressure':
        '''ForcePerUnitPressure: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1168.ForcePerUnitPressure.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to ForcePerUnitPressure. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1168.ForcePerUnitPressure)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_force_per_unit_temperature(self) -> '_1169.ForcePerUnitTemperature':
        '''ForcePerUnitTemperature: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1169.ForcePerUnitTemperature.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to ForcePerUnitTemperature. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1169.ForcePerUnitTemperature)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_fraction_measurement_base(self) -> '_1170.FractionMeasurementBase':
        '''FractionMeasurementBase: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1170.FractionMeasurementBase.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to FractionMeasurementBase. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1170.FractionMeasurementBase)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_frequency(self) -> '_1171.Frequency':
        '''Frequency: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1171.Frequency.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Frequency. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1171.Frequency)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_fuel_consumption_engine(self) -> '_1172.FuelConsumptionEngine':
        '''FuelConsumptionEngine: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1172.FuelConsumptionEngine.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to FuelConsumptionEngine. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1172.FuelConsumptionEngine)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_fuel_efficiency_vehicle(self) -> '_1173.FuelEfficiencyVehicle':
        '''FuelEfficiencyVehicle: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1173.FuelEfficiencyVehicle.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to FuelEfficiencyVehicle. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1173.FuelEfficiencyVehicle)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_gradient(self) -> '_1174.Gradient':
        '''Gradient: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1174.Gradient.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Gradient. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1174.Gradient)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_heat_conductivity(self) -> '_1175.HeatConductivity':
        '''HeatConductivity: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1175.HeatConductivity.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to HeatConductivity. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1175.HeatConductivity)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_heat_transfer(self) -> '_1176.HeatTransfer':
        '''HeatTransfer: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1176.HeatTransfer.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to HeatTransfer. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1176.HeatTransfer)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_heat_transfer_coefficient_for_plastic_gear_tooth(self) -> '_1177.HeatTransferCoefficientForPlasticGearTooth':
        '''HeatTransferCoefficientForPlasticGearTooth: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1177.HeatTransferCoefficientForPlasticGearTooth.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to HeatTransferCoefficientForPlasticGearTooth. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1177.HeatTransferCoefficientForPlasticGearTooth)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_heat_transfer_resistance(self) -> '_1178.HeatTransferResistance':
        '''HeatTransferResistance: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1178.HeatTransferResistance.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to HeatTransferResistance. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1178.HeatTransferResistance)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_impulse(self) -> '_1179.Impulse':
        '''Impulse: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1179.Impulse.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Impulse. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1179.Impulse)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_index(self) -> '_1180.Index':
        '''Index: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1180.Index.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Index. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1180.Index)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_integer(self) -> '_1181.Integer':
        '''Integer: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1181.Integer.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Integer. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1181.Integer)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_inverse_short_length(self) -> '_1182.InverseShortLength':
        '''InverseShortLength: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1182.InverseShortLength.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to InverseShortLength. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1182.InverseShortLength)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_inverse_short_time(self) -> '_1183.InverseShortTime':
        '''InverseShortTime: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1183.InverseShortTime.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to InverseShortTime. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1183.InverseShortTime)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_jerk(self) -> '_1184.Jerk':
        '''Jerk: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1184.Jerk.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Jerk. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1184.Jerk)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_kinematic_viscosity(self) -> '_1185.KinematicViscosity':
        '''KinematicViscosity: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1185.KinematicViscosity.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to KinematicViscosity. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1185.KinematicViscosity)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_length_long(self) -> '_1186.LengthLong':
        '''LengthLong: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1186.LengthLong.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to LengthLong. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1186.LengthLong)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_length_medium(self) -> '_1187.LengthMedium':
        '''LengthMedium: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1187.LengthMedium.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to LengthMedium. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1187.LengthMedium)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_length_per_unit_temperature(self) -> '_1188.LengthPerUnitTemperature':
        '''LengthPerUnitTemperature: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1188.LengthPerUnitTemperature.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to LengthPerUnitTemperature. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1188.LengthPerUnitTemperature)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_length_short(self) -> '_1189.LengthShort':
        '''LengthShort: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1189.LengthShort.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to LengthShort. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1189.LengthShort)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_length_to_the_fourth(self) -> '_1190.LengthToTheFourth':
        '''LengthToTheFourth: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1190.LengthToTheFourth.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to LengthToTheFourth. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1190.LengthToTheFourth)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_length_very_long(self) -> '_1191.LengthVeryLong':
        '''LengthVeryLong: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1191.LengthVeryLong.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to LengthVeryLong. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1191.LengthVeryLong)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_length_very_short(self) -> '_1192.LengthVeryShort':
        '''LengthVeryShort: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1192.LengthVeryShort.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to LengthVeryShort. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1192.LengthVeryShort)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_length_very_short_per_length_short(self) -> '_1193.LengthVeryShortPerLengthShort':
        '''LengthVeryShortPerLengthShort: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1193.LengthVeryShortPerLengthShort.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to LengthVeryShortPerLengthShort. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1193.LengthVeryShortPerLengthShort)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_linear_angular_damping(self) -> '_1194.LinearAngularDamping':
        '''LinearAngularDamping: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1194.LinearAngularDamping.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to LinearAngularDamping. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1194.LinearAngularDamping)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_linear_angular_stiffness_cross_term(self) -> '_1195.LinearAngularStiffnessCrossTerm':
        '''LinearAngularStiffnessCrossTerm: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1195.LinearAngularStiffnessCrossTerm.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to LinearAngularStiffnessCrossTerm. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1195.LinearAngularStiffnessCrossTerm)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_linear_damping(self) -> '_1196.LinearDamping':
        '''LinearDamping: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1196.LinearDamping.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to LinearDamping. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1196.LinearDamping)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_linear_flexibility(self) -> '_1197.LinearFlexibility':
        '''LinearFlexibility: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1197.LinearFlexibility.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to LinearFlexibility. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1197.LinearFlexibility)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_linear_stiffness(self) -> '_1198.LinearStiffness':
        '''LinearStiffness: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1198.LinearStiffness.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to LinearStiffness. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1198.LinearStiffness)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_mass(self) -> '_1199.Mass':
        '''Mass: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1199.Mass.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Mass. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1199.Mass)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_mass_per_unit_length(self) -> '_1200.MassPerUnitLength':
        '''MassPerUnitLength: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1200.MassPerUnitLength.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to MassPerUnitLength. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1200.MassPerUnitLength)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_mass_per_unit_time(self) -> '_1201.MassPerUnitTime':
        '''MassPerUnitTime: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1201.MassPerUnitTime.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to MassPerUnitTime. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1201.MassPerUnitTime)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_moment_of_inertia(self) -> '_1202.MomentOfInertia':
        '''MomentOfInertia: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1202.MomentOfInertia.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to MomentOfInertia. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1202.MomentOfInertia)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_moment_of_inertia_per_unit_length(self) -> '_1203.MomentOfInertiaPerUnitLength':
        '''MomentOfInertiaPerUnitLength: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1203.MomentOfInertiaPerUnitLength.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to MomentOfInertiaPerUnitLength. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1203.MomentOfInertiaPerUnitLength)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_moment_per_unit_pressure(self) -> '_1204.MomentPerUnitPressure':
        '''MomentPerUnitPressure: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1204.MomentPerUnitPressure.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to MomentPerUnitPressure. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1204.MomentPerUnitPressure)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_number(self) -> '_1205.Number':
        '''Number: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1205.Number.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Number. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1205.Number)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_percentage(self) -> '_1206.Percentage':
        '''Percentage: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1206.Percentage.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Percentage. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1206.Percentage)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_power(self) -> '_1207.Power':
        '''Power: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1207.Power.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Power. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1207.Power)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_power_per_small_area(self) -> '_1208.PowerPerSmallArea':
        '''PowerPerSmallArea: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1208.PowerPerSmallArea.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to PowerPerSmallArea. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1208.PowerPerSmallArea)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_power_per_unit_time(self) -> '_1209.PowerPerUnitTime':
        '''PowerPerUnitTime: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1209.PowerPerUnitTime.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to PowerPerUnitTime. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1209.PowerPerUnitTime)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_power_small(self) -> '_1210.PowerSmall':
        '''PowerSmall: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1210.PowerSmall.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to PowerSmall. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1210.PowerSmall)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_power_small_per_area(self) -> '_1211.PowerSmallPerArea':
        '''PowerSmallPerArea: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1211.PowerSmallPerArea.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to PowerSmallPerArea. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1211.PowerSmallPerArea)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_power_small_per_unit_area_per_unit_time(self) -> '_1212.PowerSmallPerUnitAreaPerUnitTime':
        '''PowerSmallPerUnitAreaPerUnitTime: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1212.PowerSmallPerUnitAreaPerUnitTime.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to PowerSmallPerUnitAreaPerUnitTime. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1212.PowerSmallPerUnitAreaPerUnitTime)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_power_small_per_unit_time(self) -> '_1213.PowerSmallPerUnitTime':
        '''PowerSmallPerUnitTime: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1213.PowerSmallPerUnitTime.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to PowerSmallPerUnitTime. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1213.PowerSmallPerUnitTime)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_pressure(self) -> '_1214.Pressure':
        '''Pressure: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1214.Pressure.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Pressure. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1214.Pressure)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_pressure_per_unit_time(self) -> '_1215.PressurePerUnitTime':
        '''PressurePerUnitTime: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1215.PressurePerUnitTime.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to PressurePerUnitTime. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1215.PressurePerUnitTime)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_pressure_velocity_product(self) -> '_1216.PressureVelocityProduct':
        '''PressureVelocityProduct: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1216.PressureVelocityProduct.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to PressureVelocityProduct. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1216.PressureVelocityProduct)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_pressure_viscosity_coefficient(self) -> '_1217.PressureViscosityCoefficient':
        '''PressureViscosityCoefficient: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1217.PressureViscosityCoefficient.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to PressureViscosityCoefficient. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1217.PressureViscosityCoefficient)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_price(self) -> '_1218.Price':
        '''Price: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1218.Price.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Price. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1218.Price)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_quadratic_angular_damping(self) -> '_1219.QuadraticAngularDamping':
        '''QuadraticAngularDamping: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1219.QuadraticAngularDamping.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to QuadraticAngularDamping. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1219.QuadraticAngularDamping)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_quadratic_drag(self) -> '_1220.QuadraticDrag':
        '''QuadraticDrag: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1220.QuadraticDrag.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to QuadraticDrag. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1220.QuadraticDrag)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_rescaled_measurement(self) -> '_1221.RescaledMeasurement':
        '''RescaledMeasurement: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1221.RescaledMeasurement.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to RescaledMeasurement. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1221.RescaledMeasurement)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_rotatum(self) -> '_1222.Rotatum':
        '''Rotatum: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1222.Rotatum.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Rotatum. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1222.Rotatum)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_safety_factor(self) -> '_1223.SafetyFactor':
        '''SafetyFactor: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1223.SafetyFactor.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to SafetyFactor. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1223.SafetyFactor)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_specific_acoustic_impedance(self) -> '_1224.SpecificAcousticImpedance':
        '''SpecificAcousticImpedance: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1224.SpecificAcousticImpedance.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to SpecificAcousticImpedance. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1224.SpecificAcousticImpedance)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_specific_heat(self) -> '_1225.SpecificHeat':
        '''SpecificHeat: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1225.SpecificHeat.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to SpecificHeat. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1225.SpecificHeat)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_square_root_of_unit_force_per_unit_area(self) -> '_1226.SquareRootOfUnitForcePerUnitArea':
        '''SquareRootOfUnitForcePerUnitArea: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1226.SquareRootOfUnitForcePerUnitArea.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to SquareRootOfUnitForcePerUnitArea. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1226.SquareRootOfUnitForcePerUnitArea)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_stiffness_per_unit_face_width(self) -> '_1227.StiffnessPerUnitFaceWidth':
        '''StiffnessPerUnitFaceWidth: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1227.StiffnessPerUnitFaceWidth.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to StiffnessPerUnitFaceWidth. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1227.StiffnessPerUnitFaceWidth)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_stress(self) -> '_1228.Stress':
        '''Stress: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1228.Stress.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Stress. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1228.Stress)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_temperature(self) -> '_1229.Temperature':
        '''Temperature: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1229.Temperature.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Temperature. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1229.Temperature)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_temperature_difference(self) -> '_1230.TemperatureDifference':
        '''TemperatureDifference: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1230.TemperatureDifference.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to TemperatureDifference. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1230.TemperatureDifference)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_temperature_per_unit_time(self) -> '_1231.TemperaturePerUnitTime':
        '''TemperaturePerUnitTime: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1231.TemperaturePerUnitTime.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to TemperaturePerUnitTime. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1231.TemperaturePerUnitTime)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_text(self) -> '_1232.Text':
        '''Text: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1232.Text.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Text. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1232.Text)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_thermal_contact_coefficient(self) -> '_1233.ThermalContactCoefficient':
        '''ThermalContactCoefficient: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1233.ThermalContactCoefficient.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to ThermalContactCoefficient. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1233.ThermalContactCoefficient)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_thermal_expansion_coefficient(self) -> '_1234.ThermalExpansionCoefficient':
        '''ThermalExpansionCoefficient: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1234.ThermalExpansionCoefficient.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to ThermalExpansionCoefficient. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1234.ThermalExpansionCoefficient)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_thermo_elastic_factor(self) -> '_1235.ThermoElasticFactor':
        '''ThermoElasticFactor: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1235.ThermoElasticFactor.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to ThermoElasticFactor. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1235.ThermoElasticFactor)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_time(self) -> '_1236.Time':
        '''Time: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1236.Time.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Time. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1236.Time)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_time_short(self) -> '_1237.TimeShort':
        '''TimeShort: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1237.TimeShort.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to TimeShort. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1237.TimeShort)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_time_very_short(self) -> '_1238.TimeVeryShort':
        '''TimeVeryShort: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1238.TimeVeryShort.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to TimeVeryShort. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1238.TimeVeryShort)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_torque(self) -> '_1239.Torque':
        '''Torque: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1239.Torque.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Torque. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1239.Torque)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_torque_converter_inverse_k(self) -> '_1240.TorqueConverterInverseK':
        '''TorqueConverterInverseK: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1240.TorqueConverterInverseK.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to TorqueConverterInverseK. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1240.TorqueConverterInverseK)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_torque_converter_k(self) -> '_1241.TorqueConverterK':
        '''TorqueConverterK: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1241.TorqueConverterK.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to TorqueConverterK. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1241.TorqueConverterK)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_torque_per_unit_temperature(self) -> '_1242.TorquePerUnitTemperature':
        '''TorquePerUnitTemperature: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1242.TorquePerUnitTemperature.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to TorquePerUnitTemperature. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1242.TorquePerUnitTemperature)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_velocity(self) -> '_1243.Velocity':
        '''Velocity: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1243.Velocity.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Velocity. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1243.Velocity)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_velocity_small(self) -> '_1244.VelocitySmall':
        '''VelocitySmall: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1244.VelocitySmall.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to VelocitySmall. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1244.VelocitySmall)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_viscosity(self) -> '_1245.Viscosity':
        '''Viscosity: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1245.Viscosity.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Viscosity. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1245.Viscosity)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_voltage(self) -> '_1246.Voltage':
        '''Voltage: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1246.Voltage.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Voltage. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1246.Voltage)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_volume(self) -> '_1247.Volume':
        '''Volume: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1247.Volume.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Volume. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1247.Volume)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_wear_coefficient(self) -> '_1248.WearCoefficient':
        '''WearCoefficient: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1248.WearCoefficient.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to WearCoefficient. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1248.WearCoefficient)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def measurement_of_type_yank(self) -> '_1249.Yank':
        '''Yank: 'Measurement' is the original name of this property.

        Note:
            This property is readonly.
        '''

        if _1249.Yank.TYPE not in self.wrapped.Measurement.__class__.__mro__:
            raise CastException('Failed to cast measurement to Yank. Expected: {}.'.format(self.wrapped.Measurement.__class__.__qualname__))

        return constructor.new(_1249.Yank)(self.wrapped.Measurement) if self.wrapped.Measurement else None

    @property
    def results(self) -> 'List[float]':
        '''List[float]: 'Results' is the original name of this property.

        Note:
            This property is readonly.
        '''

        value = conversion.pn_to_mp_objects_in_list(self.wrapped.Results, float)
        return value
