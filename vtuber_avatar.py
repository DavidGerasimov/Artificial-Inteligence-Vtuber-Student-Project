import pygame
import math

class VTuberAvatar:
    def __init__(self, width=400, height=500):
        # Иницијализација на pygame библиотеката
        pygame.init()
        self.width = width
        self.height = height
        # Креирање на прозорец за аватарот
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("VTuber Avatar")
        
        # Контрола на frame rate (брзина на анимација)
        self.clock = pygame.time.Clock()
        self.running = True
        self.is_talking = False  # Дали аватарот зборува
        self.is_thinking = False  # Дали аватарот размислува
        
        # Систем за емоции (6 различни емоции)
        self.current_emotion = 'neutral'
        
        # Променливи за анимација
        self.bounce_offset = 0  # Офсет за подскокнување
        self.mouth_animation = 0  # Анимација на уста
        self.blink_timer = 0  # Тајмер за мигање
        self.is_blinking = False  # Дали мига
        self.think_animation = 0  # Анимација за размислување
        
        # Бои (RGB формат)
        self.bg_color = (240, 240, 255)  # Светло сина позадина
        self.skin_color = (255, 220, 200)  # Боја на кожа
        self.hair_color = (100, 70, 200)  # Виолетова коса
        self.eye_color = (50, 100, 200)  # Сини очи
        self.mouth_color = (200, 100, 100)  # Црвенкаста уста
        
        # Фонт за текст
        self.font = pygame.font.Font(None, 24)
        
        print("  ✓ VTuber avatar initialized")
        
    def start_talking(self):
        # Почеток на зборување (анимација на уста)
        self.is_talking = True
        self.is_thinking = False
    
    def stop_talking(self):
        # Крај на зборување
        self.is_talking = False
    
    def start_thinking(self):
        # Почеток на размислување (балонче за мисли)
        self.is_thinking = True
        self.is_talking = False
    
    def stop_thinking(self):
        # Крај на размислување
        self.is_thinking = False
    
    def set_emotion(self, emotion):
        # Поставување на емоцијата на аватарот
        if emotion in ['happy', 'sad', 'excited', 'confused', 'curious', 'neutral']:
            self.current_emotion = emotion
    
    def draw_avatar(self):
        # Главна функција за цртање на аватарот
        
        # Анимација на подскокнување (sine wave за smooth движење)
        self.bounce_offset = math.sin(pygame.time.get_ticks() * 0.001 * 0.1) * 10
        
        # Центрирање на аватарот
        center_x = self.width // 2
        center_y = self.height // 2 + int(self.bounce_offset)
        
        # Поднагнување на главата кога размислува
        if self.is_thinking:
            tilt = math.sin(pygame.time.get_ticks() * 0.004) * 6
            center_x += int(tilt)
        
        # Цртање на глава (круг)
        head_radius = 80
        pygame.draw.circle(self.screen, self.skin_color, (center_x, center_y), head_radius)
        
        # Цртање на коса (полигон)
        hair_points = [
            (center_x - 70, center_y - 40),
            (center_x - 50, center_y - 90),
            (center_x, center_y - 100),
            (center_x + 50, center_y - 90),
            (center_x + 70, center_y - 40)
        ]
        pygame.draw.polygon(self.screen, self.hair_color, hair_points)
        
        # Позиција на очите
        eye_y = center_y - 20
        left_eye_x = center_x - 30
        right_eye_x = center_x + 30
        
        # Логика за мигање (на секои 3 секунди)
        self.blink_timer += 1
        if self.blink_timer > 180:
            self.is_blinking = True
            if self.blink_timer > 190:
                self.is_blinking = False
                self.blink_timer = 0
        
        # Цртање на очи (различно според дали мига)
        if not self.is_blinking:
            self._draw_eyes_with_emotion(left_eye_x, right_eye_x, eye_y)
        else:
            # Затворени очи (линии)
            pygame.draw.line(self.screen, (0, 0, 0), 
                           (left_eye_x - 15, eye_y), (left_eye_x + 15, eye_y), 3)
            pygame.draw.line(self.screen, (0, 0, 0), 
                           (right_eye_x - 15, eye_y), (right_eye_x + 15, eye_y), 3)
        
        # Цртање на уста (различно според емоција и дали зборува)
        mouth_y = center_y + 20
        self._draw_mouth_with_emotion(center_x, mouth_y)
        
        # Балонче за мисли кога размислува
        if self.is_thinking:
            self.think_animation += 0.12
            # Пулсирање на балончето (sine wave за scale)
            scale = 1 + 0.08 * math.sin(self.think_animation)
            # Главно балонче
            pygame.draw.circle(self.screen, (255, 255, 255), 
                             (center_x + 90, center_y - 60), int(38 * scale))
            # Помали балончиња
            pygame.draw.circle(self.screen, (255, 255, 255), 
                             (center_x + 65, center_y - 85), int(14 * scale))
            # Три точки во балончето
            font_small = pygame.font.Font(None, 28)
            ellipsis = font_small.render("...", True, (40, 40, 80))
            self.screen.blit(ellipsis, (center_x + 78, center_y - 72))
        
        # Цртање на тело (правоаголник)
        body_rect = pygame.Rect(center_x - 60, center_y + head_radius - 20, 120, 100)
        pygame.draw.rect(self.screen, (150, 150, 250), body_rect, border_radius=10)
        
        # Статус текст (прикажува тековна состојба)
        if self.is_thinking:
            status = "Thinking..."
        elif self.is_talking:
            status = f"Talking ({self.current_emotion})"
        else:
            status = f"Idle ({self.current_emotion})"
        
        text = self.font.render(status, True, (100, 100, 100))
        self.screen.blit(text, (10, 10))
    
    def _draw_eyes_with_emotion(self, left_x, right_x, y):
        # Цртање на очи според емоцијата
        
        if self.current_emotion in ['happy', 'excited']:
            # Среќни/возбудени очи (поголеми, со сјај)
            size = 1.2 if self.current_emotion == 'excited' else 1.0
            # Бел дел на окото
            pygame.draw.circle(self.screen, (255, 255, 255), (left_x, y), int(16 * size))
            pygame.draw.circle(self.screen, (255, 255, 255), (right_x, y), int(16 * size))
            # Обоен дел
            pygame.draw.circle(self.screen, self.eye_color, (left_x, y), int(9 * size))
            pygame.draw.circle(self.screen, self.eye_color, (right_x, y), int(9 * size))
            # Зеница
            pygame.draw.circle(self.screen, (0, 0, 0), (left_x, y), int(5 * size))
            pygame.draw.circle(self.screen, (0, 0, 0), (right_x, y), int(5 * size))
            # Сјај во очите (бели точки)
            pygame.draw.circle(self.screen, (255, 255, 255), (left_x - 3, y - 3), 3)
            pygame.draw.circle(self.screen, (255, 255, 255), (right_x - 3, y - 3), 3)
        
        elif self.current_emotion == 'sad':
            # Тажни очи (помали, спуштени)
            pygame.draw.circle(self.screen, (255, 255, 255), (left_x, y), 13)
            pygame.draw.circle(self.screen, (255, 255, 255), (right_x, y), 13)
            pygame.draw.circle(self.screen, self.eye_color, (left_x, y + 2), 7)
            pygame.draw.circle(self.screen, self.eye_color, (right_x, y + 2), 7)
            pygame.draw.circle(self.screen, (0, 0, 0), (left_x, y + 2), 4)
            pygame.draw.circle(self.screen, (0, 0, 0), (right_x, y + 2), 4)
        
        elif self.current_emotion == 'confused':
            # Збунети очи (едното различно од другото)
            pygame.draw.circle(self.screen, (255, 255, 255), (left_x, y), 15)
            pygame.draw.circle(self.screen, (255, 255, 255), (right_x, y - 2), 14)
            pygame.draw.circle(self.screen, self.eye_color, (left_x, y), 8)
            pygame.draw.circle(self.screen, self.eye_color, (right_x, y - 2), 7)
            pygame.draw.circle(self.screen, (0, 0, 0), (left_x, y), 5)
            pygame.draw.circle(self.screen, (0, 0, 0), (right_x, y - 2), 4)
        
        elif self.current_emotion == 'curious':
            # Љубопитни очи (широко отворени)
            pygame.draw.circle(self.screen, (255, 255, 255), (left_x, y), 16)
            pygame.draw.circle(self.screen, (255, 255, 255), (right_x, y), 16)
            pygame.draw.circle(self.screen, self.eye_color, (left_x - 2, y), 9)
            pygame.draw.circle(self.screen, self.eye_color, (right_x + 2, y), 9)
            pygame.draw.circle(self.screen, (0, 0, 0), (left_x - 2, y), 6)
            pygame.draw.circle(self.screen, (0, 0, 0), (right_x + 2, y), 6)
            pygame.draw.circle(self.screen, (255, 255, 255), (left_x - 4, y - 2), 2)
            pygame.draw.circle(self.screen, (255, 255, 255), (right_x, y - 2), 2)
        
        else:  # neutral
            # Неутрални очи (стандардни)
            pygame.draw.circle(self.screen, (255, 255, 255), (left_x, y), 15)
            pygame.draw.circle(self.screen, (255, 255, 255), (right_x, y), 15)
            pygame.draw.circle(self.screen, self.eye_color, (left_x, y), 8)
            pygame.draw.circle(self.screen, self.eye_color, (right_x, y), 8)
            pygame.draw.circle(self.screen, (0, 0, 0), (left_x, y), 5)
            pygame.draw.circle(self.screen, (0, 0, 0), (right_x, y), 5)
            pygame.draw.circle(self.screen, (255, 255, 255), (left_x - 2, y - 2), 2)
            pygame.draw.circle(self.screen, (255, 255, 255), (right_x - 2, y - 2), 2)
    
    def _draw_mouth_with_emotion(self, center_x, mouth_y):
        # Цртање на уста според емоција и дали зборува
        
        if self.is_thinking:
            # Замислена уста (права линија)
            pygame.draw.line(self.screen, self.mouth_color,
                           (center_x - 12, mouth_y), (center_x + 12, mouth_y), 4)
        
        elif self.is_talking:
            # Анимирана уста при зборување (отвора се и затвора)
            self.mouth_animation = (self.mouth_animation + 0.3) % (2 * math.pi)
            mouth_open = abs(math.sin(self.mouth_animation)) * 15
            pygame.draw.ellipse(self.screen, self.mouth_color,
                              (center_x - 15, mouth_y, 30, int(mouth_open) + 5))
        
        elif self.current_emotion == 'happy':
            # Среќна уста (голема насмевка)
            pygame.draw.arc(self.screen, self.mouth_color,
                          (center_x - 22, mouth_y - 10, 44, 24),
                          math.pi, 2 * math.pi, 4)
        
        elif self.current_emotion == 'excited':
            # Возбудена уста (многу широка насмевка)
            pygame.draw.arc(self.screen, self.mouth_color,
                          (center_x - 25, mouth_y - 12, 50, 28),
                          math.pi, 2 * math.pi, 5)
        
        elif self.current_emotion == 'sad':
            # Тажна уста (наопаку насмевка)
            pygame.draw.arc(self.screen, self.mouth_color,
                          (center_x - 18, mouth_y + 8, 36, 18),
                          0, math.pi, 4)
        
        elif self.current_emotion == 'confused':
            # Збунета уста (валовита линија)
            points = []
            for i in range(7):
                x = center_x - 12 + i * 4
                y_off = math.sin(i * 0.8) * 2
                points.append((x, mouth_y + y_off))
            if len(points) > 1:
                pygame.draw.lines(self.screen, self.mouth_color, False, points, 3)
        
        elif self.current_emotion == 'curious':
            # Љубопитна уста (мало "О")
            pygame.draw.ellipse(self.screen, self.mouth_color,
                              (center_x - 8, mouth_y - 2, 16, 12), 3)
        
        else:  # neutral
            # Неутрална уста (нормална насмевка)
            pygame.draw.arc(self.screen, self.mouth_color,
                          (center_x - 20, mouth_y - 10, 40, 20),
                          math.pi, 2 * math.pi, 3)
    
    def run(self):
        # Главна петлја за анимација (работи во посебна нишка)
        while self.running:
            # Проверка на настани (затворање на прозорец)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            # Чистење на екран
            self.screen.fill(self.bg_color)
            # Цртање на аватарот
            self.draw_avatar()
            # Ажурирање на приказот
            pygame.display.flip()
            # Контрола на frame rate (60 FPS)
            self.clock.tick(60)
        
        # Затворање на pygame
        pygame.quit()


# Тест функција
if __name__ == "__main__":
    # Креирање и стартување на аватарот
    avatar = VTuberAvatar()
    avatar.run()