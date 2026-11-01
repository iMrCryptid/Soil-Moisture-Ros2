from glob import glob
import os

from setuptools import setup

package_name = 'soil_moisture'

setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Jeffrey Acquah',
    maintainer_email='acquah015@gmail.com',
    description='Simulated soil moisture sensor publisher and monitoring subscriber',
    license='MIT',
    entry_points={
        'console_scripts': [
            'moisture_publisher = soil_moisture.moisture_publisher:main',
            'moisture_monitor = soil_moisture.moisture_monitor:main',
        ],
    },
)
