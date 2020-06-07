import struct
from collections import namedtuple
from icm20948 import ICM20948

# Number from ICM datasheet.
ICM20948_TEMP_OUT_H = 0x39
ICM20948_TEMP_OUT_L = 0x3A

ICM20948_TEMPERATURE_DEGREES_OFFSET = 21
ICM20948_TEMPERATURE_SENSITIVITY = 333.87
ICM20948_ROOM_TEMP_OFFSET = 21

Vector3 = namedtuple('Vector3', ['x', 'y', 'z'])


# https://robotics.stackexchange.com/questions/6953/how-to-calculate-euler-angles-from-gyroscope-output
class RobotImu:
    """Define a common interface to an inertial measurement unit with temperature"""
    def __init__(self):
        self._imu = ICM20948()

    def read_temperature(self):
        """Read a temperature in degrees C."""
        # PWR_MGMT_1 defaults to leave temperature enabled
        self._imu.bank(0)
        temp_raw_bytes = self._imu.read_bytes(ICM20948_TEMP_OUT_H, 2)
        temp_raw = struct.unpack('>h', bytearray(temp_raw_bytes))[0]
        temperature_deg_c = ((temp_raw - ICM20948_ROOM_TEMP_OFFSET) / ICM20948_TEMPERATURE_SENSITIVITY) + ICM20948_TEMPERATURE_DEGREES_OFFSET
        return temperature_deg_c

    def read_accelerometer(self):
        """Return prescaled accelerometer data"""
        accel_x, accel_y, accel_z, _, _, _ = self._imu.read_accelerometer_gyro_data()
        return Vector3(accel_x, accel_y, accel_z)

    def read_gyro(self):
        """Return prescaled gyro data"""
        _, _, _, gyro_x, gyro_y, gyro_z = self._imu.read_accelerometer_gyro_data()
        return Vector3(gyro_x, gyro_y, gyro_z)
