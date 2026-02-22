import pygame
import os
import random
import math
import sys


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


pygame.init()

# Настройки для мобильных устройств
info = pygame.display.Info()
# Определяем размер экрана телефона
SCREEN_WIDTH = min(info.current_w, 1080)  # Ограничиваем максимальную ширину
SCREEN_HEIGHT = min(info.current_h, 1920)  # Ограничиваем максимальную высоту

# Для телефонов обычно лучше использовать меньшие разрешения
if SCREEN_WIDTH > 800:  # Если экран большой, уменьшаем для производительности
    SCALE_FACTOR = 0.7
    SCREEN_WIDTH = int(SCREEN_WIDTH * SCALE_FACTOR)
    SCREEN_HEIGHT = int(SCREEN_HEIGHT * SCALE_FACTOR)


# Загрузка изображений с оптимизацией
def load_and_scale_image(path, scale=1):
    try:
        img = pygame.image.load(resource_path(path))
        # Оптимизация изображения для телефона
        if scale != 1:
            new_width = int(img.get_width() * scale)
            new_height = int(img.get_height() * scale)
            img = pygame.transform.scale(img, (new_width, new_height))
        return img.convert_alpha()  # convert_alpha для ускорения
    except:
        return None


# Загрузка изображений с правильными путями и масштабированием
vodka_img = load_and_scale_image('mobs/vodka.png', 0.8)
burger_img = load_and_scale_image('mobs/burger.png', 0.8)
icons = load_and_scale_image('image/Gameicons.png', 0.5)
player_img = load_and_scale_image('image/player.png', 0.9)

# Шрифты (уменьшаем размер для телефона)
font_size = int(25 * (SCREEN_WIDTH / 1000))
big_font_size = int(40 * (SCREEN_WIDTH / 1000))
menu_font_size = int(50 * (SCREEN_WIDTH / 1000))

try:
    font = pygame.font.Font(resource_path('font/font.ttf'), font_size)
    big_font = pygame.font.Font(resource_path('font/font.ttf'), big_font_size)
    menu_font = pygame.font.Font(resource_path('font/font.ttf'), menu_font_size)
except:
    font = pygame.font.Font(None, font_size)
    big_font = pygame.font.Font(None, big_font_size)
    menu_font = pygame.font.Font(None, menu_font_size)

# Загружаем изображение сала
try:
    salo_img = load_and_scale_image('mobs/salo.png', 0.7)
    if salo_img is None:
        raise Exception
