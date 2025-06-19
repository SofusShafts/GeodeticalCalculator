
#===============================================================================================================================================================
import math
import os
from datetime import datetime
class GeodeticCalculator:
    def __init__(self):
        self.results_file = "teodolit.txt"
        self.counter = 1
        self.history = []  # Список хранения истории операций
        self.points = {}  # Словарь хранения точек (ID: (x, y))
        if not os.path.exists(self.results_file):
            with open(self.results_file, 'w', encoding='utf-8') as f:
                f.write("Результаты геодезических расчетов\n\n")
    def save_to_file(self, data):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        record = (self.counter, timestamp, data)  # Кортеж записи истории
        self.history.append(record)  # Добавляем в список истории
        with open(self.results_file, 'a', encoding='utf-8') as f:
            f.write(f"{self.counter}. {timestamp}\n")
            f.write(data + "\n\n")
            self.counter += 1
    def get_valid_input(self, prompt, input_type=float, max_attempts=3, attempt=1):
        if attempt > max_attempts:
            raise ValueError("Превышено количество попыток ввода")
        try:
            value = input_type(input(prompt))
            return value
        except ValueError:
            print(f"Ошибка! Требуется ввести число ({input_type.__name__}). Попытка {attempt}/{max_attempts}")
            return self.get_valid_input(prompt, input_type, max_attempts, attempt + 1)
    def degrees_to_dms(self, degrees):
        #Конвертирует градусы в кортеж (градусы, минуты, секунды)
        d = int(degrees)
        remainder = (degrees - d) * 60
        m = int(remainder)
        s = round((remainder - m) * 60, 2)
        return (d, m, s)  # Возвращаем кортеж
    def direct_problem(self):
        print("\nРешение прямой геодезической задачи")
        try:
            x1 = float(input("Введите координату x1 первой точки: "))
            y1 = float(input("Введите координату y1 первой точки: "))
            alpha_deg = float(input("Введите дирекционный угол α в градусах: "))
            L = float(input("Введите расстояние L между точками: "))
            if L < 0:
                print("ошибка: расстояние не может быть меньше нуля")
                return self.direct_problem()
            alpha_rad = math.radians(alpha_deg)
            delta_x = L * math.cos(alpha_rad)
            delta_y = L * math.sin(alpha_rad)
            x2 = x1 + delta_x
            y2 = y1 + delta_y
            # Сохраняем точку в словарь
            point_id = f"P{len(self.points) + 1}"
            self.points[point_id] = (x2, y2)
            result = (f"Координаты второй точки:\n"
                      f"x2 = {x2:.3f}\n"
                      f"y2 = {y2:.3f}\n"
                      f"Приращения координат:\n"
                      f"Δx = {delta_x:.3f}\n"
                      f"Δy = {delta_y:.3f}\n"
                      f"Точка сохранена под ID: {point_id}")
            print("\n" + result)
            self.save_to_file(
                f"Прямая задача:\n"
                f"Исходные данные: x1={x1}, y1={y1}, α={alpha_deg}°, L={L}\n"
                f"Результат: x2={x2:.3f}, y2={y2:.3f}, ID={point_id}"
            )
            return (x2, y2, point_id)  # Возвращаем кортеж
        except ValueError as e:
            print(f"Ошибка ввода данных: {e}")
            return None
    def inverse_problem(self):
        print("\nРешение обратной геодезической задачи")
        try:
            x1 = float(input("Введите координату x1 первой точки: "))
            y1 = float(input("Введите координату y1 первой точки: "))
            x2 = float(input("Введите координату x2 второй точки: "))
            y2 = float(input("Введите координату y2 второй точки: "))
            delta_x = x2 - x1
            delta_y = y2 - y1
            if delta_x == 0 and delta_y == 0:
                print("точки совпадают")
                return self.inverse_problem()
            L = math.hypot(delta_x, delta_y)
            alpha_rad = math.atan2(delta_y, delta_x)
            alpha = math.degrees(alpha_rad) % 360
            dms = self.degrees_to_dms(alpha)  # Получаем кортеж (d, m, s)
            result = (f"Расстояние между точками: L = {L:.3f}\n"
                      f"Дирекционный угол: {dms[0]}° {dms[1]}' {dms[2]}\"\n"
                      f"Приращения координат:\n"
                      f"Δx = {delta_x:.3f}\n"
                      f"Δy = {delta_y:.3f}")
            print("\n" + result)
            self.save_to_file(
                f"Обратная задача:\n"
                f"Точка 1: ({x1}, {y1})\n"
                f"Точка 2: ({x2}, {y2})\n"
                f"Результат: L={L:.3f}, α={alpha:.6f}°"
            )
            return (L, alpha, dms)  # Возвращаем кортеж
        except ValueError as e:
            print(f"Ошибка ввода данных: {e}")
            return None
    def show_points(self): #вывод сохр точек из словаря points
        if not self.points:
            print("Нет сохраненных точек")
            return
        print("\nСохраненные точки:")
        for point_id, coords in self.points.items():
            print(f"{point_id}: x={coords[0]:.3f}, y={coords[1]:.3f}")
    def show_history(self):
        if not self.history:
            print("История операций пуста")
            return
        print("\nПоследние 5 операций:")
        for record in self.history[-5:]:  # Берем последние 5 записей
            print(f"{record[0]}. {record[1]}")  # record - кортеж (id, timestamp, data)
            print(record[2][:50] + "...")
def main():
    calculator = GeodeticCalculator()
    menu_items = [
        "Решение прямой геодезической задачи",
        "Решение обратной геодезической задачи",
        "Показать сохраненные точки",
        "Показать историю операций",
        "Выход"
    ]
    while True:
        print("\nГлавное меню:")
        for i, item in enumerate(menu_items, 1):
            print(f"{i}. {item}")
        choice = input("Выберите действие (1-5): ").strip()
        if choice == '1':
            calculator.direct_problem()
        elif choice == '2':
            calculator.inverse_problem()
        elif choice == '3':
            calculator.show_points()
        elif choice == '4':
            calculator.show_history()
        elif choice == '5':
            print("Работа программы завершена.")
            break
        else:
            print("Некорректный ввод. Пожалуйста, выберите 1-5.")
if __name__ == "__main__":
    main()