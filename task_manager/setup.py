from setuptools import find_packages, setup

package_name = 'task_manager'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', ['launch/task_mission.launch.py']),
        ('share/' + package_name + '/maps', [
            'maps/map.pgm',
            'maps/map.yaml'
        ])
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='furkanakcatepe',
    maintainer_email='akcatepefurkan1@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'task_manager_node = task_manager.task_manager_node:main'
        ],
    },
)
