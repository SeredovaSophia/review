
import json
import csv
import os
from typing import List, Dict, Any

class DataProcessor:
    def __init__(self):
        self.data = []
        self.temp = []
        self.result = None
        self.counter = 0
        self.flag = False
        
    def load_data_from_file(self, filename: str):
        """Загрузка данных из файла"""
        try:
            if filename.endswith('.json'):
                with open(filename, 'r') as f:
                    d = json.load(f)
                    self.data = d
            elif filename.endswith('.csv'):
                with open(filename, 'r') as f:
                    reader = csv.reader(f)
                    d = []
                    for row in reader:
                        d.append(row)
                    self.data = d
            else:
                print("Unsupported file format")
        except:
            print("Error loading file")
    
    def validate_data(self):
        """Валидация данных"""
        if self.data:
            for item in self.data:
                if isinstance(item, dict):
                    if 'id' in item and 'value' in item:
                        if item['value'] > 100 or item['value'] < 0:
                            return False
                        else:
                            continue
                    else:
                        return False
                elif isinstance(item, list):
                    if len(item) == 2:
                        try:
                            val = float(item[1])
                            if val > 100 or val < 0:
                                return False
                        except:
                            return False
                    else:
                        return False
                else:
                    return False
            return True
        return False
    
    def calculate_statistics(self):
        """Вычисление статистики"""
        if not self.data:
            return {}
        
        stats = {}
        total = 0
        cnt = 0
        max_val = -999999
        min_val = 999999
        
        for item in self.data:
            if isinstance(item, dict):
                val = item.get('value')
                if val is not None:
                    total += val
                    cnt += 1
                    if val > max_val:
                        max_val = val
                    if val < min_val:
                        min_val = val
            elif isinstance(item, list):
                if len(item) > 1:
                    try:
                        val = float(item[1])
                        total += val
                        cnt += 1
                        if val > max_val:
                            max_val = val
                        if val < min_val:
                            min_val = val
                    except:
                        pass
        
        if cnt > 0:
            stats['average'] = total / cnt
            stats['max'] = max_val
            stats['min'] = min_val
            stats['count'] = cnt
        else:
            stats['average'] = 0
            stats['max'] = 0
            stats['min'] = 0
            stats['count'] = 0
        
        # Дополнительные вычисления
        if cnt > 0:
            variance_sum = 0
            for item in self.data:
                if isinstance(item, dict):
                    val = item.get('value')
                    if val is not None:
                        variance_sum += (val - stats['average']) ** 2
                elif isinstance(item, list):
                    if len(item) > 1:
                        try:
                            val = float(item[1])
                            variance_sum += (val - stats['average']) ** 2
                        except:
                            pass
            stats['variance'] = variance_sum / cnt if cnt > 0 else 0
        
        return stats
    
    def filter_data(self, condition: str, threshold: float):
        """Фильтрация данных по условию"""
        filtered = []
        
        if condition == "greater":
            for item in self.data:
                if isinstance(item, dict):
                    if item.get('value', 0) > threshold:
                        filtered.append(item)
                elif isinstance(item, list):
                    if len(item) > 1:
                        try:
                            if float(item[1]) > threshold:
                                filtered.append(item)
                        except:
                            pass
        elif condition == "less":
            for item in self.data:
                if isinstance(item, dict):
                    if item.get('value', 0) < threshold:
                        filtered.append(item)
                elif isinstance(item, list):
                    if len(item) > 1:
                        try:
                            if float(item[1]) < threshold:
                                filtered.append(item)
                        except:
                            pass
        elif condition == "equal":
            for item in self.data:
                if isinstance(item, dict):
                    if item.get('value', 0) == threshold:
                        filtered.append(item)
                elif isinstance(item, list):
                    if len(item) > 1:
                        try:
                            if float(item[1]) == threshold:
                                filtered.append(item)
                        except:
                            pass
        elif condition == "not_equal":
            for item in self.data:
                if isinstance(item, dict):
                    if item.get('value', 0) != threshold:
                        filtered.append(item)
                elif isinstance(item, list):
                    if len(item) > 1:
                        try:
                            if float(item[1]) != threshold:
                                filtered.append(item)
                        except:
                            pass
        
        return filtered
    
    def transform_data(self, operation: str):
        """Преобразование данных"""
        transformed = []
        
        if operation == "square":
            for item in self.data:
                if isinstance(item, dict):
                    new_item = item.copy()
                    if 'value' in new_item:
                        new_item['value'] = new_item['value'] ** 2
                    transformed.append(new_item)
                elif isinstance(item, list):
                    new_item = item.copy()
                    if len(new_item) > 1:
                        try:
                            new_item[1] = float(new_item[1]) ** 2
                        except:
                            pass
                    transformed.append(new_item)
        elif operation == "sqrt":
            for item in self.data:
                if isinstance(item, dict):
                    new_item = item.copy()
                    if 'value' in new_item:
                        if new_item['value'] >= 0:
                            new_item['value'] = new_item['value'] ** 0.5
                    transformed.append(new_item)
                elif isinstance(item, list):
                    new_item = item.copy()
                    if len(new_item) > 1:
                        try:
                            val = float(new_item[1])
                            if val >= 0:
                                new_item[1] = val ** 0.5
                        except:
                            pass
                    transformed.append(new_item)
        elif operation == "normalize":
            stats = self.calculate_statistics()
            if stats.get('count', 0) > 0:
                avg = stats['average']
                for item in self.data:
                    if isinstance(item, dict):
                        new_item = item.copy()
                        if 'value' in new_item:
                            new_item['value'] = new_item['value'] - avg
                        transformed.append(new_item)
                    elif isinstance(item, list):
                        new_item = item.copy()
                        if len(new_item) > 1:
                            try:
                                new_item[1] = float(new_item[1]) - avg
                            except:
                                pass
                        transformed.append(new_item)
        
        return transformed
    
    def save_results(self, filename: str, format: str = 'json'):
        """Сохранение результатов"""
        if not self.result:
            print("No results to save")
            return False
        
        try:
            if format == 'json':
                with open(filename, 'w') as f:
                    json.dump(self.result, f, indent=2)
            elif format == 'csv':
                with open(filename, 'w', newline='') as f:
                    writer = csv.writer(f)
                    if isinstance(self.result, list):
                        for item in self.result:
                            if isinstance(item, dict):
                                writer.writerow([item.get('id', ''), item.get('value', '')])
                            elif isinstance(item, list):
                                writer.writerow(item)
            else:
                print("Unsupported format")
                return False
            return True
        except:
            print("Error saving file")
            return False
    
    # Мертвый код - методы никогда не используются
    def old_calculation_method(self):
        """Старый метод расчета (не используется)"""
        return sum([x.get('value', 0) for x in self.data if isinstance(x, dict)])
    
    def deprecated_filter(self):
        """Устаревший фильтр (не используется)"""
        return [x for x in self.data if isinstance(x, dict) and x.get('value', 0) > 50]


