# AMR Simulation — Pygame + ESP32

Mô phỏng robot di động tự hành (AMR - Autonomous Mobile Robot) trên bản đồ ma trận 2D bằng Pygame, sử dụng thuật toán BFS để tìm đường đến đích và tự động sinh vật cản ngẫu nhiên. Vị trí robot được hiển thị trực quan trên một LCD giả lập trong cửa sổ mô phỏng, đồng thời có thể gửi song song sang một board ESP32 thật qua cổng Serial (UART).

## Tính năng

- 🗺️ **Bản đồ ma trận ngẫu nhiên** với biên và vật cản được sinh tự động
- 🧭 **Tìm đường bằng BFS** (Breadth-First Search) từ vị trí hiện tại đến đích
- 🎯 **Đích tự sinh lại** mỗi khi AMR đến nơi, kèm thông báo trực quan trên màn hình
- 🖥️ **LCD mô phỏng** hiển thị tọa độ (row, col) hiện tại của AMR ngay trong cửa sổ Pygame
- 🔌 **Gửi dữ liệu vị trí qua Serial/UART** sang ESP32 (tự động dò cổng COM, có chế độ mô phỏng nếu không tìm thấy thiết bị)
- 🎨 Vẽ AMR với hướng di chuyển, hai trục tọa độ cục bộ và vệt đường đi (dashed trail)

## Cấu trúc thư mục

```
.
├── core/
│   ├── amr.py           # Lớp Amrs: vị trí, hướng, di chuyển của robot
│   ├── application.py   # Lớp Application: vòng lặp chính, điều phối toàn bộ hệ thống
│   ├── graphic.py        # Lớp Graphics: vẽ bản đồ, AMR, đường đi bằng Pygame
│   ├── input.py           # Lớp Input: xử lý sự kiện bàn phím/chuột/thoát
│   └── map.py             # Lớp Maps: sinh bản đồ ma trận và vật cản ngẫu nhiên
├── component/
│   ├── sensor.py          # Lớp Sensors: dò hướng trống quanh AMR
│   ├── processor.py       # Lớp Processors: thuật toán BFS + ra quyết định hướng đi
│   ├── actuator.py        # Lớp Actuators: gộp LCD mô phỏng + gửi Serial
│   └── lcd.py              # Lớp LCDDisplay: LCD mô phỏng vẽ bằng Pygame
├── utils/
│   ├── serial_sender.py   # Lớp SerialSender: giao tiếp UART với ESP32
│   └── utils.py            # Hàm tiện ích: chuyển đổi tọa độ pixel <-> ô lưới, ma trận biến đổi 2D
└── test.py                 # Entry point chạy chương trình
```

## Yêu cầu hệ thống

- Python 3.8+
- Các thư viện:
  - `pygame`
  - `numpy`
  - `pyserial`

## Cài đặt

```bash
git clone <repository-url>
cd <repository-folder>
pip install pygame numpy pyserial
```

## Chạy chương trình

```bash
python test.py
```

Chương trình sẽ mở một cửa sổ Pygame, sinh bản đồ ngẫu nhiên, đặt AMR tại vị trí khởi đầu và tự động tìm đường đến một đích ngẫu nhiên. Khi đến đích, một thông báo sẽ hiện lên trong 1.5 giây trước khi đích mới được sinh ra và AMR tiếp tục di chuyển.

## Kết nối ESP32 (tuỳ chọn)

Nếu có board ESP32 kết nối qua USB, chương trình sẽ **tự động dò cổng COM** (dựa trên các chip phổ biến CP210x, CH340, hoặc mô tả USB/UART) và gửi vị trí AMR theo định dạng:

```
R:<row>,C:<col>\n
```

Nếu không tìm thấy thiết bị, chương trình vẫn chạy bình thường ở **chế độ mô phỏng** (chỉ hiển thị trên LCD ảo, không gửi Serial).

Có thể chỉ định cổng và baudrate thủ công khi khởi tạo `Actuators`:

```python
self.actuator = Actuators(lcd_position=(lcd_x, 10), serial_port="COM5", baudrate=115200)
```

## Kiến trúc hoạt động

1. `Maps` sinh bản đồ ma trận với vật cản ngẫu nhiên.
2. `Application` sinh đích ngẫu nhiên và gọi `Processors.planPath()` để tính đường đi BFS.
3. Ở mỗi frame, `Processors.makeDecisionBFS()` trả về hướng di chuyển tiếp theo (0°/90°/180°/270°).
4. `Amrs.moveForward()` di chuyển robot theo hướng đó.
5. `Actuators` cập nhật LCD mô phỏng và gửi vị trí qua Serial (nếu có ESP32).
6. `Graphics` vẽ lại toàn bộ khung hình: bản đồ, đích, AMR, LCD.
7. Khi AMR đến đích, hệ thống hiện thông báo, sau đó sinh đích mới và lặp lại từ bước 2.

## Giấy phép

Dự án phục vụ mục đích học tập/nghiên cứu. Vui lòng cập nhật mục License phù hợp với nhu cầu của bạn (MIT, Apache 2.0, ...).
