"""Subscriber that receives soil moisture readings and classifies them.

Listens on /science/soil_moisture, logs every reading, labels it as
DRY / OK / SATURATED using configurable thresholds, and keeps a running
average so the science team gets a steadier number than a single noisy sample.
"""

from collections import deque

import rclpy
from rclpy.node import Node

from soil_interfaces.msg import SoilMoisture


class MoistureMonitor(Node):

    def __init__(self):
        super().__init__('moisture_monitor')

        self.declare_parameter('dry_threshold', 20.0)
        self.declare_parameter('saturated_threshold', 80.0)
        self.declare_parameter('average_window', 10)

        self.dry_threshold = self.get_parameter('dry_threshold').value
        self.saturated_threshold = self.get_parameter('saturated_threshold').value
        window = self.get_parameter('average_window').value
        self.recent = deque(maxlen=window)

        self.subscription = self.create_subscription(
            SoilMoisture, '/science/soil_moisture', self.on_reading, 10)

        self.get_logger().info('Listening on /science/soil_moisture')

    def classify(self, percent):
        if percent < self.dry_threshold:
            return 'DRY'
        if percent > self.saturated_threshold:
            return 'SATURATED'
        return 'OK'

    def on_reading(self, msg):
        self.recent.append(msg.moisture_percent)
        avg = sum(self.recent) / len(self.recent)
        status = self.classify(msg.moisture_percent)

        text = (f'[{msg.sensor_id}] {msg.moisture_percent:.1f}% ({status}) '
                f'raw={msg.raw_adc} avg_last_{len(self.recent)}={avg:.1f}%')

        if status == 'OK':
            self.get_logger().info(text)
        else:
            self.get_logger().warn(text)


def main(args=None):
    rclpy.init(args=args)
    node = MoistureMonitor()
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
