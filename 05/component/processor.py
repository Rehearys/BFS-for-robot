from random import choice
from collections import deque


class Processors(object):

    def __init__(self, obstacleSolution=()):
        self.obstacleSolution = obstacleSolution
        self.lastDecision = 90

        # --- BFS ---
        self.path = []          # danh sách các ô lưới (row, col) từ vị trí hiện tại đến đích
        self.nextStep = None    # ô lưới kế tiếp cần đi đến

    # ------------------------------------------------------------------
    # BFS: tìm đường ngắn nhất từ start đến goal trên bản đồ ma trận
    # ------------------------------------------------------------------
    def bfs(self, map, start, goal):
        """
        Tìm đường ngắn nhất từ start đến goal bằng BFS.

        Parameters:
            map   : ma trận 2D (0 = ô trống, 1 = vật cản)
            start : (row, col) vị trí hiện tại của AMR
            goal  : (row, col) vị trí đích

        Returns:
            list of (row, col) — đường đi từ start đến goal (bao gồm cả start và goal),
            hoặc [] nếu không tìm được đường.
        """
        if start == goal:
            return [start]

        rows = len(map)
        cols = len(map[0])

        # Hàng đợi BFS: mỗi phần tử là đường đi từ start đến ô hiện tại
        queue = deque()
        queue.append([start])

        visited = set()
        visited.add(start)

        # 4 hướng di chuyển: lên, xuống, trái, phải
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        while queue:
            path = queue.popleft()
            current = path[-1]

            for dr, dc in directions:
                neighbor = (current[0] + dr, current[1] + dc)
                nr, nc = neighbor

                # Kiểm tra hợp lệ
                if 0 <= nr < rows and 0 <= nc < cols \
                        and map[nr][nc] == 0 \
                        and neighbor not in visited:

                    new_path = path + [neighbor]

                    if neighbor == goal:
                        return new_path  # Tìm thấy đường đi

                    visited.add(neighbor)
                    queue.append(new_path)

        return []  # Không tìm được đường

    # ------------------------------------------------------------------
    # Lên kế hoạch đường đi BFS từ vị trí hiện tại đến đích
    # ------------------------------------------------------------------
    def planPath(self, map, amr_node, goal_node):
        """
        Gọi BFS và lưu đường đi vào self.path.

        Parameters:
            map       : ma trận bản đồ
            amr_node  : (row, col) vị trí hiện tại AMR
            goal_node : (row, col) vị trí đích
        """
        self.path = self.bfs(map, amr_node, goal_node)

    # ------------------------------------------------------------------
    # Chuyển bước đi kế tiếp (ô lưới) thành góc hướng (độ)
    # ------------------------------------------------------------------
    def nodeToAngle(self, current_node, next_node):
        """
        Chuyển đổi từ bước di chuyển sang góc hướng.

        Returns:
            int: 0 (Đông), 90 (Nam), 180 (Tây), 270 (Bắc)
            hoặc None nếu không xác định được.
        """
        dr = next_node[0] - current_node[0]
        dc = next_node[1] - current_node[1]

        if dr == -1 and dc == 0:
            return 270   # Bắc (lên trên)
        elif dr == 1 and dc == 0:
            return 90    # Nam (xuống dưới)
        elif dr == 0 and dc == -1:
            return 180   # Tây (sang trái)
        elif dr == 0 and dc == 1:
            return 0     # Đông (sang phải)
        return None

    # ------------------------------------------------------------------
    # Ra quyết định dựa trên BFS path
    # ------------------------------------------------------------------
    def makeDecisionBFS(self, amr_node):
        """
        Lấy bước đi kế tiếp từ đường BFS đã tính và chuyển thành góc hướng.

        Parameters:
            amr_node : (row, col) vị trí hiện tại AMR

        Returns:
            int: góc hướng di chuyển (0/90/180/270), hoặc None nếu đã đến đích.
        """
        if not self.path or len(self.path) < 2:
            return None

        # Tìm vị trí hiện tại trong path
        # (dùng ô đầu tiên trong path làm bước kế tiếp)
        next_node = self.path[1]
        angle = self.nodeToAngle(self.path[0], next_node)

        # Tiến path lên một bước
        self.path.pop(0)

        return angle

    # ------------------------------------------------------------------
    # Các hàm giữ nguyên từ bản gốc (dùng khi không có BFS)
    # ------------------------------------------------------------------
    def staticObstacleAvoidanceSolution(self, sensorInput) -> tuple:
        self.obstacleSolution = tuple(sensorInput)

    def makeDecision(self) -> int:
        bestSolution = None
        if (solutionNumber := len(self.obstacleSolution)) > 0:
            if solutionNumber > 1:
                obstacleSolution = list(self.obstacleSolution)
                if self.lastDecision in obstacleSolution:
                    obstacleSolution.remove(self.lastDecision)
                bestSolution = int(choice(obstacleSolution))
            else:
                bestSolution = int(self.obstacleSolution[0])
        self.lastDecision = bestSolution + 180
        if self.lastDecision >= 360:
            self.lastDecision %= 360
        return bestSolution