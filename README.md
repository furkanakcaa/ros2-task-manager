# ROS2 Task Manager — State Machine + Nav2 Action Client

Gazi Üniversitesi Bilgisayar Mühendisliği öğrencisi olarak DRONEQUBE stajına hazırlık sürecinde geliştirdiğim ROS2 projesi.

## Proje Hakkında

State machine mimarisi kullanarak Nav2 action client ile waypoint tabanlı görev yönetimi gerçekleştiren bir ROS2 paketi. Robot Home → A → B → C → Home sırasıyla waypoint'leri ziyaret eder, her noktada 1 saniye bekler.

## Kullanılan Teknolojiler

- ROS2 Humble
- Nav2 (NavigateToPose Action)
- Gazebo Classic
- Turtlebot3 (Burger)
- Python

## Paket İçeriği

- **task_manager_node.py** — State machine + Nav2 action client
- **task_mission.launch.py** — Gazebo + Nav2 + task_manager tek komutla başlatır
- **maps/** — Cartographer ile oluşturulan harita

## Kurulum

```bash
mkdir -p ~/task_ws/src
cd ~/task_ws/src
git clone https://github.com/furkanakcaa/ros2-task-manager
mv ros2-task-manager/task_manager .
cd ~/task_ws
colcon build --packages-select task_manager
source install/setup.bash
```

## Çalıştırma

```bash
export TURTLEBOT3_MODEL=burger
ros2 launch task_manager task_mission.launch.py
```

## Geliştirme Notları

### TimerAction + IncludeLaunchDescription Sorunu

Nav2'yi launch dosyası içinden `IncludeLaunchDescription` ile başlatırken `TimerAction` içinde map parametresi boş string olarak geliyordu.

**Neden:** `IncludeLaunchDescription` parametreleri launch başlarken çözüyor, ancak `TimerAction` henüz tetiklenmediği için map değeri boş kalıyor.

**Çözüm:** `ExecuteProcess` kullanarak Nav2'yi direkt terminal komutu olarak başlattık. Bu sayede map_file değişkeni Python tarafında önceden çözülüyor ve TimerAction tetiklendiğinde komut hazır geliyor.
