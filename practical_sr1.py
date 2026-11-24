"""Консольна програма для самостійної роботи №1."""

from __future__ import annotations

import math
import sys
from collections.abc import Iterator, Iterable


def factorial(number: int) -> int:
    """Повертає факторіал невід'ємного цілого числа через цикл for."""
    if isinstance(number, bool) or not isinstance(number, int):
        raise TypeError("Факторіал можна обчислити лише для цілого числа.")
    if number < 0:
        raise ValueError("Число для факторіалу не може бути від'ємним.")

    result = 1
    for value in range(2, number + 1):
        result *= value
    return result


def _is_finite_number(value: int | float) -> bool:
    """Перевіряє число, зокрема обробляючи надто великі цілі значення."""
    try:
        return math.isfinite(float(value))
    except OverflowError:
        return False


def circle_area(radius: float) -> float:
    """Обчислює площу круга за його радіусом."""
    if isinstance(radius, bool) or not isinstance(radius, (int, float)):
        raise TypeError("Радіус має бути числом.")
    if not _is_finite_number(radius) or radius < 0:
        raise ValueError("Радіус має бути скінченним невід'ємним числом.")
    try:
        area = math.pi * radius**2
    except OverflowError as error:
        raise ValueError("Площа круга завелика для подання числом із плаваючою крапкою.") from error
    if not math.isfinite(area):
        raise ValueError("Площа круга завелика для подання числом із плаваючою крапкою.")
    return area


def triangle_properties(a: float, b: float, c: float) -> dict[str, float | str]:
    """Повертає вид трикутника та його площу за формулою Герона."""
    sides = (a, b, c)
    if any(isinstance(side, bool) or not isinstance(side, (int, float)) for side in sides):
        raise TypeError("Довжини сторін мають бути числами.")
    if any(not _is_finite_number(side) or side <= 0 for side in sides):
        raise ValueError("Довжини сторін мають бути скінченними додатними числами.")

    x, y, z = sorted(sides)
    if x + y <= z:
        raise ValueError("Такі сторони не утворюють трикутник.")

    equal_ab = math.isclose(a, b, rel_tol=1e-9)
    equal_bc = math.isclose(b, c, rel_tol=1e-9)
    equal_ac = math.isclose(a, c, rel_tol=1e-9)
    if equal_ab and equal_bc:
        side_kind = "рівносторонній"
    elif equal_ab or equal_bc or equal_ac:
        side_kind = "рівнобедрений"
    else:
        side_kind = "різносторонній"

    # Нормалізація сторін перед піднесенням до квадрата запобігає переповненню.
    scale = z
    x_scaled, y_scaled, z_scaled = x / scale, y / scale, z / scale
    small_square_sum = x_scaled**2 + y_scaled**2
    large_square = z_scaled**2
    if math.isclose(small_square_sum, large_square, rel_tol=1e-9):
        angle_kind = "прямокутний"
    elif small_square_sum > large_square:
        angle_kind = "гострокутний"
    else:
        angle_kind = "тупокутний"

    # Формула Герона у масштабованих координатах працює для широкого діапазону сторін.
    semi_scaled = (x_scaled + y_scaled + z_scaled) / 2
    area_scaled = math.sqrt(
        max(0.0, semi_scaled * (semi_scaled - x_scaled)
            * (semi_scaled - y_scaled) * (semi_scaled - z_scaled))
    )
    area = area_scaled * scale * scale
    if not math.isfinite(area):
        raise ValueError("Площа трикутника завелика для подання числом із плаваючою крапкою.")

    return {"за сторонами": side_kind, "за кутами": angle_kind, "площа": area}


class CountdownIterator(Iterator[int]):
    """Власний ітератор, який послідовно повертає числа від start до 1."""

    def __init__(self, start: int) -> None:
        if isinstance(start, bool) or not isinstance(start, int):
            raise TypeError("Початкове значення має бути цілим числом.")
        if start < 0:
            raise ValueError("Початкове значення не може бути від'ємним.")
        self.current = start

    def __iter__(self) -> CountdownIterator:
        return self

    def __next__(self) -> int:
        if self.current == 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value


def square_values(values: Iterable[int]) -> Iterator[int]:
    """Генерує квадрати значень, не створюючи проміжного списку."""
    for value in values:
        yield value**2


def show_data_structures() -> None:
    """Демонструє список, кортеж і словник та типові операції з ними."""
    numbers = [2, 4, 6]
    numbers.append(8)
    point = (3, 5)
    concepts = {"список": "змінювана послідовність", "кортеж": "незмінна послідовність"}

    print("Список:", numbers, "| перший елемент:", numbers[0])
    print("Кортеж:", point, "| координата x:", point[0])
    print("Словник:", concepts, "| значення за ключем:", concepts["список"])
    print("Сума чисел у списку:", sum(numbers))


