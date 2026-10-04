import pygame, settings
import core.llm_client   as llm
import core.tts_client   as tts
import core.stt_client   as stt
import core.env_predict  as envp
import core.ui           as ui
import traceback, time

# ------------------------- Pygame init -------------------------
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((settings.WIDTH, settings.HEIGHT))
pygame.display.set_caption("Pixel Therapist – TAB‑to‑talk build")
clock = pygame.time.Clock()

background_img = pygame.image.load("assets/img/background.png").convert()
background_img = pygame.transform.scale(background_img, (settings.WIDTH, settings.HEIGHT))

idle_img, talk_img = ui.load_avatar()
avatar = idle_img

# layout constants
avatar_x, avatar_y = 30, 78
text_x,  text_y  = 400, 180   # where the thought‑bubble text appears
text_w           = 460
input_x, input_y, input_w = 40, 445, 860
hint_x,  hint_y,  hint_w  = 40, 477, 860
prompt_hint = "[TAB] to speak"

# ------------------------- Dialogue state ----------------------
history = [{
    "role": "system",
    "content": open("dialogue/system_prompts.md", encoding="utf-8").read()
}]

input_buf  = ""
reply_text = "Hi, I'm your therapist. How are you feeling today?"
print("[BOOT] Speaking intro line …")
snd = tts.speak(reply_text)

# timed reveal setup
displayed_text = reply_text
is_revealing   = False
reveal_start   = 0
reply_duration = 1.0

# ------------------------- Main loop ---------------------------
print("[BOOT] Entering main loop …")
running       = True
capture_ready = False

while running:
    user_msg = None

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        elif e.type == pygame.KEYUP and e.key == pygame.K_TAB and settings.USE_STT:
            capture_ready = True

        elif e.type == pygame.KEYDOWN:
            if e.key == pygame.K_RETURN and input_buf.strip():
                user_msg, input_buf = input_buf, ""
            elif e.key == pygame.K_BACKSPACE:
                input_buf = input_buf[:-1]
            elif e.key != pygame.K_TAB and e.unicode:
                input_buf += e.unicode

    # microphone capture
    if capture_ready:
        user_msg = stt.listen()
        capture_ready = False

    # finished user input
    if user_msg:
        history.append({"role": "user", "content": user_msg})
        avatar = talk_img

        try:
            reply_text = llm.chat(history)
        except Exception:
            traceback.print_exc()
            reply_text = "Sorry, I couldn't think of a response right now."

        history.append({"role": "assistant", "content": reply_text})

        try:
            snd = tts.speak(reply_text)
            reply_duration = snd.get_length() if snd else max(len(reply_text)*0.04, 1.0)
        except Exception:
            traceback.print_exc()
            snd = None
            reply_duration = max(len(reply_text)*0.04, 1.0)

        # start typewriter reveal
        displayed_text = ""
        reveal_start   = pygame.time.get_ticks()
        is_revealing   = True
        avatar = idle_img

    # progressive reveal synced to audio length
    if is_revealing:
        elapsed = (pygame.time.get_ticks() - reveal_start) / 1000.0
        frac    = min(1.0, elapsed / reply_duration)
        chars   = int(len(reply_text) * frac)
        displayed_text = reply_text[:chars]
        if frac >= 1.0:
            is_revealing = False

    # draw frame
    screen.blit(background_img, (0, 0))
    screen.blit(avatar, (avatar_x, avatar_y))
    ui.draw_text(screen, displayed_text, text_x, text_y, text_w)
    ui.draw_text(screen, "> " + input_buf, input_x, input_y, input_w)
    ui.draw_text(screen, prompt_hint, hint_x, hint_y, hint_w)
    pygame.display.flip()

    # simple mouth animation
    if snd and pygame.mixer.get_busy():
        avatar = talk_img if (pygame.time.get_ticks() // 120) % 2 else idle_img
    else:
        avatar = idle_img

    clock.tick(settings.FPS)

pygame.quit()
print("[BOOT] Graceful shutdown")
