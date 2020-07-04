from core.map import Map
import pygame


class Controller:
    def __init__(self):
        self.width = 700
        self.height = 700

        self.map = Map(50, 50)

        self.column_step = self.width / self.map.columns
        self.row_step = self.height / self.map.rows

    def run(self):
        pygame.init()

        screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Conway\'s game of life')

        instructions = [
            '[P] toggle pause',
            '[C] clear',
            '[+/-] increase/decrease speed',
            '[LMB] toggle cell'
        ]

        font = pygame.font.SysFont('monospace', 18, True)
        rendered_instruction = [font.render(msg, True, (110, 190, 40)) for msg in instructions]

        clock = pygame.time.Clock()
        running = True

        paused = True
        speed = 500

        steps = 0

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        paused = not paused
                        pygame.time.set_timer(pygame.USEREVENT, 0 if paused else speed)
                    elif event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                        speed += 100
                        pygame.time.set_timer(pygame.USEREVENT, speed)
                    elif event.key == pygame.K_MINUS:
                        if speed > 0:
                            speed -= 100
                        pygame.time.set_timer(pygame.USEREVENT, speed)
                    elif event.key == pygame.K_c:
                        self.map.clear()
                        steps = 0
                elif event.type == pygame.MOUSEBUTTONDOWN and paused:
                    x, y = pygame.mouse.get_pos()
                    column, row = int(x / self.column_step), int(y / self.row_step)

                    self.map.toggle_cell_at(column, row)
                elif event.type == pygame.USEREVENT and not paused:
                    self.map.step()
                    steps += 1

            screen.fill((0, 0, 0))

            for i in range(self.map.columns):
                pygame.draw.line(screen,
                                 (50, 50, 50),
                                 (i * self.column_step, 0),
                                 (i * self.column_step, self.height))

            for i in range(self.map.rows):
                pygame.draw.line(screen,
                                 (50, 50, 50),
                                 (0, i * self.row_step),
                                 (self.width, i * self.row_step))

            for i in range(self.map.columns):
                for j in range(self.map.rows):
                    if self.map.cell_at(i, j):
                        pygame.draw.rect(screen,
                                         (255, 255, 255),
                                         (i * self.column_step, j * self.row_step, self.column_step, self.row_step))

            for i, instruction in enumerate(rendered_instruction):
                screen.blit(instruction, (0, i * instruction.get_height()))

            speed_text = font.render(f'speed: {speed}ms', True, (230, 110, 10))
            screen.blit(speed_text, (self.width - speed_text.get_width(), 0))

            status_text = font.render('paused' if paused else 'playing',
                                      True,
                                      (240, 200, 10) if paused else (110, 190, 40))
            screen.blit(status_text, (self.width - status_text.get_width(), speed_text.get_height()))

            step_count = font.render(f'{steps} steps', True, (110, 190, 40))
            screen.blit(step_count,
                        (self.width - step_count.get_width(), speed_text.get_height() + status_text.get_height()))

            pygame.display.flip()
            clock.tick(60)

        pygame.quit()
