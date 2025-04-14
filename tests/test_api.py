import pytest
import requests

# Фикстура для создания и удаления стола
@pytest.fixture
def create_table():
    # Создание стола
    response = requests.post("http://localhost:8000/tables/", json={
        "name": "тестовое имя",
        "seats": 1,
        "location": "тестовая локация"
    })
    assert response.status_code == 200
    table_id = response.json()['id']
    yield table_id
    # Удаление созданного стола после тестов
    requests.delete(f"http://localhost:8000/tables/{table_id}")

# Фикстура для создания и удаления резерва
@pytest.fixture
def create_reservation():
    # Создание резерва
    response = requests.post("http://localhost:8000/reservations/", json={
        "customer_name": "Тестовый гость",
        "table_id": 9,
        "reservation_time": "2025-09-13T20:19:56.547Z",
        "duration_minutes": 15
    })
    assert response.status_code == 200
    reservation_id = response.json()['id']
    yield reservation_id
    # Удаление созданного резерва после тестов
    requests.delete(f"http://localhost:8000/reservations/{reservation_id}")

def test_get_tables():
    """
    Получить все столы
    """
    response = requests.get("http://localhost:8000/tables/")
    assert response.status_code == 200

def test_delete_table(create_table):
    """
    Удалить стол по id
    """
    # Используемая фикстура автоматически создаёт и предоставляет id стола
    table_id = create_table
    # Удаляем созданный стол
    response = requests.delete(f"http://localhost:8000/tables/{table_id}")
    assert response.status_code == 200  # Успешное удаление

def test_get_reservations():
    """
    Получить все резервы
    """
    response = requests.get("http://localhost:8000/reservations/")
    assert response.status_code == 200

def test_delete_reservation(create_reservation):
    """
    Удаление резерва
    """
    # Используемая фикстура автоматически создаёт и предоставляет id резерва
    reservation_id = create_reservation
    # Удаляем созданную бронь
    response = requests.delete(f"http://localhost:8000/reservations/{reservation_id}")
    assert response.status_code == 200  # Успешное удаление

def test_time_reservation(create_table):
    """
    Проверить, если в указанный временной слот столик уже занят
    """
    table_id = create_table

    # Создаём основную бронь
    response = requests.post("http://localhost:8000/reservations/", json={
        "customer_name": "Тестовый гость 1",
        "table_id": table_id,
        "reservation_time": "2025-09-13T20:19:56.547Z",
        "duration_minutes": 15
    })
    assert response.status_code == 200
    reservation_id = response.json()['id']

    # Попытка создать бронь на то же время и тот же стол
    response2 = requests.post("http://localhost:8000/reservations/", json={
        "customer_name": "Тестовый гость 2",
        "table_id": table_id,
        "reservation_time": "2025-09-13T20:19:56.547Z",
        "duration_minutes": 10
    })
    assert response2.status_code == 400  # Ожидаемое поведение: резервирование невозможно

    # Удаление тестовой брони после теста
    requests.delete(f"http://localhost:8000/reservations/{reservation_id}")




