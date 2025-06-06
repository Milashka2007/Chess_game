import pygame
import sys

# Константы
WINDOW_SIZE = 800

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        self.is_selected = False

    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        if self.is_selected:
            color = self.hover_color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 2)

        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

class Menu:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Шахматы - Главное меню")
        
        # Цвета
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.LIGHT_BLUE = (173, 216, 230)
        
        # Кнопки для выбора времени
        button_width = 200
        button_height = 50
        spacing = 20
        start_y = WINDOW_SIZE // 2 - 100
        
        self.time_buttons = [
            Button(WINDOW_SIZE//2 - button_width//2, start_y, 
                  button_width, button_height, "1 минута", self.GRAY, self.LIGHT_BLUE),
            Button(WINDOW_SIZE//2 - button_width//2, start_y + button_height + spacing,
                  button_width, button_height, "5 минут", self.GRAY, self.LIGHT_BLUE),
            Button(WINDOW_SIZE//2 - button_width//2, start_y + (button_height + spacing) * 2,
                  button_width, button_height, "10 минут", self.GRAY, self.LIGHT_BLUE),
            Button(WINDOW_SIZE//2 - button_width//2, start_y + (button_height + spacing) * 3,
                  button_width, button_height, "30 минут", self.GRAY, self.LIGHT_BLUE)
        ]
        
        # Кнопка для начала новой игры
        self.new_game_button = Button(WINDOW_SIZE//2 - button_width//2,
                                    start_y + (button_height + spacing) * 4,
                                    button_width, button_height,
                                    "Новая игра", self.GRAY, self.LIGHT_BLUE)
        
        self.selected_time = None

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # Проверяем нажатия на кнопки времени
                for i, button in enumerate(self.time_buttons):
                    if button.handle_event(event):
                        self.selected_time = [1, 5, 10, 30][i]
                        # Сбрасываем выделение с других кнопок
                        for other_button in self.time_buttons:
                            other_button.is_selected = False
                        button.is_selected = True
                
                # Проверяем нажатие на кнопку новой игры
                if self.new_game_button.handle_event(event):
                    if self.selected_time is not None:
                        return self.selected_time
            
            # Отрисовка
            self.screen.fill(self.WHITE)
            
            # Рисуем заголовок
            font = pygame.font.Font(None, 48)
            title = font.render("Выберите время на ход:", True, self.BLACK)
            title_rect = title.get_rect(center=(WINDOW_SIZE//2, WINDOW_SIZE//4))
            self.screen.blit(title, title_rect)
            
            # Рисуем кнопки
            for button in self.time_buttons:
                button.draw(self.screen)
            self.new_game_button.draw(self.screen)
            
            pygame.display.flip()

def main():
    pygame.init()
    menu = Menu()
    time_limit = menu.run()
    return time_limit

if __name__ == "__main__":
    main() 