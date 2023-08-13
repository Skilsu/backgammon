import json
import random

import pygame

import sys

# Spiel-Parameter
BACKGROUND_COLOR = (0, 0, 0)
BOARD_RIM = 30

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
LIGHT_BROWN = (240, 107, 15)
DARK_BROWN = (120, 53, 7)
ORANGE = (255, 182, 0)

colors = [
    (168, 0, 185),  # Lila
    (255, 0, 255),  # pink
    (255, 0, 0),  # rot
    (255, 73, 0),  # rot-orange
    (255, 109, 0),  # orange-rot
    (255, 146, 0),  # orange
    (255, 182, 0),  # orange-gelb
    (255, 219, 0),  # gelb-orange
    (255, 255, 0),  # gelb
    (200, 255, 0)  # gelb-grün
]

width, height = 100, 100
DOTS = {
    1: [(width // 2, height // 2)],
    2: [(width // 4, height // 4), (3 * width // 4, 3 * height // 4)],
    3: [(width // 4, height // 4), (width // 2, height // 2), (3 * width // 4, 3 * height // 4)],
    4: [(width // 4, height // 4), (3 * width // 4, height // 4), (width // 4, 3 * height // 4),
        (3 * width // 4, 3 * height // 4)],
    5: [(width // 4, height // 4), (3 * width // 4, height // 4), (width // 2, height // 2),
        (width // 4, 3 * height // 4), (3 * width // 4, 3 * height // 4)],
    6: [(width // 4, height // 4), (3 * width // 4, height // 4), (width // 4, height // 2),
        (3 * width // 4, height // 2), (width // 4, 3 * height // 4), (3 * width // 4, 3 * height // 4)],
}


def read_json(filename):
    with open(f"{filename}.json", "r") as infile:
        return json.load(infile)


def save_json(filename, json_dict):
    with open(f"{filename}.json", "w") as outfile:
        json.dump(json_dict, outfile)


def draw_field_info():  # TODO maybe use logic???
    pass
    """
    pygame.draw.rect(self.screen, FIELDS[self.current_field]["color"], (0, 800, 300, 130))

    # Render the text
    if FIELDS[self.current_field]["color"] == YELLOW:
        text_color = BLACK
    else:
        text_color = WHITE

    title_surface = self.font.render(FIELDS[self.current_field]["title"], True, text_color)
    self.screen.blit(title_surface, (10, 810))

    text_lines = []
    text = FIELDS[self.current_field]["text"]
    max_line_width = 270  # Leave some padding on each side

    # Split the text into lines based on the width of the box
    words = text.split()
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        if self.font_text.size(test_line)[0] <= max_line_width:
            current_line = test_line
        else:
            text_lines.append(current_line)
            current_line = word + " "
    if current_line:
        text_lines.append(current_line)

    line_height = self.font_text.get_linesize()
    for i, line in enumerate(text_lines):
        text_surface = self.font_text.render(line, True, text_color)
        self.screen.blit(text_surface, (10, 840 + i * line_height))
        """


class Game:

    def __init__(self, screen, width, height):

        self.SCREEN_WIDTH = width
        self.SCREEN_HEIGHT = height

        self.radius = (self.SCREEN_WIDTH / 2 - self.SCREEN_WIDTH / 12 - BOARD_RIM * 2) / 12
        radius_check = self.SCREEN_HEIGHT / 16 + 35

        if self.radius > radius_check:
            self.radius = radius_check

        self.PLAYER_SPACE = self.radius * 4 + 15

        self.radius = (self.SCREEN_WIDTH / 2 - self.PLAYER_SPACE - BOARD_RIM * 2) / 12
        radius_check = self.SCREEN_HEIGHT / 16 + 35

        if self.radius > radius_check:
            self.radius = radius_check
        pygame.init()
        self.screen = screen
        # TODO self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.clock = pygame.time.Clock()
        self.state = "roll"

        self.font = pygame.font.Font(None, 35)
        self.active_color = "black"

        # click handling
        self.active_fields = []
        self.fields = []

        # game logic
        self.black = []
        self.white = []
        for i in range(26):
            self.black.append(0)
            self.white.append(0)

        self.white[0] = 2
        self.black[5] = 5
        self.black[7] = 3
        self.white[11] = 5
        self.black[12] = 5
        self.white[16] = 3
        self.white[18] = 5
        self.black[23] = 2

        self.locked_positions = []
        self.values = []
        self.motion_action = -1
        self.pos = (0, 0)

    def draw_single_info_rect(self, color, x, y, hight, witdh, amount=0, single=None, more=None):  # TODO usable???
        if amount > 0:
            pygame.draw.rect(self.screen, color, (x, y, hight, witdh))
            y += 5

            if amount == 1:
                title = self.font.render(single, True, BLACK)
            else:
                title = self.font.render(str(amount) + " " + more, True, BLACK)
            self.screen.blit(title, (x + 5, y))
            return y + 40
        return y

    def descriptions(self):  # TODO maybe later???

        debt_description_str = "Ein Schuldschein entspricht 20.000 Schulden. Du kannst einen Schuldschein zu " \
                               "jederzeit im Spiel für 22.000 abbezahlen oder du musst deine Schulden am Ende des" \
                               " Spiels für 25.000 begleichen."
        words = debt_description_str.split()
        text_lines = []
        max_line_width = 280
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if self.font.size(test_line)[0] <= max_line_width:
                current_line = test_line
            else:
                text_lines.append(current_line)
                current_line = word + " "
        if current_line:
            text_lines.append(current_line)

        line_height = self.font.get_linesize()
        for i, line in enumerate(text_lines):
            text_surface = self.font.render(line, True, BLACK)
            self.screen.blit(text_surface, (1415, 705 + i * line_height))

    def draw_wheel_fields(self, active_fields=None):
        triangles = []
        col = True
        if active_fields is None:
            active_fields = []
        for i in range(6):
            col = not col
            x = self.PLAYER_SPACE + BOARD_RIM + (self.SCREEN_WIDTH / 2 - self.PLAYER_SPACE - BOARD_RIM * 2) * i / 6
            delta_x1 = self.PLAYER_SPACE + BOARD_RIM + (self.SCREEN_WIDTH / 2 - self.PLAYER_SPACE - BOARD_RIM * 2) * (
                    i + 1) / 6
            delta_x2 = x + (delta_x1 - x) / 2
            delta_y = self.SCREEN_HEIGHT / 5 * 2

            if i in active_fields:
                if col:
                    color = WHITE
                else:
                    color = BLACK
                pygame.draw.polygon(self.screen, color,
                                    [(x - 5, BOARD_RIM - 5), (delta_x1 + 5, BOARD_RIM - 5), (delta_x2, delta_y + 15)])
            if col:
                color = BLACK
            else:
                color = WHITE
            triangles.append(pygame.draw.polygon(self.screen, color,
                                                 [(x, BOARD_RIM), (delta_x1, BOARD_RIM), (delta_x2, delta_y)]))

        for i in range(6):
            col = not col
            x = self.SCREEN_WIDTH / 2 + BOARD_RIM + (self.SCREEN_WIDTH / 2 - self.PLAYER_SPACE - BOARD_RIM * 2) * i / 6
            delta_x1 = self.SCREEN_WIDTH / 2 + BOARD_RIM + (
                    self.SCREEN_WIDTH / 2 - self.PLAYER_SPACE - BOARD_RIM * 2) * (i + 1) / 6
            delta_x2 = x + (delta_x1 - x) / 2
            delta_y = self.SCREEN_HEIGHT / 5 * 2

            if i + 6 in active_fields:
                if col:
                    color = WHITE
                else:
                    color = BLACK
                pygame.draw.polygon(self.screen, color,
                                    [(x - 5, BOARD_RIM - 5), (delta_x1 + 5, BOARD_RIM - 5), (delta_x2, delta_y + 15)])
            if col:
                color = BLACK
            else:
                color = WHITE
            triangles.append(pygame.draw.polygon(self.screen, color,
                                                 [(x, BOARD_RIM), (delta_x1, BOARD_RIM), (delta_x2, delta_y)]))
        col = not col

        for i in reversed(range(6)):
            col = not col
            y = self.SCREEN_HEIGHT - BOARD_RIM
            x = self.SCREEN_WIDTH / 2 + BOARD_RIM + (self.SCREEN_WIDTH / 2 - self.PLAYER_SPACE - BOARD_RIM * 2) * i / 6
            delta_x1 = self.SCREEN_WIDTH / 2 + BOARD_RIM + (
                    self.SCREEN_WIDTH / 2 - self.PLAYER_SPACE - BOARD_RIM * 2) * (
                               i + 1) / 6
            delta_x2 = x + (delta_x1 - x) / 2
            delta_y = self.SCREEN_HEIGHT - self.SCREEN_HEIGHT / 5 * 2

            if 17 - i in active_fields:
                if col:
                    color = WHITE
                else:
                    color = BLACK
                pygame.draw.polygon(self.screen, color,
                                    [(x - 5, y + 5), (delta_x1 + 5, y + 5),
                                     (delta_x2, delta_y - 15)])
            if col:
                color = BLACK
            else:
                color = WHITE
            triangles.append(pygame.draw.polygon(self.screen, color,
                                                 [(x, y), (delta_x1, y), (delta_x2, delta_y)]))
        for i in reversed(range(6)):
            col = not col
            y = self.SCREEN_HEIGHT - BOARD_RIM
            x = self.PLAYER_SPACE + BOARD_RIM + (self.SCREEN_WIDTH / 2 - self.PLAYER_SPACE - BOARD_RIM * 2) * i / 6
            delta_x1 = self.PLAYER_SPACE + BOARD_RIM + (
                    self.SCREEN_WIDTH / 2 - self.PLAYER_SPACE - BOARD_RIM * 2) * (
                               i + 1) / 6
            delta_x2 = x + (delta_x1 - x) / 2
            delta_y = self.SCREEN_HEIGHT - self.SCREEN_HEIGHT / 5 * 2

            if 23 - i in active_fields:
                if col:
                    color = WHITE
                else:
                    color = BLACK
                pygame.draw.polygon(self.screen, color,
                                    [(x - 5, y + 5), (delta_x1 + 5, y + 5),
                                     (delta_x2, delta_y - 15)])
            if col:
                color = BLACK
            else:
                color = WHITE
            triangles.append(pygame.draw.polygon(self.screen, color,
                                                 [(x, y), (delta_x1, y), (delta_x2, delta_y)]))
        return triangles

    def draw_dice(self, numbers):

        x = self.SCREEN_WIDTH / 2 - 25
        y = BOARD_RIM + 5
        if not numbers:
            return
        for number in numbers:
            pygame.draw.rect(self.screen, BLACK, (x, y, 50, 50), border_radius=10)  # Outer black rectangle
            pygame.draw.rect(self.screen, WHITE, (x + 5, y + 5, 40, 40), border_radius=8)  # Inner white rectangle
            for dot_position in DOTS.get(number, []):
                x_pos = dot_position[0] / 2 + x
                y_pos = dot_position[1] / 2 + y
                pygame.draw.circle(self.screen, BLACK, (x_pos, y_pos), 5)
            y += 60

    def draw_circles(self):
        color = DARK_BROWN
        fields = [pygame.draw.rect(self.screen, BLACK, (0, 0, self.PLAYER_SPACE, self.SCREEN_HEIGHT)),
                  pygame.draw.rect(self.screen, BLACK,
                                   (self.SCREEN_WIDTH - self.PLAYER_SPACE, 0, self.PLAYER_SPACE, self.SCREEN_HEIGHT))]
        for idx, field in enumerate(self.black):
            if idx < 6:
                x = self.PLAYER_SPACE + BOARD_RIM + (self.SCREEN_WIDTH / 2 - self.PLAYER_SPACE - BOARD_RIM * 2) * (
                        idx + 0.5) / 6
                y = BOARD_RIM + self.radius
                for i in range(field):
                    pygame.draw.circle(self.screen, color, (x, y), self.radius)
                    y += self.radius * 2
            elif idx < 12:
                x = self.SCREEN_WIDTH / 2 + BOARD_RIM + (self.SCREEN_WIDTH / 2 - self.PLAYER_SPACE - BOARD_RIM * 2) * (
                        idx - 6 + 0.5) / 6
                y = BOARD_RIM + self.radius
                for i in range(field):
                    pygame.draw.circle(self.screen, color, (x, y), self.radius)
                    y += self.radius * 2

            elif idx < 18:
                x = self.SCREEN_WIDTH / 2 + BOARD_RIM + (self.SCREEN_WIDTH / 2 - self.PLAYER_SPACE - BOARD_RIM * 2) * (
                        17 - idx + 0.5) / 6
                y = self.SCREEN_HEIGHT - BOARD_RIM - self.radius
                for i in range(field):
                    pygame.draw.circle(self.screen, color, (x, y), self.radius)
                    y -= self.radius * 2
            elif idx < 24:
                x = self.PLAYER_SPACE + BOARD_RIM + (self.SCREEN_WIDTH / 2 - self.PLAYER_SPACE - BOARD_RIM * 2) * (
                        23 - idx + 0.5) / 6
                y = self.SCREEN_HEIGHT - BOARD_RIM - self.radius
                for i in range(field):
                    pygame.draw.circle(self.screen, color, (x, y), self.radius)
                    y -= self.radius * 2

            elif idx == 24:
                y = self.radius
                first = True
                for i in range(field):
                    if first:
                        first = False
                        x = self.radius + 5
                        pygame.draw.circle(self.screen, color, (x, y), self.radius)
                    else:
                        first = True
                        x = self.radius * 3 + 10
                        pygame.draw.circle(self.screen, color, (x, y), self.radius)
                        y += self.radius * 2 + 5
            elif idx == 25 and field > 0:
                circle_center = (self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2 - self.radius - 5)
                if 26 in self.active_fields and self.active_color == "black":
                    val = 10
                else:
                    val = 3
                pygame.draw.circle(self.screen, ORANGE, circle_center, self.radius + val)
                fields.append(pygame.draw.circle(self.screen, color, circle_center, self.radius))

                text = self.font.render(str(field), True, WHITE)
                text_rect = text.get_rect(center=circle_center)
                self.screen.blit(text, text_rect)

        color = ORANGE
        for idx, field in enumerate(self.white):
            if idx < 6:
                x = self.PLAYER_SPACE + BOARD_RIM + (self.SCREEN_WIDTH / 2 - self.PLAYER_SPACE - BOARD_RIM * 2) * (
                        idx + 0.5) / 6
                y = BOARD_RIM + self.radius
                for i in range(field):
                    pygame.draw.circle(self.screen, color, (x, y), self.radius)
                    y += self.radius * 2
            elif idx < 12:
                x = self.SCREEN_WIDTH / 2 + BOARD_RIM + (self.SCREEN_WIDTH / 2 - self.PLAYER_SPACE - BOARD_RIM * 2) * (
                        idx - 6 + 0.5) / 6
                y = BOARD_RIM + self.radius
                for i in range(field):
                    pygame.draw.circle(self.screen, color, (x, y), self.radius)
                    y += self.radius * 2

            elif idx < 18:
                x = self.SCREEN_WIDTH / 2 + BOARD_RIM + (
                        self.SCREEN_WIDTH / 2 - self.PLAYER_SPACE - BOARD_RIM * 2) * (
                            17 - idx + 0.5) / 6
                y = self.SCREEN_HEIGHT - BOARD_RIM - self.radius
                for i in range(field):
                    pygame.draw.circle(self.screen, color, (x, y), self.radius)
                    y -= self.radius * 2
            elif idx < 24:
                x = self.PLAYER_SPACE + BOARD_RIM + (self.SCREEN_WIDTH / 2 - self.PLAYER_SPACE - BOARD_RIM * 2) * (
                        23 - idx + 0.5) / 6
                y = self.SCREEN_HEIGHT - BOARD_RIM - self.radius
                for i in range(field):
                    pygame.draw.circle(self.screen, color, (x, y), self.radius)
                    y -= self.radius * 2

            elif idx == 24:
                y = self.radius
                first = True
                for i in range(field):
                    if first:
                        first = False
                        x = self.radius + 5
                        pygame.draw.circle(self.screen, color, (x, y), self.radius)
                    else:
                        first = True
                        x = self.radius * 3 + 10
                        pygame.draw.circle(self.screen, color, (x, y), self.radius)
                        y += self.radius * 2 + 5
            elif idx == 25 and field > 0:
                circle_center = (self.SCREEN_WIDTH / 2, self.SCREEN_HEIGHT / 2 + self.radius + 5)
                if 26 in self.active_fields and self.active_color == "white":
                    pygame.draw.circle(self.screen, ORANGE, circle_center, self.radius + 10)
                    pygame.draw.circle(self.screen, LIGHT_BROWN, circle_center, self.radius + 3)
                fields.append(pygame.draw.circle(self.screen, color, circle_center, self.radius))

                text = self.font.render(str(field), True, WHITE)
                text_rect = text.get_rect(center=circle_center)
                self.screen.blit(text, text_rect)
        return fields

    def draw_background_field(self):
        pygame.draw.rect(self.screen, DARK_BROWN,
                         (self.PLAYER_SPACE, 0, self.SCREEN_WIDTH - self.PLAYER_SPACE * 2, self.SCREEN_HEIGHT))
        pygame.draw.rect(self.screen, LIGHT_BROWN, (self.PLAYER_SPACE + BOARD_RIM,
                                                    BOARD_RIM,
                                                    self.SCREEN_WIDTH - self.PLAYER_SPACE * 2 - BOARD_RIM * 2,
                                                    self.SCREEN_HEIGHT - BOARD_RIM * 2))
        pygame.draw.rect(self.screen, DARK_BROWN,
                         (self.SCREEN_WIDTH / 2 - BOARD_RIM, 0, BOARD_RIM * 2, self.SCREEN_HEIGHT))

    def find_pos(self, pos):
        for idx, rect in enumerate(self.fields):
            if rect.collidepoint(pos):
                return idx
        return -1

    def check_move(self):
        pass

    def change_pos(self, pos):
        if self.active_color == "black":
            if self.white[pos] == 0:
                if 24 in self.locked_positions:
                    self.locked_positions.remove(24 - pos)
                    self.black[24 - pos] += 1
                else:
                    self.locked_positions.remove(pos)
                    self.black[pos] += 1
                return True
            elif self.white[pos] == 1:
                self.white[pos] = 0
                self.white[25] += 1
                if 24 in self.locked_positions:
                    self.locked_positions.remove(24 - pos)
                    self.black[24 - pos] += 1
                else:
                    self.locked_positions.remove(pos)
                    self.black[pos] += 1
                return True
            elif self.white[pos] > 1:
                return False
        if self.active_color == "white":
            if self.black[pos] == 0:
                self.white[pos] += 1
                self.locked_positions.remove(pos)
                return True
            elif self.black[pos] == 1:
                self.white[pos] += 1
                self.black[pos] = 0
                self.black[25] += 1
                self.locked_positions.remove(pos)
                return True
            elif self.black[pos] > 1:
                return False

    def run(self):
        running = True
        while running:

            self.pos = pygame.mouse.get_pos()

            self.screen.fill(BACKGROUND_COLOR)
            self.draw_background_field()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_ESCAPE:
                        pass

                    if event.key == pygame.K_SPACE:
                        if self.state == "roll":
                            self.values = [random.randint(1, 6), random.randint(1, 6)]
                            if self.values[0] == self.values[1]:
                                self.values.append(self.values[0])
                                self.values.append(self.values[0])
                            self.state = "choose"
                        elif self.state == "choose":
                            if len(self.locked_positions) == 2:
                                if self.active_color == "black":
                                    if self.black[25] > 0:
                                        print(f"{self.locked_positions=}, {self.values=}")
                                        if self.locked_positions[0] == 26:
                                            val = 24 - self.locked_positions[1]
                                            if val in self.values:
                                                if self.change_pos(val):
                                                    self.black[25] -= 1
                                                    self.values.remove(val)
                                        elif self.locked_positions[1] == 26:
                                            val = 24 - self.locked_positions[0]
                                            if val in self.values:
                                                if self.change_pos(val):
                                                    self.black[25] -= 1
                                                    self.values.remove(val)
                                    elif self.locked_positions[0] > self.locked_positions[1]:
                                        val = self.locked_positions[0] - self.locked_positions[1]
                                        if val in self.values and self.black[self.locked_positions[0]] > 0:
                                            if self.change_pos(self.locked_positions[1]):
                                                self.black[self.locked_positions[0]] -= 1
                                                self.values.remove(val)
                                    else:
                                        val = self.locked_positions[1] - self.locked_positions[0]
                                        if val in self.values and self.black[self.locked_positions[1]] > 0:
                                            if self.change_pos(self.locked_positions[0]):
                                                self.black[self.locked_positions[1]] -= 1
                                                self.values.remove(val)
                                else:
                                    if self.white[25] > 0:
                                        if self.locked_positions[0] == 26:
                                            val = self.locked_positions[1]
                                            if val + 1 in self.values:
                                                if self.change_pos(val):
                                                    self.white[25] -= 1
                                                    self.values.remove(val + 1)
                                        elif self.locked_positions[1] == 26:
                                            val = self.locked_positions[0]
                                            if val + 1 in self.values:
                                                if self.change_pos(val):
                                                    self.white[25] -= 1
                                                    self.values.remove(val + 1)
                                    elif self.locked_positions[1] > self.locked_positions[0]:
                                        val = self.locked_positions[0] - self.locked_positions[1]
                                        if - val in self.values and self.white[self.locked_positions[0]] > 0:
                                            if self.change_pos(self.locked_positions[1]):
                                                self.white[self.locked_positions[0]] -= 1
                                                self.values.remove(- val)
                                    else:
                                        val = self.locked_positions[0] - self.locked_positions[1]
                                        if - val in self.values and self.white[self.locked_positions[1]] > 0:
                                            if self.change_pos(self.locked_positions[0]):
                                                self.white[self.locked_positions[1]] -= 1
                                                self.values.remove(- val)
                            self.locked_positions = []
                            self.active_fields = []
                            self.motion_action = -1
                            if not self.values:
                                self.state = "change_player"

                        if self.state == "change_player":
                            self.state = "roll"
                            if self.active_color == "black":
                                self.active_color = "white"
                            else:
                                self.active_color = "black"

                if event.type == pygame.MOUSEMOTION:
                    if self.motion_action >= 0 and self.motion_action in self.active_fields:
                        self.active_fields.remove(self.motion_action)
                    i = self.find_pos(self.pos)
                    if i not in self.active_fields:
                        self.motion_action = i
                        self.active_fields.append(i)

                if event.type == pygame.MOUSEBUTTONDOWN:
                    i = self.find_pos(self.pos)
                    if i not in self.active_fields:
                        self.active_fields.append(i)
                    if i not in self.locked_positions:
                        self.locked_positions.append(i)
                    elif self.motion_action is not i:
                        self.active_fields.remove(i)
                        self.locked_positions.remove(i)
                    self.motion_action = -1

            self.fields = self.draw_wheel_fields(self.active_fields)
            self.fields.extend(self.draw_circles())
            self.draw_dice(self.values)
            if self.active_color == "black":
                text_str = "Black"
            else:
                text_str = "White"
            text = self.font.render(text_str, True, WHITE)
            text_rect = text.get_rect(midtop=(self.SCREEN_WIDTH // 2, 5))
            self.screen.blit(text, text_rect)
            pygame.display.update()
            self.clock.tick(60)

    def move(self):
        pass


if __name__ == "__main__":
    width = 1000
    height = 750
    Game(pygame.display.set_mode((width, height)), width, height).run()