except:
    salo_img = pygame.Surface((int(120 * SCREEN_WIDTH / 1000), int(80 * SCREEN_WIDTH / 1000)))
    salo_img.fill((255, 182, 193))
    salo_text = font.render("САЛО", True, (0, 0, 0))
    text_rect = salo_text.get_rect(center=(salo_img.get_width() // 2, salo_img.get_height() // 2))
    salo_img.blit(salo_text, text_rect)

# Загружаем изображение масла
try:
    oil_img = load_and_scale_image('mobs/oil.png', 0.7)
    if oil_img is None:
        raise Exception
except:
    oil_img = pygame.Surface((int(150 * SCREEN_WIDTH / 1000), int(150 * SCREEN_WIDTH / 1000)))
    oil_img.fill((255, 255, 0))
    oil_text = font.render("МАСЛО", True, (0, 0, 0))
    text_rect = oil_text.get_rect(center=(oil_img.get_width() // 2, oil_img.get_height() // 2))
    oil_img.blit(oil_text, text_rect)

# Создаем окно на весь экран для телефона
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Burmaldatik Mobile')
if icons:
    pygame.display.set_icon(icons)

# Цвета (без изменений)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (237, 145, 33)
PURPLE = (128, 0, 128)
PINK = (255, 182, 193)
GOLD = (255, 215, 0)

# Переменные для сенсорного управления
touch_active = False
touch_x = 0
touch_y = 0
jump_pressed = False


# Класс для снаряда сала (оптимизирован)
class SaloProjectile:
    def __init__(self, x, y, target_x, target_y):
        self.x = x
        self.y = y
        size = int(25 * (SCREEN_WIDTH / 1000))
        self.width = size
        self.height = int(size * 0.7)
        self.rect = pygame.Rect(x, y, self.width, self.height)

        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx ** 2 + dy ** 2)
        if distance > 0:
            speed = 15 * (SCREEN_WIDTH / 1000)
            self.speed_x = (dx / distance) * speed
            self.speed_y = (dy / distance) * speed
        else:
            self.speed_x = 10
            self.speed_y = 0

        self.active = True
        self.scaled_salo = pygame.transform.scale(salo_img, (self.width, self.height))

    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.rect.x = self.x
        self.rect.y = self.y

        if self.x > SCREEN_WIDTH + 100 or self.x < -100 or self.y > SCREEN_HEIGHT + 100 or self.y < -100:
            self.active = False

    def draw(self, screen):
        screen.blit(self.scaled_salo, (self.x, self.y))


# Класс для кнопки (оптимизирован для телефона)
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, font_size=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.clicked = False
        if font_size is None:
            font_size = int(40 * (SCREEN_WIDTH / 1000))
        self.font = pygame.font.Font(resource_path('font/font.ttf'), font_size)

    def draw(self, screen):
        pygame.draw.rect(screen, self.current_color, self.rect, border_radius=10)
        pygame.draw.rect(screen, BLACK, self.rect, 3, border_radius=10)
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def update(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.current_color = self.hover_color
        else:
            self.current_color = self.color

    def is_clicked(self, mouse_pos, mouse_click):
        return self.rect.collidepoint(mouse_pos) and mouse_click[0]


# Функция магазина (оптимизирована)
def shop_screen(burger_count, salo_count):
    shop_run = True
    clock_shop = pygame.time.Clock()

    btn_width = int(300 * (SCREEN_WIDTH / 1000))
    btn_height = int(80 * (SCREEN_WIDTH / 1000))

    buy_salo_button = Button(SCREEN_WIDTH // 2 - btn_width // 2, SCREEN_HEIGHT // 2 - 100,
                             btn_width, btn_height, "КУПИТЬ САЛО", GREEN, YELLOW, 30)
    exit_button = Button(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 150,
                         200, 60, "НАЗАД", BLUE, YELLOW, 40)

    purchase_message = ""
    purchase_timer = 0

    while shop_run:
        clock_shop.tick(60)
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_AC_BACK:  # Обработка кнопки "Назад" на Android
                    return burger_count, salo_count

        buy_salo_button.update(mouse_pos)
        exit_button.update(mouse_pos)

        if buy_salo_button.is_clicked(mouse_pos, mouse_click):
            if burger_count >= 20:
                burger_count -= 20
                salo_count += 1
                purchase_message = f"Куплено сало! Всего: {salo_count}"
                purchase_timer = 90
            else:
                purchase_message = f"Нужно еще {20 - burger_count} бургеров"
                purchase_timer = 90

        if exit_button.is_clicked(mouse_pos, mouse_click):
            return burger_count, salo_count

        if purchase_timer > 0:
            purchase_timer -= 1
        else:
            purchase_message = ""

        screen.fill(ORANGE)

        # Заголовок
        title_surface = menu_font.render("МАГАЗИН", True, BLACK)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 80))
        screen.blit(title_surface, title_rect)

        # Информация
        y_offset = 150
        burger_info = font.render(f"Бургеры: {burger_count}", True, BLACK)
        screen.blit(burger_info, (SCREEN_WIDTH // 2 - 100, y_offset))

        salo_info = font.render(f"Сало: {salo_count}", True, BLACK)
        screen.blit(salo_info, (SCREEN_WIDTH // 2 - 100, y_offset + 40))

        # Товар
        pygame.draw.rect(screen, PINK, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50, 300, 100), border_radius=10)
        pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 50, 300, 100), 3,
                         border_radius=10)

        salo_rect = salo_img.get_rect(center=(SCREEN_WIDTH // 2 - 70, SCREEN_HEIGHT // 2))
        screen.blit(salo_img, salo_rect)

        price_text = font.render("20 бургеров", True, BLACK)
        screen.blit(price_text, (SCREEN_WIDTH // 2 + 20, SCREEN_HEIGHT // 2 - 20))

        buy_salo_button.draw(screen)
        exit_button.draw(screen)

        if purchase_message:
            msg_surface = font.render(purchase_message, True, PURPLE if "Куплено" in purchase_message else RED)
            msg_rect = msg_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
            screen.blit(msg_surface, msg_rect)

        pygame.display.update()


# Функция экрана проигрыша
def game_over_screen(drink_count):
    over_run = True
    clock_over = pygame.time.Clock()

    restart_button = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 200, 300, 80, "ЗАНОВО", GREEN, YELLOW, 40)
    menu_button = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT - 100, 300, 80, "МЕНЮ", BLUE, YELLOW, 40)

    while over_run:
        clock_over.tick(60)
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_AC_BACK:
                    return "menu"

        restart_button.update(mouse_pos)
        menu_button.update(mouse_pos)

        if restart_button.is_clicked(mouse_pos, mouse_click):
            return "restart"
        if menu_button.is_clicked(mouse_pos, mouse_click):
            return "menu"

        screen.fill(ORANGE)

        oil_rect = oil_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(oil_img, oil_rect)

        game_over_text = big_font.render("ТЫ ПЕРЕПИЛ!", True, RED)
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        screen.blit(game_over_text, text_rect)

        count_text = font.render(f"Выпито: {drink_count}/16", True, BLACK)
        screen.blit(count_text, (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2 + 100))

        restart_button.draw(screen)
        menu_button.draw(screen)

        pygame.display.update()


# Функция главного меню
def show_menu():
    menu_run = True
    clock_menu = pygame.time.Clock()
    start_button = Button(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2, 300, 80, "СТАРТ", GREEN, YELLOW)
    bg_offset = 0

    while menu_run:
        clock_menu.tick(60)
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        start_button.update(mouse_pos)

        if start_button.is_clicked(mouse_pos, mouse_click):
            return

        screen.fill(ORANGE)

        # Упрощенный фон для производительности
        bg_offset = (bg_offset + 2) % 60
        if random.random() < 0.1:  # Рисуем не каждый кадр для экономии батареи
            for i in range(0, SCREEN_WIDTH, 80):
                screen.blit(pygame.transform.scale(vodka_img, (20, 20)), (i + bg_offset, 100))
                screen.blit(pygame.transform.scale(burger_img, (20, 20)), (i - bg_offset, 200))

        title_surface = menu_font.render("BURMALDATIK", True, BLACK)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title_surface, title_rect)

        start_button.draw(screen)

        # Инструкции
        info_y = SCREEN_HEIGHT // 2 + 100
        info_text = font.render("Стрелки/Свайпы - движение", True, BLACK)
        screen.blit(info_text, (SCREEN_WIDTH // 2 - 150, info_y))

        info_text2 = font.render("M - магазин, Тап - кинуть сало", True, PURPLE)
        screen.blit(info_text2, (SCREEN_WIDTH // 2 - 150, info_y + 40))

        pygame.display.update()


# Основная функция игры
def main_game():
    # Базовые параметры
    ps = int(8 * (SCREEN_WIDTH / 1000))
    px = 50
    GROUND_Y = SCREEN_HEIGHT - 150
    py = GROUND_Y
    is_jump = False
    jump_count = 10
    run = True
    salo_count = 0

    LEFT_BOUND = 20
    RIGHT_BOUND = SCREEN_WIDTH - 100

    vodka_list = []
    burger_list = []
    projectiles = []

    message = ""
    message_timer = 0
    message_alpha = 255
    drink_count = 0
    burger_count = 0
    special_message_shown = False

    drink_messages = ["Леха выпил водку(((", "Шансон врубайте", "на искупаться", "ШАНСООООН"]
    burger_messages = ["Леха покушал! 🍔", "Вкусняшка!", "Ням-ням!", "Бургер съеден!"]

    vodka_timer = pygame.USEREVENT + 1
    burger_timer = pygame.USEREVENT + 2
    pygame.time.set_timer(vodka_timer, 3000)
    pygame.time.set_timer(burger_timer, 6000)

    clock = pygame.time.Clock()

    # Для сенсорного управления
    last_touch_x = px

    while run:
        dt = clock.tick(60) / 16.67  # Нормализация времени

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            # Сенсорное управление
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Левый клик/тап
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    if salo_count > 0 and mouse_y < SCREEN_HEIGHT - 200:  # Не в области кнопок
                        new_projectile = SaloProjectile(px + 35, py + 35, mouse_x, mouse_y)
                        projectiles.append(new_projectile)
                        salo_count -= 1
                        message = "Сало летит!"
                        message_timer = 60
                        message_alpha = 255

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    burger_count, salo_count = shop_screen(burger_count, salo_count)

            if event.type == vodka_timer:
                new_vodka = pygame.Rect(SCREEN_WIDTH - 100, GROUND_Y, 40, 40)
                vodka_list.append(new_vodka)

            if event.type == burger_timer:
                new_burger = pygame.Rect(SCREEN_WIDTH - 100, random.randint(GROUND_Y - 100, GROUND_Y), 40, 40)
                burger_list.append(new_burger)

        # Управление с клавиатуры или сенсора
        keys = pygame.key.get_pressed()

        # Горизонтальное движение
        if keys[pygame.K_LEFT] and px > LEFT_BOUND:
            px -= ps
        if keys[pygame.K_RIGHT] and px < RIGHT_BOUND:
            px += ps

        # Прыжок
        if not is_jump:
            if keys[pygame.K_UP]:
                is_jump = True
        else:
            if jump_count >= -10:
                if jump_count > 0:
                    py -= (jump_count ** 2) / 1.5
                else:
                    py += (jump_count ** 2) / 1.5
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 10
                py = GROUND_Y

        # Движение объектов
        for vodka_rect in vodka_list[:]:
            vodka_rect.x -= 8
            if vodka_rect.x < -100:
                vodka_list.remove(vodka_rect)

        for burger_rect in burger_list[:]:
            burger_rect.x -= 6
            if burger_rect.x < -100:
                burger_list.remove(burger_rect)

        # Обновление снарядов
        for projectile in projectiles[:]:
            projectile.update()
            if not projectile.active:
                projectiles.remove(projectile)
                continue

            for vodka_rect in vodka_list[:]:
                if projectile.rect.colliderect(vodka_rect):
                    vodka_list.remove(vodka_rect)
                    projectiles.remove(projectile)
                    break

        # Столкновения с игроком
        player_rect = pygame.Rect(px, py, 50, 50)

        for vodka_rect in vodka_list[:]:
            if player_rect.colliderect(vodka_rect):
                message = random.choice(drink_messages)
                message_timer = 90
                message_alpha = 255
                drink_count += 1
                vodka_list.remove(vodka_rect)

                if drink_count >= 15 and not special_message_shown:
                    message = "я не рассчитал силу водки"
                    message_timer = 180
                    special_message_shown = True

                if drink_count >= 16:
                    return "game_over", drink_count, burger_count, salo_count

        for burger_rect in burger_list[:]:
            if player_rect.colliderect(burger_rect):
                message = random.choice(burger_messages)
                message_timer = 90
                message_alpha = 255
                burger_count += 1
                burger_list.remove(burger_rect)

        # Обновление сообщения
        if message_timer > 0:
            message_timer -= 1
            if message_timer < 30:
                message_alpha = int(255 * (message_timer / 30))
        else:
            message = ""

        # Отрисовка
        screen.fill(ORANGE)
        pygame.draw.rect(screen, (100, 100, 100), (0, GROUND_Y + 50, SCREEN_WIDTH, 10))

        # Рисуем игрока
        if player_img:
            screen.blit(player_img, (px, py))
        else:
            pygame.draw.rect(screen, BLUE, (px, py, 50, 50))

        # Рисуем объекты
        for vodka_rect in vodka_list:
            if vodka_img:
                screen.blit(vodka_img, vodka_rect)
            else:
                pygame.draw.rect(screen, RED, vodka_rect)

        for burger_rect in burger_list:
            if burger_img:
                screen.blit(burger_img, burger_rect)
            else:
                pygame.draw.rect(screen, GREEN, burger_rect)

        for projectile in projectiles:
            projectile.draw(screen)

        # Сообщение
        if message:
            text_surface = font.render(message, True, RED)
            text_surface.set_alpha(message_alpha)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 100))
            screen.blit(text_surface, text_rect)

        # Статистика
        y = 10
        screen.blit(font.render(f'Водки: {len(vodka_list)}', True, BLACK), (10, y))
        screen.blit(font.render(f'Бургеры: {len(burger_list)}', True, BLACK), (10, y + 30))
        screen.blit(font.render(f'Выпито: {drink_count}/16', True, BLACK), (10, y + 60))
        screen.blit(font.render(f'Съедено: {burger_count}', True, BLACK), (10, y + 90))
        screen.blit(font.render(f'Сало: {salo_count}', True, PURPLE), (10, y + 120))

        # Подсказка
        hint = font.render("M - магазин", True, PURPLE)
        screen.blit(hint, (SCREEN_WIDTH - 200, 20))

        pygame.display.update()


# Запуск игры
while True:
    show_menu()
    result, drink_count, burger_count, salo_count = main_game()

    if result == "game_over":
        action = game_over_screen(drink_count)
        if action == "menu":
            continue
        elif action == "restart":
            continue
    else:
        break

pygame.quit()
