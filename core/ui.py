import pygame, settings
pygame.font.init()
FONT = pygame.font.Font(settings.FONT_PATH, settings.FONT_SIZE) \
       if settings.FONT_PATH else pygame.font.Font(None, settings.FONT_SIZE)

AVATAR_W = 340   # 👈 change width to taste
AVATAR_H = 340   # 👈 change height to taste

def draw_text(surface, text, x, y, w):
    words, line, h = text.split(" "), "", 0
    for word in words:
        test = f"{line}{word} "
        img  = FONT.render(test, True, settings.TEXT_COLOR)
        if img.get_width() > w:
            surface.blit(FONT.render(line, True, settings.TEXT_COLOR), (x, y+h))
            line, h = f"{word} ", h + img.get_height() + 4
        else:
            line = test
    surface.blit(FONT.render(line, True, settings.TEXT_COLOR), (x, y+h))

def load_avatar():
    idle  = pygame.image.load("assets/img/avatar_idle.png").convert_alpha()
    talk  = pygame.image.load("assets/img/avatar_talk.png").convert_alpha()

    idle  = pygame.transform.smoothscale(idle, (AVATAR_W, AVATAR_H))
    talk  = pygame.transform.smoothscale(talk, (AVATAR_W, AVATAR_H))
    return idle, talk
