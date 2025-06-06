import pygame
import sys
import time
from menu import main as menu_main

# Константы
WINDOW_SIZE = 800
BOARD_SIZE = 8
SQUARE_SIZE = WINDOW_SIZE // BOARD_SIZE

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

class ChessPiece:
    def __init__(self, color, position, piece_type):
        self.color = color
        self.position = position
        self.piece_type = piece_type
        self.has_moved = False

class Pawn(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position, 'pawn')

    def get_valid_moves(self, board, board_instance):
        # Проверяем, что position хранится как (col, row)
        col, row = self.position
        moves = []
        direction = -1 if self.color == 'white' else 1
        start_row = 6 if self.color == 'white' else 1
        
        # Проверяем ход вперед на одну клетку
        # Обращаемся к доске board[ряд][колонка]
        if 0 <= row + direction < BOARD_SIZE:
            if board[row + direction][col] is None:
                moves.append((col, row + direction))
                
                # Проверяем ход вперед на две клетки с начальной позиции
                if not self.has_moved and board[row + 2*direction][col] is None:
                    moves.append((col, row + 2*direction))
        
        # Проверяем взятие по диагонали
        for dx in [-1, 1]: # Изменение колонки
            new_col = col + dx
            new_row = row + direction
            if 0 <= new_col < BOARD_SIZE and 0 <= new_row < BOARD_SIZE:
                target = board[new_row][new_col]
                if target is not None and target.color != self.color:
                    moves.append((new_col, new_row))
        
        # Проверяем взятие на проходе
        if board_instance.last_move:
            last_piece, last_start, last_end = board_instance.last_move
            # last_start и last_end должны быть в формате (колонка, ряд)
            if (isinstance(last_piece, Pawn) and 
                abs(last_end[1] - last_start[1]) == 2 and # Разница по рядам
                last_end[1] == row and # Закончил на том же ряду
                abs(last_end[0] - col) == 1): # Разница по колонкам
                moves.append((last_end[0], row + direction)) # Целевая позиция за съеденной пешкой
        
        return moves

class Rook(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position, 'rook')

    def get_valid_moves(self, board, board_instance):
        moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        
        for dx, dy in directions:
            x, y = self.position
            while True:
                x, y = x + dx, y + dy
                if not (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE):
                    break
                target = board[y][x]
                if target is None:
                    moves.append((x, y))
                elif target.color != self.color:
                    moves.append((x, y))
                    break
                else:
                    break
        return moves

class Knight(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position, 'knight')

    def get_valid_moves(self, board, board_instance):
        moves = []
        knight_moves = [
            (2, 1), (2, -1), (-2, 1), (-2, -1),
            (1, 2), (1, -2), (-1, 2), (-1, -2)
        ]
        
        for dx, dy in knight_moves:
            new_x = self.position[0] + dx
            new_y = self.position[1] + dy
            if 0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE:
                target = board[new_y][new_x]
                if target is None or target.color != self.color:
                    moves.append((new_x, new_y))
        return moves

class Bishop(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position, 'bishop')

    def get_valid_moves(self, board, board_instance):
        moves = []
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        
        for dx, dy in directions:
            x, y = self.position
            while True:
                x, y = x + dx, y + dy
                if not (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE):
                    break
                target = board[y][x]
                if target is None:
                    moves.append((x, y))
                elif target.color != self.color:
                    moves.append((x, y))
                    break
                else:
                    break
        return moves

class Queen(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position, 'queen')

    def get_valid_moves(self, board, board_instance):
        moves = []
        directions = [
            (0, 1), (0, -1), (1, 0), (-1, 0),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]
        
        for dx, dy in directions:
            x, y = self.position
            while True:
                x, y = x + dx, y + dy
                if not (0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE):
                    break
                target = board[y][x]
                if target is None:
                    moves.append((x, y))
                elif target.color != self.color:
                    moves.append((x, y))
                    break
                else:
                    break
        return moves

