import pygame
import math
from utils import scale_image, blit_rotate_center

PARKING_LOT = pygame.image.load("imgs/ParkingLot.jpg")
PARKING_LOT_BORDERS = pygame.image.load("imgs/ParkingLotBorders.png")
PARKING_LOT_BORDERS_MASK = pygame.mask.from_surface(PARKING_LOT_BORDERS)
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
        self.curr_car = self.img
        self.curr_car_pos = (0, 0)
        self.can_bounce = 0

    def rotate(self, left=False, right=False):
        if self.vel != 0:
            if right:
                self.angle -= self.rotation_vel * self.vel
            elif left:
                self.angle += self.rotation_vel * self.vel

    def draw(self, win):
        curr_car, new_rect_pos = blit_rotate_center(win, self.img, (self.x, self.y), self.angle)
        self.curr_car = curr_car
        self.curr_car_pos = new_rect_pos

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

    def collide(self, mask, win, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.curr_car)
        offset = (int(self.curr_car_pos[0] - x), int(self.curr_car_pos[1] - y))
        poi = mask.overlap(car_mask, offset)
        return poi


class ParkingCar(AbstractCar):
    IMG = CAR
    START_POS = (5, 5)

    def reduce_speed(self):
        if self.vel > 0:
            self.vel = max(self.vel - self.acceleration / 2.0, 0)
            self.move()
        if self.vel < 0:
            self.vel = min(self.vel + self.acceleration / 2.0, 0)
            self.move()

    def bounce(self):
        self.vel = -0.5 * self.vel
        self.move()


def draw(win, images, parking_car):
    for img, pos in images:
        win.blit(img, pos)
    parking_car.draw(win)
    pygame.display.update()


run = True
clock = pygame.time.Clock()
images = [(PARKING_LOT, (0, 0))]
parking_car = ParkingCar(2, -2, 1)

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
    if keys[pygame.K_DOWN] and parking_car.vel <= 0:
        moved = True
        parking_car.move_backwards()
    elif keys[pygame.K_SPACE]:
        moved = True
        parking_car.brake_car()
    if not moved:
        parking_car.reduce_speed()

    if parking_car.can_bounce == 0:
        if parking_car.collide(PARKING_LOT_BORDERS_MASK, WINDOW) is not None:
            parking_car.bounce()
            parking_car.can_bounce = 3
    else:
        parking_car.can_bounce -= 1
pygame.quit()
