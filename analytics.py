# Импортируем стек категорий, чтобы получить данные о категориях расходов
from core import get_categories

def find_day_max_expense(expenses):
    """
    Найти день с максимальной суммой расходов с помощью линейного поиска по списку расходов.
    Параметры:
        expenses (list): список сумм расходов по дням (индекс 0 = день 1)
    Возвращает:
        tuple или None: (номер дня, максимальная сумма) или None, если расходов нет
    """
    # Проверяем, есть ли данные о расходах
    if not expenses:
        return None

    # Проверяем, все ли дни имеют нулевые расходы
    if all(x == 0 for x in expenses):
        return None

    # Находим максимальную сумму и её индекс
    max_sum = max(expenses)
    max_day = expenses.index(max_sum) + 1

    return max_day, max_sum

def aggregate_by_category():
    """
    Собрать суммы расходов по категориям.
    Использует данные из categories_stack.
    Возвращает:
        dict: словарь {категория: общая сумма}
    """
    # Получаем стек с категориями всех расходов
    categories = get_categories()
    result = {}

    # Проходимся по каждому расходу с помощью цикла и суммируем по категориям
    for item in categories:
        cat = item['category']
        amount = item['amount']
        result[cat] = result.get(cat, 0) + amount # возвращает текущую сумму для категории или 0, если категория новая

    return result

def sort_categories_insertion(category_dict):
    """
    Отсортировать категории по сумме трат с помощью сортировки вставками.
    Сортировка по убыванию суммы.
    Параметры:
        category_dict: словарь {категория: сумма}
    Возвращает:
        list: список кортежей, отсортированный по убыванию
    """
    # Если словарь пустой, возвращаем пустой список
    if not category_dict:
        return []

    # Преобразуем словарь в список кортежей
    items = list(category_dict.items())

    # Сортировка вставками по убыванию суммы (со второго элемента)
    for i in range(1, len(items)):
        # Запоминаем текущий элемент (категорию и сумму)
        key_cat, key_amount = items[i]
        # Сравниваем с предыдущим элементом
        j = i - 1

        # Сдвигаем элементы вправо, пока они меньше, чем key_amount (сортируем по убыванию)
        while j >= 0 and items[j][1] < key_amount:
            items[j + 1] = items[j]
            j -= 1

        # Вставляем элемент, который запоминали, в правильную позицию
        items[j + 1] = (key_cat, key_amount)

    return items

def build_expense_tree(expenses):
    """
    Представить дерево трат в форме строки.
    Структура дерева:
        Месяц (корень) - День N (сумма руб.) - Категория (сумма руб.)
    Параметры:
        expenses (list): список сумм расходов по дням
    Возвращает:
        str: дерево трат в виде строки
    """
    # Проверяем, есть ли расходы (расходов нет, если пустой список или все нули)
    if not expenses or all(x == 0 for x in expenses):
        return "Дерево пусто, расходов нет"

    # Получаем стек с категориями всех расходов
    categories = get_categories()

    # Группируем категории по дням
    cats_by_day = {} # создаем пустой словарь для группировки категорий по дням
    for item in categories: # проходим по каждому расходу из стека категорий
        day = item['day'] # получаем номер дня расхода
        # Если дня ещё нет в словаре, создаём для него пустой список
        if day not in cats_by_day:
            cats_by_day[day] = []
        # Добавляем текущий расход в список категорий этого дня
        cats_by_day[day].append(item)

    result = "Месяц\n" # строим дерево, начиная с корня

    for day_idx, day_sum in enumerate(expenses): # проходимся по всем дням
        if day_sum == 0: # пропускаем дни без расходов
            continue

        day_num = day_idx + 1
        # Добавляем ветку дня
        result += f"День {day_num}: {day_sum} руб.\n"

        # Если у этого дня есть категории, добавляем их, как листья
        if day_num in cats_by_day:
            for exp in cats_by_day[day_num]:
                result += f"    -- {exp['category']}: {exp['amount']} руб.\n"

    return result
