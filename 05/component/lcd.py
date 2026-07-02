"""
LCDDisplay: Mô phỏng màn hình LCD hiển thị vị trí AMR (hàng, cột)
trên bản đồ ma trận trong cửa sổ pygame.
"""
import pygame


class LCDDisplay(object):

    def __init__(self, position=(10, 10), cell_size=(200, 110)):
        """
        Khởi tạo màn hình LCD mô phỏng.

        Parameters:
            position (tuple): Tọa độ góc trên-trái của LCD trên màn hình pygame (x, y).
            cell_size (tuple): Kích thước khung LCD (width, height).
        """
        self.x, self.y = position
        self.width, self.height = cell_size
        self.row = 0
        self.col = 0

        # Màu sắc LCD thực tế
        self.color_bg        = (0,  60,  0)    # Nền LCD xanh đậm
        self.color_border    = (0, 120,  0)    # Viền LCD
        self.color_text      = (0, 230,  0)    # Chữ LCD xanh sáng
        self.color_title     = (0, 180,  0)    # Chữ tiêu đề LCD
        self.color_frame     = (40, 40, 40)    # Viền ngoài vỏ nhựa

        # Font chữ monospace
        pygame.font.init()
        self.font_title = pygame.font.SysFont("Courier New", 13, bold=True)
        self.font_text  = pygame.font.SysFont("Courier New", 20, bold=True)

    def update(self, row, col):
        """
        Cập nhật vị trí hiện tại của AMR.

        Parameters:
            row (int): Chỉ số hàng trên bản đồ ma trận.
            col (int): Chỉ số cột trên bản đồ ma trận.
        """
        self.row = row
        self.col = col

    def draw(self, screen):
        """
        Vẽ màn hình LCD lên pygame surface.

        Parameters:
            screen: pygame.Surface — cửa sổ chính của chương trình.
        """
        padding = 8

        # --- Vỏ ngoài (màu nhựa tối) ---
        outer_rect = pygame.Rect(self.x - 6, self.y - 6,
                                 self.width + 12, self.height + 12)
        pygame.draw.rect(screen, self.color_frame, outer_rect, border_radius=8)

        # --- Nền LCD ---
        inner_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.color_bg, inner_rect, border_radius=4)

        # --- Viền LCD ---
        pygame.draw.rect(screen, self.color_border, inner_rect,
                         width=2, border_radius=4)

        # --- Tiêu đề ---
        title_surf = self.font_title.render("[ LCD DISPLAY ]", True, self.color_title)
        screen.blit(title_surf, (self.x + padding, self.y + padding))

        # --- Đường kẻ ngang phân cách ---
        line_y = self.y + padding + 18
        pygame.draw.line(screen, self.color_border,
                         (self.x + padding, line_y),
                         (self.x + self.width - padding, line_y), 1)

        # --- Hiển thị Row ---
        row_text  = f"Row : {self.row:02d}"
        row_surf  = self.font_text.render(row_text, True, self.color_text)
        screen.blit(row_surf, (self.x + padding, self.y + padding + 26))

        # --- Hiển thị Col ---
        col_text  = f"Col : {self.col:02d}"
        col_surf  = self.font_text.render(col_text, True, self.color_text)
        screen.blit(col_surf, (self.x + padding, self.y + padding + 58))
