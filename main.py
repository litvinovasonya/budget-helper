# Импортируем функции из модулей core.py, analytics.py
from core import add_expense, get_sum_between, undo_last, get_categories
from analytics import find_day_max_expense, aggregate_by_category, sort_categories_insertion, build_expense_tree
def main():
    """
    Главная функция программы.
    Запускает бесконечный цикл меню.
    """
    # Создаём пустой список для хранения расходов по дням
    expenses = []
    # Создаём пустой стек для отмены операций
    undo_stack = []

    # Бесконечный цикл меню
    while True:
        # Выводим текущие расходы
        if expenses:
            print("\nТекущие расходы по дням:")
            # Перебираем все дни, у которых есть расходы
            for i in range(len(expenses)):
                if expenses[i] > 0:  # показываем только ненулевые расходы
                    print(f"  День {i + 1}: {expenses[i]} руб.")
        else:
            print("\n(расходов нет)")

        # Выводим меню с вариантами выбора
        print("  1. Добавить расход")
        print("  2. Сумма за период")
        print("  3. День с максимальной тратой")
        print("  4. Топ категорий")
        print("  5. Дерево трат")
        print("  6. Отменить последнее действие")
        print("  7. Выход")

        # Запрашиваем выбор пользователя
        choice = input("Ваш выбор (1-7): ").strip()

        # Обработка выбора 1: Добавить расход
        if choice == "1":
            print("\nДобавление расхода")
            # Запрашиваем номер дня (1-31)
            while True:
                try:
                    day = int(input("Номер дня (1-31): "))
                    # Проверяем, что день в допустимом диапазоне
                    if 1 <= day <= 31:
                        break  # выходим из цикла, если день корректен
                    else:
                        print("Ошибка: день должен быть от 1 до 31")
                except ValueError:
                    print("Ошибка: введите целое число!")

            # Запрашиваем сумму расхода
            while True:
                try:
                    amount = float(input("Сумма расхода (руб): "))
                    # Проверяем, что сумма положительная
                    if amount > 0:
                        break
                    else:
                        print("Ошибка: сумма должна быть больше 0")
                except ValueError:
                    print("Ошибка: введите число")

            # Запрашиваем категорию расхода
            category = input("Категория: ").strip()
            # Если категория не введена, ставим "прочее"
            if not category:
                category = "прочее"

            # Вызываем функцию добавления расхода из core.py
            add_expense(expenses, undo_stack, day, amount, category)
            # Подтверждаем добавление
            print(f"\nРасход {amount} руб. (категория: {category}) добавлен за день {day}")

        # Обработка выбора 2: Сумма за период
        elif choice == "2":
            print("\nСумма за период")
            # Проверяем, есть ли расходы
            if not expenses:
                print("Нет данных о расходах. Сначала добавьте расходы")
                continue  # возвращаемся в начало цикла

            # Запрашиваем начальный день периода
            while True:
                try:
                    day_a = int(input("Начальный день: "))
                    # Проверяем, что день не меньше 1
                    if day_a >= 1:
                        break
                    else:
                        print("Ошибка: день должен быть >= 1")
                except ValueError:
                    print("Ошибка: введите целое число")


            # Запрашиваем конечный день периода
            while True:
                try:
                    day_b = int(input("Конечный день: "))
                    # Проверяем, что день не меньше начального
                    if day_b >= day_a:
                        break
                    else:
                        print("Ошибка: конечный день должен быть >= начального")
                except ValueError:
                    print("Ошибка: введите целое число")

            # Вызываем функцию получения суммы за период из core.py
            total = get_sum_between(expenses, day_a, day_b)
            # Выводим результат
            print(f"\nСумма расходов с дня {day_a} по день {day_b}: {total} руб.")

        # Обработка выбора 3: День с максимальной тратой
        elif choice == "3":
            print("\nДень с максимальной тратой")
            result = find_day_max_expense(expenses)
            if result is None:
                print("Нет данных о расходах")
            else:
                day, amount = result
                print(f"День {day}: {amount} руб.")

        # Обработка выбора 4: Топ категорий
        elif choice == "4":
            print("\nТоп категорий по сумме трат")
            cat_dict = aggregate_by_category()
            if not cat_dict:
                print("Нет данных о расходах")
            else:
                sorted_cats = sort_categories_insertion(cat_dict)
                for cat, total in sorted_cats:
                    print(f"{cat}: {total} руб.")

        # Обработка выбора 5: Дерево трат
        elif choice == "5":
            print("\nДерево трат")
            tree = build_expense_tree(expenses)
            print(tree)

        # Обработка выбора 6: Отмена последнего действия
        elif choice == "6":
            print("\nОтмена последнего действия")
            success = undo_last(expenses, undo_stack)
            if success:
                print("Последнее добавление расхода отменено")
            else:
                print("Нечего отменять")

        # Обработка выбора 7: Выход
        elif choice == "7":
            print("\nПрограмма завершена")
            break

        # Обработка ошибки (неверного выбора)
        else:
            print("\nТакого варианта нет. Введите число от 1 до 7")

if __name__ == "__main__":
    main()
