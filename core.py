# Стек для хранения категорий каждого расхода
categories_stack = []

def add_expense(expenses, undo_stack, day, amount, category):
    """
    Добавить расход за день.
    Сохраняет предыдущее состояние в стек отмены.
    Параметры:
    - expenses: список расходов
    - undo_stack: стек для отмены операций
    - day: номер дня
    - amount: сумма расхода
    - category: категория расхода
    """
    # Проверяем, что день в допустимом диапазоне (1-31)
    if day < 1 or day > 31:
        raise ValueError("День должен быть от 1 до 31")

    # Сохраняем информацию для отмены в стек
    # Для каждого добавления запоминаем день и сумму, которая была до добавления
    undo_stack.append({
        'day': day,  # номер дня
        'previous_amount': expenses[day - 1] if day <= len(expenses) else 0,  # старая сумма (если день существовал)
    })

    # Расширяем список расходов, если день выходит за текущую границу
    while len(expenses) < day:
        expenses.append(0)  # добавляем нули для отсутствующих дней

    # Добавляем сумму к уже существующему расходу за этот день
    expenses[day - 1] += amount
    categories_stack.append({
        'day': day,
        'amount': amount,
        'category': category
    })
    return True

def build_prefix_sum(expenses):
    """
    Построить массив префиксных сумм на основе списка расходов.
    prefix[i] = сумма расходов с 1 по i день.
    """
    # Получаем количество дней, по которым есть расходы
    n = len(expenses)
    # Создаём массив префиксных сумм размером n+1
    # prefix[0] всегда 0 (сумма за 0 дней)
    prefix = [0] * (n + 1)
    # Заполняем массив префиксных сумм
    for i in range(1, n + 1):
        prefix[i] = prefix[i - 1] + expenses[i - 1]
    return prefix

def get_sum_between(expenses, day_a, day_b):
    """
    Сумма расходов за период с day_a по day_b (включительно).
    Использует префиксные суммы для O(1) ответа.
    """

    # Проверка на некорректный ввод диапазона
    if day_a < 1 or day_a > day_b:
        return 0

    # Если день b больше длины списка, то считаем дни до конца списка
    actual_day_b = min(day_b, len(expenses))

    prefix = build_prefix_sum(expenses)
    return prefix[actual_day_b] - prefix[day_a - 1]


def undo_last(expenses, undo_stack):
    """
    Отменить последнее добавление расхода.
    Восстанавливает предыдущую сумму за день.
    Возвращает True, если отмена успешна, иначе False.
    """
    # Проверяем, есть ли что отменять
    if not undo_stack:
        return False  # стек пуст, нечего отменять

    # Извлекаем последнюю операцию из стека
    last = undo_stack.pop()
    # Вычисляем индекс в списке
    day_index = last['day'] - 1

    # Отменяем последнюю категорию
    if categories_stack:
        categories_stack.pop()

    # Восстанавливаем предыдущую сумму за этот день
    if day_index < len(expenses):
        expenses[day_index] = last['previous_amount']
        # Если последний день стал нулевым, удаляем хвостовые нули
        if expenses[day_index] == 0 and day_index == len(expenses) - 1:
            # Удаляем нули с конца, пока последний элемент не станет ненулевым
            while len(expenses) > 0 and expenses[-1] == 0:
                expenses.pop()
    return True

def get_categories():
    return categories_stack
