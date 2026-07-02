"""
Actuators: Cơ cấu chấp hành của AMR.
- LCDDisplay: hiển thị vị trí (row, col) trên màn hình mô phỏng Pygame.
- SerialSender: gửi vị trí (row, col) sang ESP32 qua cổng Serial (UART).
"""
from component.lcd import LCDDisplay
from utils.serial_sender import SerialSender


class Actuators(object):

    def __init__(self, lcd_position=(10, 10), serial_port=None, baudrate=115200):
        """
        Khởi tạo các cơ cấu chấp hành.

        Parameters:
            lcd_position (tuple): Vị trí góc trên-trái của LCD mô phỏng (x, y).
            serial_port  (str)  : Cổng COM kết nối ESP32. None = tự động tìm.
            baudrate     (int)  : Tốc độ Serial, mặc định 9600.
        """
        self.lcd = LCDDisplay(position=lcd_position)
        self.serial = SerialSender(port=serial_port, baudrate=baudrate)

    def setPosition(self, row, col):
        """
        Cập nhật vị trí AMR:
        - Hiển thị lên LCD mô phỏng trong Pygame.
        - Gửi vị trí sang ESP32 qua Serial.

        Parameters:
            row (int): Chỉ số hàng trên bản đồ ma trận.
            col (int): Chỉ số cột trên bản đồ ma trận.
        """
        self.lcd.update(row, col)
        self.serial.send(row, col)

    def draw(self, screen):
        """
        Vẽ LCD mô phỏng lên màn hình Pygame.

        Parameters:
            screen: pygame.Surface — cửa sổ chính.
        """
        self.lcd.draw(screen)

    def close(self):
        """Đóng kết nối Serial khi thoát chương trình."""
        self.serial.close()