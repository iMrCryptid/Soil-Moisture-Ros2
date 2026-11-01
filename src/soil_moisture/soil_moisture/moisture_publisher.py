"""Simulated capacitive soil moisture sensor.

Publishes SoilMoisture messages on /science/soil_moisture. The raw value mimics
a capacitive sensor read by a 12 bit ADC: it reads HIGH in dry soil and LOW in
wet soil. The node converts raw counts to a percentage using two calibration
points (raw value in open air, raw value in water), the same way the real
sensor would be calibrated.
"""

import random

import rclpy
from rclpy.node import Node

from soil_interfaces.msg import SoilMoisture


class MoisturePublisher(Node):

    def __init__(self):
        super().__init__('moisture_publisher')

        # Parameters can be changed at launch without editing code
        self.declare_parameter('sensor_id', 'probe_1')
        self.declare_parameter('publish_rate_hz', 2.0)
        self.declare_parameter('dry_raw', 2600)   # calibration: sensor in open air
        self.declare_parameter('wet_raw', 1100)   # calibration: sensor in water

        self.sensor_id = self.get_parameter('sensor_id').value
        rate = self.get_parameter('publish_rate_hz').value
        self.dry_raw = self.get_parameter('dry_raw').value
        self.wet_raw = self.get_parameter('wet_raw').value

        self.publisher_ = self.create_publisher(SoilMoisture, '/science/soil_moisture', 10)
        self.timer = self.create_timer(1.0 / rate, self.publish_reading)

        # Start somewhere in the middle and let the soil "drift"
        self.true_raw = random.uniform(1500, 2200)

        self.get_logger().info(
            f'Publishing {self.sensor_id} readings at {rate} Hz on /science/soil_moisture')

    def simulate_raw(self):
        # Slow random walk (the arm moving between sample spots / soil drying)
        self.true_raw += random.gauss(0, 25)
        # Occasionally jump, as if the probe was pushed into a new patch of soil
        if random.random() < 0.05:
            self.true_raw = random.uniform(self.wet_raw, self.dry_raw)
        self.true_raw = min(max(self.true_raw, self.wet_raw), self.dry_raw)
        # Small electrical noise on each reading
        noisy = self.true_raw + random.gauss(0, 8)
        return int(min(max(noisy, 0), 4095))

    def raw_to_percent(self, raw):
        percent = (self.dry_raw - raw) / (self.dry_raw - self.wet_raw) * 100.0
        return float(min(max(percent, 0.0), 100.0))

    def publish_reading(self):
        raw = self.simulate_raw()

        msg = SoilMoisture()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'soil_probe'
        msg.sensor_id = self.sensor_id
        msg.raw_adc = raw
        msg.moisture_percent = self.raw_to_percent(raw)

        self.publisher_.publish(msg)
        self.get_logger().info(
            f'[{msg.sensor_id}] raw={msg.raw_adc} moisture={msg.moisture_percent:.1f}%')


def main(args=None):
    rclpy.init(args=args)
    node = MoisturePublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