class King(ChessPiece):
    def __init__(self, color, position):
        super().__init__(color, position, 'king')

    def get_valid_moves(self, board, board_instance):
        moves = []
        directions = [
            (0, 1), (0, -1), (1, 0), (-1, 0),
            (1, 1), (1, -1), (-1, 1), (-1, -1)
        ]

        for dx, dy in directions:
            new_x = self.position[0] + dx
            new_y = self.position[1] + dy
            if 0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE:
                target = board[new_y][new_x]
                if target is None or target.color != self.color:
                    moves.append((new_x, new_y))

        # Добавляем рокировку (базовая проверка, без учета шаха)
        # Полная проверка условий рокировки (включая шах на пути и в конечной точке)
        # будет выполняться в get_valid_moves_with_check при симуляции хода короля.
        if not self.has_moved:
            # Короткая рокировка
            if (board[self.position[1]][7] is not None and
                isinstance(board[self.position[1]][7], Rook) and
                not board[self.position[1]][7].has_moved):
                # Добавляем ход рокировки, если путь свободен (без проверки на атаку)
                if board[self.position[1]][5] is None and board[self.position[1]][6] is None:
                     moves.append((6, self.position[1])) # Потенциальный ход рокировки

            # Длинная рокировка
            if (board[self.position[1]][0] is not None and
                isinstance(board[self.position[1]][0], Rook) and
                not board[self.position[1]][0].has_moved):
                 # Добавляем ход рокировки, если путь свободен (без проверки на атаку)
                if board[self.position[1]][1] is None and board[self.position[1]][2] is None and board[self.position[1]][3] is None:
                     moves.append((2, self.position[1])) # Потенциальный ход рокировки

        return moves

