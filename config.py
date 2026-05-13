DATABASE_NAME = 'home_inventory.db'


WINDOW_TITLE = "Домашний учёт материалов"
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 500

COLORS = {
    'title': 'darkblue',
    'add_button': '#4CAF50',      # Зеленый
    'update_button': '#2196F3',   # Синий
    'delete_button': '#f44336',   # Красный
    'clear_button': '#FF9800',    # Оранжевый
    'income_button': '#4CAF50',   # Зеленый
    'expense_button': '#FF5722',  # Оранжево-красный
    'info_text': 'gray'
}

FONTS = {
    'title': ('Arial', 14, 'bold'),
    'label': ('Arial', 10),
    'label_bold': ('Arial', 10, 'bold'),
    'entry': ('Arial', 10),
    'button': ('Arial', 10, 'bold'),
    'button_small': ('Arial', 9),
    'info': ('Arial', 10, 'italic')
}

DEFAULT_UNIT = "шт."
LOW_STOCK_THRESHOLD = 5

UI_TEXTS = {
    'title': "📦 ДОМАШНИЙ УЧЁТ МАТЕРИАЛОВ",
    'input_frame': "Добавить или изменить материал",
    'operation_frame': "Быстрые операции с количеством",
    'name_label': "Название:",
    'unit_label': "Ед. изм:",
    'quantity_label': "Кол-во:",
    'note_label': "Примечание:",
    'search_label': "🔍 Поиск:",
    'add_btn': "➕ Добавить",
    'update_btn': "✏️ Изменить",
    'delete_btn': "🗑️ Удалить",
    'clear_btn': "🧹 Очистить поля",
    'income_btn': "📥 Приход (+)",
    'expense_btn': "📤 Расход (-)",
    'refresh_btn': "🔄 Обновить"
}

TABLE_COLUMNS = {
    'name': '📋 Название',
    'quantity': '📊 Количество',
    'unit': '📏 Ед. изм.',
    'note': '📝 Примечание'
}

ERROR_MESSAGES = {
    'empty_name': "Введите название материала!",
    'invalid_quantity': "Количество должно быть целым числом!",
    'positive_quantity': "Введите положительное число!",
    'select_material': "Выберите материал!",
    'not_enough': "Недостаточно материала! В наличии: {}",
    'already_exists': "Материал с названием '{}' уже существует!",
    'low_stock': "Материала '{}' осталось мало: {} ед.!"
}

SUCCESS_MESSAGES = {
    'added': "Материал '{}' добавлен!",
    'updated': "Материал '{}' обновлен!",
    'deleted': "Материал '{}' удален!",
    'income': "Добавлено {} единиц к '{}'!",
    'expense': "Списано {} единиц из '{}'!"
}