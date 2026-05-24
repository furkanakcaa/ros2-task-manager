import rclpy
from rclpy.node import Node
from enum import Enum
import time

class RobotState(Enum):
    BEKLIYOR = 0
    GOREVE_GIDIYOR = 1
    GOREVDE_BEKLIYOR = 2
    GOREV_TAMAMLANDI = 3

class TaskManager(Node):
    def __init__(self):
        super().__init__('task_manager')

        self.state = RobotState.BEKLIYOR
        self.waypoints = ['A', 'B', 'C', 'HOME']
        self.current_index = 0

        self.timer = self.create_timer(1.0, self.state_machine)
        self.get_logger().info('Görev yöneticisi başladı.')

    def state_machine(self):
        if self.state == RobotState.BEKLIYOR:
            self.get_logger().info('Görev başlıyor...')
            self.state = RobotState.GOREVE_GIDIYOR

        elif self.state == RobotState.GOREVE_GIDIYOR:
            hedef = self.waypoints[self.current_index]
            self.get_logger().info(f'{hedef} noktasına gidiliyor..')
            time.sleep(2.0)
            self.state = RobotState.GOREVDE_BEKLIYOR

        elif self.state == RobotState.GOREVDE_BEKLIYOR:
            hedef = self.waypoints[self.current_index]
            self.get_logger().info(f'{hedef} noktasında 1 saniye bekleniyor...')
            time.sleep(1.0)
            self.current_index += 1
            if self.current_index >= len(self.waypoints):
                self.state = RobotState.GOREV_TAMAMLANDI
            else:
                self.state = RobotState.GOREVE_GIDIYOR

        elif self.state == RobotState.GOREV_TAMAMLANDI:
            self.get_logger().info('Tüm görevler tamamlandı! Robot HOME\'a döndü.')
            self.timer.cancel()

def main(args=None):
    rclpy.init(args=args)
    node = TaskManager()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()