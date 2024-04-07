import pygame
import math
import time
from utils import scale_image, blit_rotate_center

PARKING_LOT = pygame.image.load("imgs/ParkingLot.jpg")
CAR = scale_image(pygame.image.load("imgs/Car.png"), 0.17)

WIDTH, HEIGHT = PARKING_LOT.get_width(), PARKING_LOT.get_height()

WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Self Parking car")

FPS = 60


class AbstractCar:

    def __init__(self, max_vel, min_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.min_vel = min_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.05
        self.brake = 0.08

    def rotate(self, left=False, right=False):
        if right:
            self.angle -= self.rotation_vel
        elif left:
            self.angle += self.rotation_vel

    def draw(self, win):
        blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def move_backwards(self):
        self.vel = max(self.vel - self.acceleration, self.min_vel)
        self.move()

    def brake_car(self):
        if self.vel > 0:
            self.vel = max(self.vel - self.brake, 0)
            self.move()
        if self.vel < 0:
            self.vel = min(self.vel + self.brake, 0)
            self.move()

    def move(self):
        radians = math.radians(self.angle)
        vertical = math.cos(radians) * self.vel
        horizontal = math.sin(radians) * self.vel

        self.y -= vertical
        self.x -= horizontal

    def reduce_speed(self):
        if self.vel > 0:
            self.vel = max(self.vel - self.acceleration / 2.0, 0)
            self.move()
        if self.vel < 0:
            self.vel = min(self.vel + self.acceleration / 2.0, 0)
            self.move()


class ParkingCar(AbstractCar):
    IMG = CAR
    START_POS = (180, 200)


def draw(win, images, parking_car):
    for img, pos in images:
        win.blit(img, pos)
    parking_car.draw(win)
    pygame.display.update()


run = True
clock = pygame.time.Clock()
images = [(PARKING_LOT, (0, 0))]
parking_car = ParkingCar(4, -4, 4)

while run:
    clock.tick(FPS)

    draw(WINDOW, images, parking_car)
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
    keys = pygame.key.get_pressed()
    moved = False

    if keys[pygame.K_LEFT]:
        parking_car.rotate(left=True)
    if keys[pygame.K_RIGHT]:
        parking_car.rotate(right=True)
    if keys[pygame.K_UP] and parking_car.vel >= 0:
        moved = True
        parking_car.move_forward()
    elif keys[pygame.K_DOWN] and parking_car.vel <= 0:
        moved = True
        parking_car.move_backwards()
    elif keys[pygame.K_SPACE]:
        moved = True
        parking_car.brake_car()

    if not moved:
        parking_car.reduce_speed()
pygame.quit()
