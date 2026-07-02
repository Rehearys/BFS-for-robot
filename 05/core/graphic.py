import pygame
import math
import numpy
# from core.map import Maps
from utils.utils import *

class Graphics(object):

    # initialize all objects to draw
    def __init__(self, screenSize):
        # initialize all pygame modules
        pygame.init()
        # indicate rendering details
        displayFlags = pygame.RESIZABLE
        # create and display the window
        self.screen = pygame.display.set_mode(screenSize, displayFlags)
        # set the text that appears in the title bar of the window
        pygame.display.set_caption("AMR in Pygame")      

    # draw dot line
    def drawDottedLine(self, color, start_pos, end_pos, dot_length=5, space_length=15):
        # Calculate total distance
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        distance = math.hypot(dx, dy)

        # Calculate unit vector
        dx /= distance
        dy /= distance

        # Draw dots
        num_dots = int(distance // (dot_length + space_length))
        for i in range(num_dots + 1):
            start_x = start_pos[0] + (dot_length + space_length) * i * dx
            start_y = start_pos[1] + (dot_length + space_length) * i * dy
            end_x = start_x + dot_length * dx
            end_y = start_y + dot_length * dy
            pygame.draw.line(self.screen, color, (start_x, start_y), (end_x, end_y), 2)

    # draw the map by pygame 
    def drawMap(self, map, color=(107, 107, 105)): 
        for row in range(len(map)): 
            pixelPos1 = turn2pixel(map, self.screen.get_height(), self.screen.get_width(), row, 0)
            pixelPos2 = turn2pixel(map, self.screen.get_height(), self.screen.get_width(), row, len(map[row]) - 1)
            pygame.draw.line(self.screen, color, pixelPos1, pixelPos2, 1) 
        for col in range(len(map[0])): 
            pixelPos1 = turn2pixel(map, self.screen.get_height(), self.screen.get_width(), 0, col)
            pixelPos2 = turn2pixel(map, self.screen.get_height(), self.screen.get_width(), len(map) - 1, col)
            pygame.draw.line(self.screen, color, pixelPos1, pixelPos2, 1)
        for row in range(len(map)): 
            for col in range(len(map[row])): 
                if map[row][col] != 0: 
                    pixelPos = turn2pixel(map, self.screen.get_height(), self.screen.get_width(), row, col)
                    pygame.draw.circle(self.screen, (255, 0, 0), pixelPos, 6) 

    # draw amr in pixel map
    def drawAmr(self, amr):
        # 4 points on amr coordinate system
        points = numpy.array([[- amr.width/2, - amr.height/2],
                              [amr.width/2, - amr.height/2],
                              [amr.width/2, amr.height/2],
                              [-amr.width/2, amr.height/2]])
        if amr.heading == 90:
            angle = 270
        elif amr.heading == 270:
            angle = 90
        else:
            angle = amr.heading
        tMatrix = transformationMatrix2d(rotation_deg=angle, translation=amr.pos)
        # 4 points of amr on the global coordinate system
        tPoints = apply_transformation(points, tMatrix)
        pygame.draw.lines(self.screen, (200, 100, 50), True, tPoints, 3)
        # two axis on amr coordinate system
        axisPoints = numpy.array([[0, 0],
                                 [amr.width, 0],
                                 [0, 0],
                                 [0, amr.height]])
        aPoints = apply_transformation(axisPoints, tMatrix)
        # draw amr x axis
        pygame.draw.line(self.screen, (255, 0, 0), aPoints[0], aPoints[1], 2)
        # draw amr y axis
        pygame.draw.line(self.screen, (0, 255, 0), aPoints[2], aPoints[3], 2)

        # draw coordinate origin of the amr in pixel        
        pygame.draw.circle(self.screen, amr.color, amr.pos, 3)
        
        # draw path
        if len(amr.path_points) > 1:
            for index in range(len(amr.path_points) - 1):
                self.drawDottedLine((245, 149, 5), amr.path_points[index], amr.path_points[index + 1])
            # pygame.draw.lines(self.screen, (255, 251, 0), closed=False, points=amr.path_points, width=2)
        