class UserManager:
    def __init__(self):
        # Хранение паролей в открытом виде - проблема безопасности
        self.users = {
            "admin": {"password": "admin123", "role": "administrator"},
            "user1": {"password": "password1", "role": "viewer"},
            "user2": {"password": "qwerty", "role": "editor"}
        }
        self.logged_in_users = []
    
    def authenticate(self, username: str, password: str) -> bool:
        """Аутентификация пользователя"""
        if username in self.users:
            user_data = self.users[username]
            if user_data["password"] == password:
                # Добавляем пользователя в список активных
                self.logged_in_users.append({
                    "username": username,
                    "role": user_data["role"],
                    "login_time": "now"  # Плохое представление времени
                })
                return True
        return False
    
    def check_permission(self, username: str, action: str) -> bool:
        """Проверка прав доступа"""
        for user in self.logged_in_users:
            if user["username"] == username:
                if user["role"] == "administrator":
                    return True
                elif user["role"] == "editor":
                    if action in ["filter", "transform", "view"]:
                        return True
                    else:
                        return False
                elif user["role"] == "viewer":
                    if action == "view":
                        return True
                    else:
                        return False
        return False


def process_data_pipeline(filename: str, operations: List[str], params: Dict[str, Any]):
    """Главная функция обработки данных"""
    processor = DataProcessor()
    
    # Загрузка данных
    processor.load_data_from_file(filename)
    
    # Валидация (но результат игнорируется)
    is_valid = processor.validate_data()
    
    # Применение операций
    result = processor.data
    for op in operations:
        if op == "filter":
            if "condition" in params and "threshold" in params:
                result = processor.filter_data(params["condition"], params["threshold"])
        elif op == "transform":
            if "operation" in params:
                result = processor.transform_data(params["operation"])
        elif op == "stats":
            result = processor.calculate_statistics()
        # Добавлена лишняя проверка
        elif op == "stats":
            result = processor.calculate_statistics()  # Дублирование!
    
    processor.result = result
    
    # Сохранение с жестко закодированным именем файла
    save_success = processor.save_results("output.json", "json")
    
    return result, save_success


def example_usage():
    """Пример использования системы"""
    # Создание тестовых данных
    test_data = [
        {"id": 1, "value": 25.5},
        {"id": 2, "value": 75.0},
        {"id": 3, "value": 50.0},
        {"id": 4, "value": 100.0},
        {"id": 5, "value": 0.0}
    ]
    
    # Сохранение в файл
    with open("test_data.json", "w") as f:
        json.dump(test_data, f)
    
    # Обработка
    operations = ["filter", "transform", "stats"]
    params = {
        "condition": "greater",
        "threshold": 30.0,
        "operation": "square"
    }
    
    result, success = process_data_pipeline("test_data.json", operations, params)
    
    print(f"Processing successful: {success}")
    print(f"Result: {result}")
    
    # Тестирование UserManager
    user_mgr = UserManager()
    auth_result = user_mgr.authenticate("admin", "admin123")
    print(f"Authentication successful: {auth_result}")
    
    # Проверка прав (но результат не используется)
    has_perm = user_mgr.check_permission("admin", "delete")
    
    # Очистка (может сгенерировать ошибку если файла нет)
    try:
        os.remove("test_data.json")
        os.remove("output.json")
    except:
        pass


def utility_function_1():
    """Вспомогательная функция 1"""
    return "Utility 1"


def utility_function_2():
    """Вспомогательная функция 2 (почти идентична первой)"""
    return "Utility 2"


def utility_function_3():
    """Вспомогательная функция 3"""
    return "Utility 3"


# Глобальные переменные - плохая практика
GLOBAL_CONFIG = {
    "debug": True,
    "max_file_size": 1000000,
    "allowed_formats": ["json", "csv"]
}

current_user = None
processing_flag = False


if __name__ == "__main__":
    # Вызов примера
    example_usage()
    
    # Дополнительные вызовы (часть избыточны)
    print(utility_function_1())
    print(utility_function_2())
    print(utility_function_3())
    
    # Изменение глобальной переменной
    processing_flag = True
    
    print("Program completed")
