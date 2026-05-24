import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped, PoseWithCovarianceStamped
from std_msgs.msg import String
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

        self.action_client = ActionClient(self, NavigateToPose, 'navigate_to_pose')

        self.initial_pose_publisher = self.create_publisher(
            PoseWithCovarianceStamped, 
            'initialpose', 
            10
        )
        self.create_timer(2.0, self.publish_initial_pose)
        self.initial_pose_sent = False

        self.state_publisher = self.create_publisher(String, 'robot_state', 10)
        
        self.state = RobotState.BEKLIYOR
        self.current_index = 0
        self.navigating = False

        self.waypoints = [
            ('Home', 1.99, -0.71),
            ('A', 0.11, -2.57),
            ('B', -0.51, -0.73),
            ('C', -1.73, 0.14),
            ('Home', 1.99, -0.71)
        ]

        self.timer = self.create_timer(0.5, self.state_machine)
        self.get_logger().info('Görev yöneticisi başladı.')

    def publish_initial_pose(self):
        if self.initial_pose_sent:
            return
        
        msg = PoseWithCovarianceStamped()
        msg.header.frame_id = 'map'
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.pose.pose.position.x = -2.0
        msg.pose.pose.position.y = -0.5
        msg.pose.pose.orientation.w = 1.0
        msg.pose.covariance[0] = 0.25
        msg.pose.covariance[7] = 0.25
        msg.pose.covariance[35] = 0.06853

        self.initial_pose_publisher.publish(msg)
        self.initial_pose_sent = True
        self.get_logger().info('Initial pose gönderildi!')


    def go_to(self, x, y, label):
        self.get_logger().info(f'{label} noktasına gidiliyor...')

        goal = NavigateToPose.Goal()
        goal.pose.header.frame_id = 'map'
        goal.pose.header.stamp = self.get_clock().now().to_msg()
        goal.pose.pose.position.x = x
        goal.pose.pose.position.y = y
        goal.pose.pose.orientation.w = 1.0

        self.action_client.wait_for_server()
        self._send_goal_future = self.action_client.send_goal_async(goal)
        self._send_goal_future.add_done_callback(self.goal_response_callback)
        self.navigating = True

    def goal_response_callback(self, future):
        goal_handle = future.result()
        self._result_future = goal_handle.get_result_async()
        self._result_future.add_done_callback(self.result_callback)

    def result_callback(self, future):
        self.get_logger().info(f'Hedefe ulaşıldı!')
        self.navigating = False
        self.state = RobotState.GOREVDE_BEKLIYOR

    def state_machine(self):
        msg = String()
        msg.data = self.state.name
        self.state_publisher.publish(msg)

        if self.state == RobotState.BEKLIYOR:
            self.get_logger().info('Görev başlıyor...')
            self.state = RobotState.GOREVE_GIDIYOR

        elif self.state == RobotState.GOREVE_GIDIYOR:
            if not self.navigating:
                label, x, y = self.waypoints[self.current_index]
                self.go_to(x, y, label)
        
        elif self.state == RobotState.GOREVDE_BEKLIYOR:
            label = self.waypoints[self.current_index][0]
            self.get_logger().info(f'{label} noktasında 1 saniye bekleniyor...')
            time.sleep(1.0)
            self.current_index += 1
            if self.current_index >= len(self.waypoints):
                self.state = RobotState.GOREV_TAMAMLANDI
            else: 
                self.state = RobotState.GOREVE_GIDIYOR

        elif self.state == RobotState.GOREV_TAMAMLANDI:
            self.get_logger().info('Tüm görevler tamamlandı!')
            self.timer.cancel()

def main(args=None):
    rclpy.init(args = args)
    node = TaskManager()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()