def show_iteration_and_generators() -> None:
    """Показує вбудований і власний ітератори та функцію-генератор."""
    values = (2, 4, 6)
    built_in_iterator = iter(values)
    print("Кортеж для обходу:", values)
    print("Перші два значення через next():", next(built_in_iterator), next(built_in_iterator))
    print("Залишок ітератора:", list(built_in_iterator))
    try:
        next(built_in_iterator)
    except StopIteration:
        print("Після завершення next(): StopIteration")

    custom_iterator = CountdownIterator(3)
    print("Власний CountdownIterator:", list(custom_iterator))

    generated_squares = square_values(values)
    print("Тип генератора:", type(generated_squares).__name__)
    print("Перший квадрат через next():", next(generated_squares))
    print("Решта квадратів:", list(generated_squares))
    try:
        next(generated_squares)
    except StopIteration:
        print("Після обходу генератора next(): StopIteration")


def read_integer(prompt: str) -> int:
    """Запитує ціле число й повторює запит після помилкового введення."""
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("Помилка: введіть ціле число.")


def read_finite_float(prompt: str, *, allow_zero: bool = False) -> float:
    """Запитує скінченне число, додатне або невід'ємне за allow_zero."""
    while True:
        try:
            value = float(input(prompt).strip())
            valid_sign = value >= 0 if allow_zero else value > 0
            if math.isfinite(value) and valid_sign:
                return value
            qualifier = "невід'ємне" if allow_zero else "додатне"
            print(f"Помилка: введіть скінченне {qualifier} число.")
        except ValueError:
            print("Помилка: введіть число, наприклад 3 або 2.5.")


def run_factorial() -> None:
    number = read_integer("Введіть невід'ємне ціле число: ")
    try:
        print(f"{number}! = {factorial(number)}")
    except ValueError as error:
        print("Помилка:", error)


def run_triangle() -> None:
    a = read_finite_float("Сторона a: ")
    b = read_finite_float("Сторона b: ")
    c = read_finite_float("Сторона c: ")
    try:
        result = triangle_properties(a, b, c)
        print(f"Трикутник {result['за сторонами']}, {result['за кутами']}.")
        print(f"Площа: {result['площа']:.4f}")
    except ValueError as error:
        print("Помилка:", error)


def run_circle() -> None:
    radius = read_finite_float("Радіус круга: ", allow_zero=True)
    print(f"Площа круга: {circle_area(radius):.4f}")


def run_menu() -> None:
    """Основний цикл консольного меню; команда 0 завершує програму."""
    actions = {
        1: run_factorial,
        2: run_triangle,
        3: run_circle,
        4: show_data_structures,
        5: show_iteration_and_generators,
    }
    while True:
        print("\n=== Головне меню ===")
        print("1 — факторіал; 2 — трикутник; 3 — площа круга")
        print("4 — структури даних; 5 — ітератори й генератори; 0 — вихід")
        choice = read_integer("Ваш вибір: ")
        if choice == 0:
            print("Роботу програми завершено.")
            break
        action = actions.get(choice)
        if action is None:
            print("Невідомий пункт меню. Введіть число від 0 до 5.")
            continue
        action()


def run_demo() -> None:
    """Виводить короткий відтворюваний приклад усіх можливостей програми."""
    print("=== Математичні обчислення ===")
    print("5! =", factorial(5))
    print("0! =", factorial(0))
    triangle = triangle_properties(3, 4, 5)
    print(
        "Трикутник 3, 4, 5:",
        f"{triangle['за сторонами']}, {triangle['за кутами']}, "
        f"площа = {triangle['площа']:.4f}",
    )
    print(f"Круг радіуса 2: площа = {circle_area(2):.4f}")

    print("\n=== Структури даних ===")
    show_data_structures()

    print("\n=== Ітератори та генератори ===")
    show_iteration_and_generators()

    print("\n=== Граничні випадки ===")
    print("0! =", factorial(0), "(добуток порожнього набору дорівнює 1)")
    print("Площа круга радіуса 0 =", circle_area(0))
    try:
        triangle_properties(1, 2, 3)
    except ValueError as error:
        print("Сторони 1, 2, 3:", error)
    try:
        factorial(-1)
    except ValueError as error:
        print("Факторіал -1:", error)


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        run_demo()
    elif len(sys.argv) > 1:
        print("Використання: python practical_sr1.py [--demo]")
        raise SystemExit(2)
    else:
        run_menu()


if __name__ == "__main__":
    main()