class ChessBoard:
    def __init__(self, time_limit=600):
        self.board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.selected_piece = None
        self.current_player = 'white'
        self.valid_moves = []
        self.game_over = False
        self.winner = None
        self.time_limit = time_limit
        self.white_time = time_limit
        self.black_time = time_limit
        self.last_move = None
        self.king_positions = {'white': None, 'black': None}
        self._move_cache = {}  # Кэш для ходов
        self.initialize_board()
        self.load_piece_images() # Загрузка изображений фигур

    def load_piece_images(self):
        """Загрузка изображений фигур"""
        self.piece_images = {}
        piece_types = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king']
        colors = ['white', 'black']
        
        for color in colors:
            for piece in piece_types:
                try:
                    image = pygame.image.load(f'assets/images/{color}_{piece}.png')
                    image = pygame.transform.scale(image, (SQUARE_SIZE - 10, SQUARE_SIZE - 10))
                    self.piece_images[f"{color}_{piece}"] = image
                except pygame.error:
                    print(f"Не удалось загрузить изображение: {color}_{piece}.png")
                    self.piece_images[f"{color}_{piece}"] = None

    def _get_move_key(self, piece, position):
        """Создает уникальный ключ для кэширования ходов"""
        return (piece.color, piece.piece_type, piece.position, position)

    def initialize_board(self):
        """Инициализирует начальную позицию фигур на доске"""
        # Расставляем пешки
        for x in range(BOARD_SIZE):
            self.board[1][x] = Pawn('black', (x, 1))
            self.board[6][x] = Pawn('white', (x, 6))
        
        # Расставляем остальные фигуры
        piece_order = ['rook', 'knight', 'bishop', 'queen', 'king', 'bishop', 'knight', 'rook']
        for x, piece_type in enumerate(piece_order):
            # Черные фигуры
            self.board[0][x] = self.create_piece('black', piece_type, (x, 0))
            # Белые фигуры
            self.board[7][x] = self.create_piece('white', piece_type, (x, 7))

        # Сохраняем начальные позиции королей
        self.king_positions = {
            'white': (4, 7),  # e1
            'black': (4, 0)   # e8
        }

    def create_piece(self, color, piece_type, position):
        piece_classes = {
            'rook': Rook,
            'knight': Knight,
            'bishop': Bishop,
            'queen': Queen,
            'king': King,
            'pawn': Pawn
        }
        return piece_classes[piece_type](color, position)

    def get_basic_moves(self, piece):
        """Получает базовые ходы фигуры без учета шаха"""
        return piece.get_valid_moves(self.board, self)

    def is_square_under_attack(self, row, col, attacking_color):
        """Проверяет, атакован ли квадрат (row, col) фигурами attacking_color"""
        # Перебираем все фигуры на доске
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                piece = self.board[y][x]
                # Если это фигура атакующего цвета
                if piece and piece.color == attacking_color:
                    # Получаем базовые ходы этой фигуры (без учета шаха и других сложных правил)
                    # Важно: здесь не вызывается get_valid_moves_with_check, чтобы избежать рекурсии
                    # Используем отдельный метод, если get_valid_moves включает сложную логику
                    if piece.piece_type == 'king':
                        # Для короля в is_square_under_attack достаточно проверить 8 соседних клеток
                        king_moves = [(piece.position[0] + dx, piece.position[1] + dy) for dx in [-1, 0, 1] for dy in [-1, 0, 1] if (dx, dy) != (0, 0)]
                        if (col, row) in king_moves:
                            return True
                    else:
                         # Для остальных фигур используем их базовые ходы
                        basic_moves = piece.get_valid_moves(self.board, self)
                        if (col, row) in basic_moves:
                            return True
        return False

    def is_king_in_check(self, color):
        """Проверяет, находится ли король под шахом"""
        king_pos = self.king_positions.get(color)
        if king_pos is None:
            return False  # Если король не найден, считаем что шаха нет

        attacking_color = 'black' if color == 'white' else 'white'
        # Проверяем, атакован ли квадрат короля
        return self.is_square_under_attack(king_pos[1], king_pos[0], attacking_color)

    def get_valid_moves_with_check(self, piece):
        """Получает список допустимых ходов с учетом шаха"""
        if self.game_over:
            return []

        # Получаем базовые ходы фигуры
        basic_moves = piece.get_valid_moves(self.board, self)
        legal_moves = []

        # Сохраняем текущее состояние
        original_board_state = [row[:] for row in self.board]
        original_king_positions = self.king_positions.copy()
        original_piece_position = piece.position
        original_has_moved = piece.has_moved
        original_last_move = self.last_move

        for move in basic_moves:
            # Проверяем кэш
            move_key = self._get_move_key(piece, move)
            if move_key in self._move_cache:
                if self._move_cache[move_key]:
                    legal_moves.append(move)
                continue

            # Симулируем ход
            target_piece = self.board[move[1]][move[0]]
            self.board[move[1]][move[0]] = piece
            self.board[piece.position[1]][piece.position[0]] = None
            piece.position = move
            piece.has_moved = True

            # Специальная обработка для рокировки при симуляции
            is_castling = False
            if piece.piece_type == 'king' and abs(move[0] - original_piece_position[0]) == 2:
                is_castling = True
                rook_original_pos = (7, original_piece_position[1]) if move[0] == 6 else (0, original_piece_position[1])
                rook_simulated_pos = (5, original_piece_position[1]) if move[0] == 6 else (3, original_piece_position[1])
                rook_piece = self.board[rook_original_pos[1]][rook_original_pos[0]]
                if rook_piece and isinstance(rook_piece, Rook):
                    self.board[rook_simulated_pos[1]][rook_simulated_pos[0]] = rook_piece
                    self.board[rook_original_pos[1]][rook_original_pos[0]] = None

            # Специальная обработка для взятия на проходе при симуляции
            is_en_passant = False
            if piece.piece_type == 'pawn' and move[0] != original_piece_position[0] and target_piece is None:
                is_en_passant = True
                captured_pawn_pos = (move[0], original_piece_position[1])
                captured_pawn = self.board[captured_pawn_pos[1]][captured_pawn_pos[0]]
                if captured_pawn and isinstance(captured_pawn, Pawn) and captured_pawn.color != piece.color:
                    self.board[captured_pawn_pos[1]][captured_pawn_pos[0]] = None

            # Обновляем позицию короля, если двигаем короля
            if piece.piece_type == 'king':
                self.king_positions[piece.color] = move

            # Временно обновляем last_move для корректной симуляции взятия на проходе
            self.last_move = (piece, original_piece_position, move)

            # Проверяем, не остался ли король под шахом после хода
            is_check_after_move = self.is_king_in_check(piece.color)

            # Сохраняем результат в кэш и добавляем ход, если нет шаха
            self._move_cache[move_key] = not is_check_after_move
            if not is_check_after_move:
                # Дополнительная проверка для рокировки
                if is_castling:
                    path_clear = True
                    if move[0] == 6:  # Короткая рокировка
                        if self.is_square_under_attack(original_piece_position[1], original_piece_position[0] + 1, 'black' if piece.color == 'white' else 'white') or \
                           self.is_square_under_attack(original_piece_position[1], original_piece_position[0] + 2, 'black' if piece.color == 'white' else 'white'):
                            path_clear = False
                    elif move[0] == 2:  # Длинная рокировка
                        if self.is_square_under_attack(original_piece_position[1], original_piece_position[0] - 1, 'black' if piece.color == 'white' else 'white') or \
                           self.is_square_under_attack(original_piece_position[1], original_piece_position[0] - 2, 'black' if piece.color == 'white' else 'white'):
                            path_clear = False
                    if path_clear:
                        legal_moves.append(move)
                else:
                    legal_moves.append(move)

            # Восстанавливаем состояние доски
            self.board = [row[:] for row in original_board_state]
            piece.position = original_piece_position
            piece.has_moved = original_has_moved
            self.king_positions = original_king_positions.copy()
            self.last_move = original_last_move

        return legal_moves

    def has_legal_moves(self, color):
        """Проверяет, есть ли у игрока легальные ходы"""
        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                piece = self.board[y][x]
                if piece and piece.color == color:
                    moves = self.get_valid_moves_with_check(piece)
                    if moves:
                        return True
        return False

    def is_checkmate(self, color):
        """Проверяет, является ли текущая позиция матом"""
        return self.is_king_in_check(color) and not self.has_legal_moves(color)

    def is_stalemate(self, color):
        """Проверяет, является ли текущая позиция патом"""
        return not self.is_king_in_check(color) and not self.has_legal_moves(color)

    def is_insufficient_material_draw(self):
        """Проверяет, является ли текущая позиция ничьей из-за недостатка материала"""
        white_pieces = []
        black_pieces = []

        for y in range(BOARD_SIZE):
            for x in range(BOARD_SIZE):
                piece = self.board[y][x]
                if piece:
                    if piece.color == 'white':
                        white_pieces.append(piece)
                    else:
                        black_pieces.append(piece)

        # Король против Короля
        if len(white_pieces) == 1 and isinstance(white_pieces[0], King) and \
           len(black_pieces) == 1 and isinstance(black_pieces[0], King):
            return True

        # Король против Короля и Слона
        if len(white_pieces) == 1 and isinstance(white_pieces[0], King) and \
           len(black_pieces) == 2 and isinstance(black_pieces[0], King) and isinstance(black_pieces[1], Bishop):
            return True
        if len(white_pieces) == 2 and isinstance(white_pieces[0], King) and isinstance(white_pieces[1], Bishop) and \
           len(black_pieces) == 1 and isinstance(black_pieces[0], King):
            return True

        # Король против Короля и Коня
        if len(white_pieces) == 1 and isinstance(white_pieces[0], King) and \
           len(black_pieces) == 2 and isinstance(black_pieces[0], King) and isinstance(black_pieces[1], Knight):
            return True
        if len(white_pieces) == 2 and isinstance(white_pieces[0], King) and isinstance(white_pieces[1], Knight) and \
           len(black_pieces) == 1 and isinstance(black_pieces[0], King):
            return True

        # Король против Короля и двух однополых Слонов
        if len(white_pieces) == 3 and isinstance(white_pieces[0], King) and isinstance(white_pieces[1], Bishop) and isinstance(white_pieces[2], Bishop):
            bishop1 = white_pieces[1]
            bishop2 = white_pieces[2]
            # Проверяем, находятся ли слоны на клетках одного цвета
            if (bishop1.position[0] + bishop1.position[1]) % 2 == (bishop2.position[0] + bishop2.position[1]) % 2:
                 if len(black_pieces) == 1 and isinstance(black_pieces[0], King):
                     return True
        if len(black_pieces) == 3 and isinstance(black_pieces[0], King) and isinstance(black_pieces[1], Bishop) and isinstance(black_pieces[2], Bishop):
            bishop1 = black_pieces[1]
            bishop2 = black_pieces[2]
            # Проверяем, находятся ли слоны на клетках одного цвета
            if (bishop1.position[0] + bishop1.position[1]) % 2 == (bishop2.position[0] + bishop2.position[1]) % 2:
                 if len(white_pieces) == 1 and isinstance(white_pieces[0], King):
                     return True

        # TODO: Добавить проверку для К+С vs К+С одного цвета
        # TODO: Добавить проверку для других возможных ничейных окончаний (при необходимости)

        return False

    def update_timers(self, dt):
        if not self.game_over:
            # Обновляем таймер текущего игрока
            if self.current_player == 'white':
                self.white_time -= dt
            else:
                self.black_time -= dt

            # Проверяем, вышло ли время
            if self.white_time <= 0:
                self.white_time = 0
                self.game_over = True
                self.winner = 'Черные'
            elif self.black_time <= 0:
                self.black_time = 0
                self.game_over = True
                self.winner = 'Белые'

    def format_time(self, seconds):
        """Форматирует время в формат MM:SS"""
        minutes = int(seconds) // 60
        seconds = int(seconds) % 60
        return f"{minutes:02d}:{seconds:02d}"

    def draw_board(self, screen):
        """Отрисовывает доску и фигуры"""
        # Отрисовка доски
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                color = WHITE if (row + col) % 2 == 0 else GRAY
                pygame.draw.rect(screen, color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        # Отрисовка фигур
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                piece = self.board[row][col]
                if piece:
                    # Используем изображение, если оно загружено
                    image_key = f"{piece.color}_{piece.piece_type}"
                    image = self.piece_images.get(image_key)
                    if image:
                        # Центрируем изображение на клетке
                        image_rect = image.get_rect(center=(col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2))
                        screen.blit(image, image_rect)
                    else:
                        # Если изображение не загружено, отрисовываем круг с буквой
                        center = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
                        radius = SQUARE_SIZE // 3
                        piece_color = BLACK if piece.color == 'white' else WHITE # Цвет буквы контрастный к фону
                        pygame.draw.circle(screen, piece_color, center, radius)

                        # Отрисовка буквы типа фигуры
                        font = pygame.font.Font(None, 36);
                        # Используем первую букву класса фигуры
                        piece_letter = piece.__class__.__name__[0].upper()
                        text = font.render(piece_letter, True, 
                                         BLACK if piece.color == 'white' else WHITE)
                        text_rect = text.get_rect(center=center)
                        screen.blit(text, text_rect)

        # Отрисовка выделения для выбранной фигуры
        if self.selected_piece:
            # selected_piece хранится как (col, row)
            col, row = self.selected_piece
            pygame.draw.rect(screen, YELLOW,
                           (col * SQUARE_SIZE, row * SQUARE_SIZE,
                            SQUARE_SIZE, SQUARE_SIZE), 3);

        # Отрисовка возможных ходов
        if self.valid_moves:
            for move in self.valid_moves:
                # move хранится как (col, row)
                if isinstance(move, tuple) and len(move) == 2:
                    col, row = move  # Правильная распаковка: (колонка, ряд)
                    center = (col * SQUARE_SIZE + SQUARE_SIZE // 2,
                             row * SQUARE_SIZE + SQUARE_SIZE // 2)
                    pygame.draw.circle(screen, BLUE, center, 10)

        # Отрисовка подсветки последнего хода
        if self.last_move:
            _ , from_pos, to_pos = self.last_move # last_move = (piece, from_pos, to_pos), позиции в (col, row)
            from_col, from_row = from_pos
            to_col, to_row = to_pos
            # Используем светло-желтый цвет для подсветки
            highlight_color = (255, 255, 153) # Светло-желтый
            # Нарисуем рамку толщиной 3 вокруг начальной и конечной клетки последнего хода
            pygame.draw.rect(screen, highlight_color, 
                             (from_col * SQUARE_SIZE, from_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)
            pygame.draw.rect(screen, highlight_color, 
                             (to_col * SQUARE_SIZE, to_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 3)

        # Отрисовка подсветки короля, если он под шахом
        if self.is_king_in_check(self.current_player):
            king_pos = self.king_positions.get(self.current_player)
            if king_pos:
                king_col, king_row = king_pos
                # Нарисуем красную рамку толщиной 5 вокруг клетки короля
                pygame.draw.rect(screen, RED, 
                                 (king_col * SQUARE_SIZE, king_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 5)

        # Отрисовка таймеров
        font = pygame.font.Font(None, 36);
        white_text = font.render(f"Белые: {int(self.white_time // 60)}:{int(self.white_time % 60):02d}", True, BLACK) # Форматируем время
        black_text = font.render(f"Черные: {int(self.black_time // 60)}:{int(self.black_time % 60):02d}", True, BLACK) # Форматируем время

        white_rect = white_text.get_rect(topleft=(10, 10))
        black_rect = black_text.get_rect(topleft=(10, 40))

        screen.blit(white_text, white_rect)
        screen.blit(black_text, black_rect);

        # Отрисовка кнопки "Играть снова"
        if self.game_over:
            self.draw_play_again_button(screen)

    def draw_play_again_button(self, screen):
        button_color = GREEN
        button_text_color = WHITE
        button_width = 200
        button_height = 50
        button_x = (WINDOW_SIZE - button_width) // 2
        button_y = WINDOW_SIZE // 2 + 100 # Располагаем ниже сообщения о победителе/ничьей

        self.play_again_button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
        pygame.draw.rect(screen, button_color, self.play_again_button_rect)

        font = pygame.font.Font(None, 36)
        text = font.render("Играть снова", True, button_text_color)
        text_rect = text.get_rect(center=self.play_again_button_rect.center)
        screen.blit(text, text_rect)

    def handle_click(self, event):
        if self.game_over:
            # Если игра окончена, проверяем клик по кнопке "Играть снова"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if hasattr(self, 'play_again_button_rect') and self.play_again_button_rect.collidepoint(event.pos):
                    self.reset_game() # Метод для сброса игры
                    # После сброса игры, выходим из обработчика клика, чтобы избежать дальнейшей обработки в старом состоянии
                    return
            return

        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        # Получаем координаты клика в формате (колонка, ряд)
        col, row = event.pos[0] // SQUARE_SIZE, event.pos[1] // SQUARE_SIZE

        # Проверяем, был ли клик в пределах доски
        if not (0 <= col < BOARD_SIZE and 0 <= row < BOARD_SIZE):
             # Если клик вне доски и есть выбранная фигура, сбрасываем выбор
            if self.selected_piece is not None:
                self.selected_piece = None
                self.valid_moves = []
            return

        # Получаем объект фигуры на кликнутом поле
        clicked_piece = self.board[row][col]

        if self.selected_piece is None:
            # Выбор фигуры
            # Проверяем, что выбрана фигура текущего игрока
            if clicked_piece is not None and clicked_piece.color == self.current_player:
                self.selected_piece = (col, row)  # Сохраняем координаты выбранной фигуры в формате (колонка, ряд)
                # Получаем легальные ходы с учетом шаха
                self.valid_moves = self.get_valid_moves_with_check(clicked_piece) # Используем функцию с учетом шаха
        else:
            # Попытка сделать ход выбранной фигурой
            move_pos = (col, row) # Целевая позиция хода в формате (колонка, ряд)

            # Проверяем, является ли выбранное поле допустимым ходом
            if move_pos in self.valid_moves:
                # Выполняем ход
                self.move_piece(self.selected_piece, move_pos)

                # --- Восстанавливаем логику проверки шаха и мата ---
                # После хода проверяем на мат или пат для СЛЕДУЮЩЕГО игрока
                next_player_color = 'black' if self.current_player == 'white' else 'white'
                if self.is_checkmate(next_player_color):
                    self.game_over = True
                    self.winner = self.current_player # Победитель - текущий игрок
                elif self.is_stalemate(next_player_color):
                     self.game_over = True
                     self.winner = None # Пат - ничья
                else:
                    # Если не мат и не пат, переключаем ход
                    self.switch_turn()
                # -----------------------------------------------------

                # Проверяем на ничью из-за недостатка материала
                if not self.game_over and self.is_insufficient_material_draw():
                    self.game_over = True
                    self.winner = None # Недостаток материала - ничья

                self.selected_piece = None
                self.valid_moves = []

            else:
                # Если ход невалидный, но клик по другой фигуре текущего игрока, выбираем её
                if clicked_piece is not None and clicked_piece.color == self.current_player:
                     self.selected_piece = (col, row)  # Сохраняем координаты выбранной фигуры
                     self.valid_moves = self.get_valid_moves_with_check(clicked_piece)
                else:
                    # Клик по пустой клетке или фигуре противника после выбора своей фигуры
                    self.selected_piece = None
                    self.valid_moves = []

    def move_piece(self, from_pos, to_pos):
        """Перемещает фигуру и обновляет состояние игры"""
        # from_pos и to_pos приходят в формате (col, row)
        from_col, from_row = from_pos
        to_col, to_row = to_pos

        piece = self.board[from_row][from_col]
        if piece is None:
            return False

        # Очищаем кэш при каждом ходе
        self._move_cache.clear()

        # Сохраняем информацию о ходе для взятия на проходе
        self.last_move = (piece, from_pos, to_pos)

        # Обновляем флаг has_moved для пешки, короля и ладьи
        if piece.piece_type in ['pawn', 'king', 'rook']:
            piece.has_moved = True

        # Обновляем позицию короля, если двигаем короля
        if piece.piece_type == 'king':
            self.king_positions[piece.color] = to_pos

        # Выполняем рокировку, если это ход короля на две клетки
        if piece.piece_type == 'king' and abs(to_col - from_col) == 2:
            # Определяем, какая ладья двигается
            rook_col = 7 if to_col > from_col else 0
            rook_to_col = to_col - 1 if to_col > from_col else to_col + 1
            rook = self.board[from_row][rook_col]
            if rook and isinstance(rook, Rook):
                self.board[from_row][rook_to_col] = rook
                self.board[from_row][rook_col] = None
                rook.position = (rook_to_col, from_row)
                rook.has_moved = True # Ладья также считается передвинутой при рокировке

        # Выполняем взятие на проходе
        # Проверяем, что фигура - пешка, ход по диагонали, и на целевой клетке пусто
        if piece.piece_type == 'pawn' and abs(to_col - from_col) == 1 and self.board[to_row][to_col] is None:
            # Это взятие на проходе, нужно убрать пешку, которая была взята
            captured_pawn_row = from_row
            captured_pawn_col = to_col # Пешка, которую берем, находится в той же колонке, куда ходит наша пешка, но на нашем ряду
            if self.board[captured_pawn_row][captured_pawn_col] and isinstance(self.board[captured_pawn_row][captured_pawn_col], Pawn):
                self.board[captured_pawn_row][captured_pawn_col] = None # Удаляем взятую пешку

        # Перемещаем фигуру на новую позицию в массиве доски
        self.board[to_row][to_col] = piece
        # Очищаем старую позицию в массиве доски
        self.board[from_row][from_col] = None
        # Обновляем позицию фигуры в объекте
        piece.position = to_pos

        # Проверяем шах и мат для следующего игрока (логика определения конца игры)
        next_player = 'black' if self.current_player == 'white' else 'white'
        if self.is_king_in_check(next_player):
            if self.is_checkmate(next_player):
                self.game_over = True
                self.winner = self.current_player
            else:
                pass # Не мат
        elif self.is_stalemate(next_player):
            self.game_over = True
            self.winner = None
        else:
            pass # Нет ни шаха, ни мата, ни пата

        return True

    def switch_turn(self):
        self.current_player = 'black' if self.current_player == 'white' else 'white'

    def reset_game(self):
        # Сброс состояния игры для начала новой игры
        self.__init__(self.time_limit) # Используем сохраненное начальное время

def main():
    try:
        print("Инициализация Pygame...")
        # Инициализация Pygame
        pygame.init()
        print("Pygame инициализирован.")

        print(f"Создание окна размером {WINDOW_SIZE}x{WINDOW_SIZE}...")
        # Создаем окно
        screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Шахматы")
        print("Окно создано. Отображение заголовка и подготовка к меню...")

        # Получаем время из меню (возвращается в минутах)
        print("Запуск меню...")
        time_limit_minutes = menu_main()
        if time_limit_minutes is None:  # Если пользователь закрыл меню
            print("Меню закрыто пользователем. Завершение работы.")
            pygame.quit()
            sys.exit()

        print(f"Время из меню получено: {time_limit_minutes} минут.")
        # Конвертируем время из минут в секунды
        time_limit_seconds = time_limit_minutes * 60
        print(f"Лимит времени в секундах: {time_limit_seconds}")

        # Создаем доску с выбранным временем (в секундах)
        print("Создание объекта ChessBoard...")
        board = ChessBoard(time_limit_seconds)
        print("Объект ChessBoard создан.")

        clock = pygame.time.Clock()
        last_time = time.time()
        print("Вход в основной игровой цикл...")

        while True:
            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print("Получено событие QUIT. Завершение Pygame.")
                    pygame.quit()
                    sys.exit()
                board.handle_click(event)

            # Обновляем таймеры
            board.update_timers(dt)

            # Отрисовка
            screen.fill(WHITE)
            board.draw_board(screen)
            pygame.display.flip()

            clock.tick(60)

    except Exception as e:
        print(f"Произошла ошибка: {e}")
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()
