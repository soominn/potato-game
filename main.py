import pygame, sys
from scenes.menu import MainMenuScene
from scenes.dodge import DodgeScene
from scenes.catch import CatchScene

SCENES = {
    "menu": MainMenuScene,
    "dodge": DodgeScene,
    "catch": CatchScene,
}

def main():
    pygame.init()
    W, H = 600, 800
    FPS = 60

    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("감자 게임")
    clock = pygame.time.Clock()
    dt = 0.0

    current = SCENES["menu"](W, H)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            current.handle_event(event)

        current.update(dt)
        current.draw(screen)
        pygame.display.flip()

        if getattr(current, "next_scene", None):
            name = current.next_scene
            current = SCENES[name](W, H)

        dt = clock.tick(FPS) / 1000.0

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
