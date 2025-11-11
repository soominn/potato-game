import pygame

class Button:
    def __init__(self, rect, text, font):
        self.rect = pygame.Rect(rect)
        self.text_surf = font.render(text, True, (0, 0, 0))
        self.text_rect = self.text_surf.get_rect(center = self.rect.center)

    def draw(self, screen):
        hovered = self.rect.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(screen, (255, 255, 255) if hovered else (210, 210, 210), self.rect, border_radius=12)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2, border_radius = 12)
        screen.blit(self.text_surf, self.text_rect)

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)

class MainMenuScene:
    def __init__(self, W, H):
        self.W, self.H = W, H
        self.next_scene = None
        try:
            self.font = pygame.font.Font("./fonts/PretendardVariable.ttf", 48)
        except FileNotFoundError:
            self.font = pygame.font.SysFont(None, 48)

        self.title = self.font.render("감자 게임", True, (50, 30, 0))
        self.title_rect = self.title.get_rect(center=(W // 2, 200))
        self.btn_dodge = Button((W // 2 - 120, 350, 240, 80), "감자 피하기", self.font)
        self.btn_catch = Button((W // 2 - 120, 470, 240, 80), "감자 받기", self.font)
        self.btn_exit  = Button((W // 2 - 120, 590, 240, 80), "게임 종료", self.font)

    def handle_event(self, event):
        if self.btn_dodge.clicked(event):
            self.next_scene = "dodge"
        if self.btn_catch.clicked(event):
            self.next_scene = "catch"
        if self.btn_exit.clicked(event):
            pygame.quit()
            raise SystemExit

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill((245, 222, 179))
        screen.blit(self.title, self.title_rect)
        self.btn_dodge.draw(screen)
        self.btn_catch.draw(screen)
        self.btn_exit.draw(screen)
