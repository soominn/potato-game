import pygame
import random

class BackGround:
    def __init__(self, image):
        self.image = image

    def draw(self, surface):
        surface.blit(self.image, (0, 0))

class Player:
    def __init__(self, image, x, y, speed = 500, world_w = 600):
        self.base_image = image
        self.image = image
        self.rect = self.image.get_rect(center = (x, y))
        self.speed = speed
        self.facing_right = True
        self.world_w = world_w

    def update(self, dt, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed * dt
            self.facing_right = False
        elif keys[pygame.K_RIGHT]:
            self.rect.x += self.speed * dt
            self.facing_right = True

        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > self.world_w: self.rect.right = self.world_w

        self.image = pygame.transform.flip(self.base_image, not self.facing_right, False)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class Potato:
    def __init__(self, image, speed, x, y = -60):
        self.image = image
        self.rect = self.image.get_rect(midtop = (x, y))
        self.speed = speed

    def update(self, dt):
        self.rect.y += self.speed * dt

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def is_out(self, H):
        return self.rect.top > H

class PotatoManager:
    def __init__(self, image, W, H, spawn_interval = 0.7, speed_range = (320, 700), spawn_count = 3, max_count = 120):
        self.image = image
        self.W, self.H = W, H
        self.spawn_interval = spawn_interval
        self.speed_range = speed_range
        self.spawn_count = spawn_count
        self.max_count = max_count
        self.timer = 0.0
        self.potatoes: list[Potato] = []

    def step(self, dt):
        self.timer += dt
        while self.timer >= self.spawn_interval:
            self._spawn_batch(self.spawn_count)
            self.timer -= self.spawn_interval
        for p in self.potatoes:
            p.update(dt)

    def cull_out_and_count(self):
        avoided = 0
        kept = []
        for p in self.potatoes:
            if p.is_out(self.H):
                avoided += 1
            else:
                kept.append(p)
        self.potatoes = kept
        return avoided

    def _spawn_batch(self, n):
        for _ in range(n):
            if len(self.potatoes) >= self.max_count:
                break
            self.spawn()

    def spawn(self):
        x = random.randint(25, self.W - 25)
        speed = random.uniform(*self.speed_range)
        self.potatoes.append(Potato(self.image, speed, x))

    def draw(self, surface):
        for p in self.potatoes:
            p.draw(surface)

    def collide_with(self, rect):
        return any(p.rect.colliderect(rect) for p in self.potatoes)
    
    def clear(self):
        self.potatoes.clear()
        self.timer = 0.0

class DodgeScene:
    def __init__(self, W, H):
        self.W, self.H = W, H
        self.next_scene = None

        self.background_image = pygame.image.load("./images/background.png").convert()
        self.player_image = pygame.transform.scale(pygame.image.load("./images/player.png").convert_alpha(), (45, 70))
        self.potato_image = pygame.transform.scale(pygame.image.load("./images/poisonous_potato.png").convert_alpha(), (30, 23))

        self.background = BackGround(self.background_image)
        self.player = Player(self.player_image, W / 2, H / 2 + 270, world_w = W)
        self.manager = PotatoManager(self.potato_image, W, H, spawn_interval = 0.7, speed_range = (320, 700), spawn_count = 3, max_count = 120)

        for _ in range(6):
            self.manager.spawn()

        try:
            self.font = pygame.font.Font("./fonts/PretendardVariable.ttf", 36)
            self.title_font = pygame.font.Font("./fonts/PretendardVariable.ttf", 80)
            self.hint_font = pygame.font.Font("./fonts/PretendardVariable.ttf", 28)
        except FileNotFoundError:
            self.font = pygame.font.SysFont(None, 36)
            self.title_font = pygame.font.SysFont(None, 80)
            self.hint_font = pygame.font.SysFont(None, 28)

        self.hint = self.font.render("ESC : 메뉴로", True, (0, 0, 0))
        self._dt_cap = 0.05

        self.avoided = 0
        self.elapsed = 0.0
        self.game_over = False
        self._modal_shown = False
        self._ignore_next_dt = False

        self.level = 1
        self._next_level_at = 10.0
        self._toast_timer = 0.0
        self._toast_text = ""

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.next_scene = "menu"

    def update(self, dt):
        if self.game_over:
            return

        if getattr(self, "_ignore_next_dt", False):
            dt = 0.0
            self._ignore_next_dt = False

        if self._toast_timer > 0:
            self._toast_timer = max(self._toast_timer - dt, 0.0)

        dt_for_motion = min(dt, self._dt_cap)

        keys = pygame.key.get_pressed()
        self.player.update(dt_for_motion, keys)

        self.manager.step(dt_for_motion)

        if self.manager.collide_with(self.player.rect):
            self.manager.clear()
            self.game_over = True
            return

        self.avoided += self.manager.cull_out_and_count()
        self.elapsed += dt

        if self.elapsed >= self._next_level_at:
            self.level += 1
            self._next_level_at += 10.0

            new_interval = max(0.25, self.manager.spawn_interval * 0.85)
            lo, hi = self.manager.speed_range
            lo = int(min(lo + 35, 1000))
            hi = int(min(hi + 60, 1400))

            self.manager.spawn_interval = new_interval
            self.manager.speed_range = (lo, hi)

            self._toast_text = f"난이도 상승! Lv.{self.level}"
            self._toast_timer = 1.5

    def draw(self, screen):
        self.background.draw(screen)
        self.manager.draw(screen)
        self.player.draw(screen)

        hud_left, hud_top, gap = 12, 12, 40
        txt_level   = self.font.render(f"현재 레벨 : {self.level}", True, (20, 20, 20))
        txt_avoided = self.font.render(f"피한 개수 : {self.avoided}", True, (20, 20, 20))
        txt_time    = self.font.render(f"생존 시간 : {self.elapsed:.2f}s", True, (20, 20, 20))
        screen.blit(self.hint, (hud_left, hud_top))
        screen.blit(txt_level,   (hud_left, hud_top + gap))
        screen.blit(txt_avoided, (hud_left, hud_top + gap * 2))
        screen.blit(txt_time,    (hud_left, hud_top + gap * 3))

        if self._toast_timer > 0.0 and self._toast_text:
            self._draw_toast(screen, self._toast_text, y=90)

        if self.game_over and not self._modal_shown:
            self._modal_shown = True
            self._run_game_over_modal(screen)

    def _draw_text_center(self, surface, text, font, color, y):
        s = font.render(text, True, color)
        rect = s.get_rect(center = (self.W // 2, y))
        surface.blit(s, rect)

    def _draw_toast(self, screen, text, y = 90):
        msg = self.title_font.render(text, True, (255, 255, 255))
        pad_x, pad_y = 24, 10
        card = msg.get_rect(center = (self.W // 2, y))
        card.inflate_ip(pad_x, pad_y)

        overlay = pygame.Surface(card.size, pygame.SRCALPHA)
        overlay.fill((20, 20, 20, 170))
        screen.blit(overlay, card.topleft)
        pygame.draw.rect(screen, (255, 255, 255), card, 2, border_radius = 12)

        screen.blit(msg, msg.get_rect(center = card.center))

    def _run_game_over_modal(self, screen):
        overlay = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        card_w, card_h = 520, 320
        card = pygame.Rect(0, 0, card_w, card_h)
        card.center = (self.W // 2, self.H // 2)
        pygame.draw.rect(screen, (245, 245, 245), card, border_radius = 18)
        pygame.draw.rect(screen, (220, 220, 220), card, 2, border_radius = 18)

        top = card.top
        self._draw_text_center(screen, "GAME OVER", self.title_font, (30, 30, 30), top + 70)
        self._draw_text_center(screen, f"현재 레벨 : {self.level}", self.font, (50, 50, 50), top + 140)
        self._draw_text_center(screen, f"피한 개수 : {self.avoided}", self.font, (50, 50, 50), top + 180)
        self._draw_text_center(screen, f"생존 시간 : {self.elapsed:.2f}초", self.font, (50, 50, 50), top + 220)
        self._draw_text_center(screen, "R : 재시작 | ESC : 메뉴", self.hint_font, (90, 90, 90), top + 290)
        pygame.display.flip()

        clock = pygame.time.Clock()
        waiting = True
        while waiting:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit(); raise SystemExit
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_r:
                        self.reset()
                        self._ignore_next_dt = True
                        pygame.event.clear()
                        waiting = False
                    elif e.key == pygame.K_ESCAPE:
                        self.next_scene = "menu"
                        waiting = False
            clock.tick(60)

    def reset(self):
        self.avoided = 0
        self.elapsed = 0.0
        self.game_over = False
        self._modal_shown = False
        self._ignore_next_dt = False

        self.level = 1
        self._next_level_at = 10.0
        self._toast_timer = 0.0
        self._toast_text = ""

        self.manager.clear()
        for _ in range(6):
            self.manager.spawn()
        self.player.rect.centerx = self.W // 2
        self.player.rect.centery = self.H // 2 + 270
