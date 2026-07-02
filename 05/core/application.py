"""
This is a main class for an application to simulate an amr in the enviroment.
"""
import pygame
import sys
from random import randint
from core.input import Input
from core.map import Maps
from core.graphic import Graphics
from core.amr import Amrs
from component.sensor import Sensors
from component.processor import Processors
from component.actuator import Actuators
from utils.utils import *


class Application(object):
    def __init__(self, screenSize=[1400, 800]):

        self.graphic = Graphics(screenSize)
        self.running = True
        self.clock = pygame.time.Clock()
        self.lastTime = pygame.time.get_ticks()
        self.input = Input()
        self.map = Maps()
        self.map.randomMap()
        self.amr = Amrs(position=[4*self.unitDistance()[1], 2*self.unitDistance()[0]])
        self.sensor = Sensors(position=[4*self.unitDistance()[1], 2*self.unitDistance()[0]])
        self.processor = Processors()

        lcd_x = self.graphic.screen.get_width() - 230
        self.actuator = Actuators(lcd_position=(lcd_x, 10))

        # --- Đích (Goal) ---
        self.goal = self._randomGoal()
        self.show_message = False
        self.goal_reached_timer = 0

        # Font thông báo
        pygame.font.init()
        self.font_msg = pygame.font.SysFont("Arial", 36, bold=True)

        # --- Lên kế hoạch BFS lần đầu ---
        amr_node = turn2node(self.map.map,
                             self.graphic.screen.get_width(),
                             self.graphic.screen.get_height(),
                             self.amr.pos[0], self.amr.pos[1])
        self.processor.planPath(self.map.map, amr_node, self.goal)

    # ------------------------------------------------------------------ #
    def _randomGoal(self):
        while True:
            row = randint(1, len(self.map.map) - 2)
            col = randint(1, len(self.map.map[0]) - 2)
            if self.map.map[row][col] == 0:
                return (row, col)

    def _goalPixel(self):
        return turn2pixel(self.map.map,
                          self.graphic.screen.get_height(),
                          self.graphic.screen.get_width(),
                          self.goal[0], self.goal[1])

    def _checkGoalReached(self, amr_node):
        return amr_node[0] == self.goal[0] and amr_node[1] == self.goal[1]

    def _drawGoal(self):
        px, py = self._goalPixel()
        pygame.draw.circle(self.graphic.screen, (255, 215, 0),   (int(px), int(py)), 14)
        pygame.draw.circle(self.graphic.screen, (255, 140, 0),   (int(px), int(py)), 8)
        pygame.draw.circle(self.graphic.screen, (255, 255, 255), (int(px), int(py)), 3)

    def _drawBFSPath(self):
        if len(self.processor.path) < 2:
            return
        for node in self.processor.path[1:]:
            px, py = turn2pixel(self.map.map,
                                self.graphic.screen.get_height(),
                                self.graphic.screen.get_width(),
                                node[0], node[1])
            pygame.draw.circle(self.graphic.screen, (100, 180, 255),
                               (int(px), int(py)), 4)

    def _drawGoalMessage(self, amr_node):
        sw = self.graphic.screen.get_width()
        sh = self.graphic.screen.get_height()
        overlay = pygame.Surface((sw, sh), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        self.graphic.screen.blit(overlay, (0, 0))
        box_w, box_h = 480, 110
        box_x = (sw - box_w) // 2
        box_y = (sh - box_h) // 2
        pygame.draw.rect(self.graphic.screen, (30, 30, 30),
                         (box_x, box_y, box_w, box_h), border_radius=12)
        pygame.draw.rect(self.graphic.screen, (255, 215, 0),
                         (box_x, box_y, box_w, box_h), width=3, border_radius=12)
        msg1 = self.font_msg.render("GOAL REACHED!", True, (255, 215, 0))
        self.graphic.screen.blit(msg1,
            (box_x + (box_w - msg1.get_width()) // 2, box_y + 15))
        font_sub = pygame.font.SysFont("Arial", 20)
        msg2 = font_sub.render(
            f"Row {amr_node[0]:02d} | Col {amr_node[1]:02d}  ->  Generating new goal...",
            True, (200, 200, 200))
        self.graphic.screen.blit(msg2,
            (box_x + (box_w - msg2.get_width()) // 2, box_y + 65))

    # ------------------------------------------------------------------ #
    def unitDistance(self):
        row_segment = len(self.map.map) - 1
        col_segment = len(self.map.map[0]) - 1
        row_distance = self.graphic.screen.get_height() / row_segment
        col_distance  = self.graphic.screen.get_width()  / col_segment
        return (row_distance, col_distance)

    def initialize(self):
        pass

    def update(self):
        pass

    def run(self):
        self.initialize()

        while self.running:

            self.input.update()
            if self.input.quit:
                self.running = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.update()

            ## vị trí ô lưới hiện tại ##
            node = turn2node(self.map.map,
                             self.graphic.screen.get_width(),
                             self.graphic.screen.get_height(),
                             self.amr.pos[0], self.amr.pos[1])

            ## kiểm tra đến đích ##
            if self._checkGoalReached(node) and not self.show_message:
                self.show_message = True
                self.goal_reached_timer = pygame.time.get_ticks()

            ## sau 1.5 giây: sinh đích mới, lên kế hoạch BFS mới ##
            if self.show_message:
                if pygame.time.get_ticks() - self.goal_reached_timer > 1500:
                    self.goal = self._randomGoal()
                    self.processor.planPath(self.map.map, node, self.goal)
                    self.show_message = False

            ## di chuyển theo BFS ##
            if not self.show_message:
                if len(self.processor.path) >= 2:
                    solution = self.processor.makeDecisionBFS(node)
                else:
                    self.processor.planPath(self.map.map, node, self.goal)
                    solution = None

                if solution is not None:
                    if solution in [90, 270]:
                        self.amr.speed = self.unitDistance()[0]
                    elif solution in [0, 180]:
                        self.amr.speed = self.unitDistance()[1]
                    self.amr.heading = solution
                    self.amr.moveForward(self.amr.speed)

            ## actuator: cập nhật LCD ##
            self.actuator.setPosition(row=node[0], col=node[1])

            ## draw ##
            self.graphic.screen.fill((255, 255, 255))
            self.graphic.drawMap(self.map.map, (220, 220, 220))
            #self._drawBFSPath()
            self._drawGoal()
            self.graphic.drawAmr(self.amr)
            self.actuator.draw(self.graphic.screen)

            if self.show_message:
                self._drawGoalMessage(node)

            pygame.display.flip()
            self.clock.tick(3)

        pygame.quit()
        sys.exit()