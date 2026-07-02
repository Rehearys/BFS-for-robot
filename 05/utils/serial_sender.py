"""
SerialSender: Gửi vị trí (row, col) của AMR sang ESP32 qua cổng Serial (UART).
"""

import serial
import serial.tools.list_ports


class SerialSender:

    def __init__(self, port=None, baudrate=115200):

        self.ser = None
        self.connected = False

        if port is None:
            port = self._autoDetectPort()

        if port:
            try:
                self.ser = serial.Serial(
                    port=port,
                    baudrate=baudrate,
                    timeout=1
                )

                self.connected = True
                print(f"[Serial] Đã kết nối ESP32 tại {port} - {baudrate} baud")

            except Exception as e:
                print(f"[Serial] Không thể mở cổng {port}: {e}")

        else:
            print("[Serial] Không tìm thấy ESP32. Chạy ở chế độ mô phỏng.")

    def _autoDetectPort(self):

        ports = serial.tools.list_ports.comports()

        for p in ports:

            if (
                "CP210" in p.description
                or "CH340" in p.description
                or "USB" in p.description
                or "UART" in p.description
            ):
                print(f"[Serial] Tìm thấy ESP32 tại: {p.device}")
                return p.device

        return None

    def send(self, row, col):

        if self.connected and self.ser:

            try:

                msg = f"R:{row:02d},C:{col:02d}\n"

                print("SEND:", msg.strip())

                self.ser.write(msg.encode("utf-8"))
                self.ser.flush()

            except Exception as e:

                print("[Serial Error]", e)
                self.connected = False

    def close(self):

        if self.ser and self.ser.is_open:

            self.ser.close()

            print("[Serial] Đã đóng kết nối.")