import pytest
import requests



def test_get_table():
    """
    Получить все столы
    :return:
    """
    response = requests.get("http://127.0.0.1:8000/tables/")
    assert  response.status_code == 200

def test_delete_table():
    """
    Удалить стол по id
    :return:
    """
    # Создаём новый стол
    response = requests.post("http://localhost:8000/tables/", json={
        "name": "тестовое имя",
        "seats": 1,
        "location": "тестоваая локация"
    })
    assert response.status_code == 200

    # Получаем ID созданного стола из ответа
    created_table = response.json()
    table_id = created_table.get("id")
    assert table_id is not None, "Created table should have an ID"

    # Удаляем созданный стол
    delete_response = requests.delete(f"http://localhost:8000/tables/{table_id}")
    assert delete_response.status_code == 200  # Успешное удаление

def test_get_reservation():
    """
    Получить все резервы
    :return:
    """
    response = requests.get("http://127.0.0.1:8000/reservations/")
    assert  response.status_code == 200

def test_delete_reservation():
    """
    Удаление резерва
    :return:
    """
    # Создаём новую бронь
    response = requests.post("http://localhost:8000/reservations/", json={
        "customer_name": "Тестовый гость",
        "table_id": 9,
        "reservation_time": "2025-09-13T20:19:56.547Z",
        "duration_minutes": 15
    })
    assert response.status_code == 200

    # Получаем ID созданного стола из ответа
    created_reservation = response.json()
    reservation_id = created_reservation.get("id")
    assert reservation_id is not None, "Created reservation should have an ID"

    # Удаляем созданную бронь
    delete_response = requests.delete(f"http://localhost:8000/reservations/{reservation_id}")
    assert delete_response.status_code == 200  # Успешное удаление


def test_time_reservation():
    """
    Проверить, если в указанный временной слот столик уже занят
    :return:
    """
    # Создаём новую бронь
    response = requests.post("http://localhost:8000/reservations/", json={
        "customer_name": "Тестовый гость 1",
        "table_id": 9,
        "reservation_time": "2025-09-13T20:19:56.547Z",
        "duration_minutes": 15
    })
    assert response.status_code == 200
    # Создаём бронь на тоже время
    response2 = requests.post("http://localhost:8000/reservations/", json={
        "customer_name": "Тестовый гость 2",
        "table_id": 9,
        "reservation_time": "2025-09-13T20:19:56.547Z",
        "duration_minutes": 10
    })
    assert response2.status_code == 400

    # Получаем ID созданной брони из ответа
    created_reservation = response.json()
    reservation_id = created_reservation.get("id")
    assert reservation_id is not None, "Created reservation should have an ID"

    # Удаляем созданную бронь
    delete_response = requests.delete(f"http://localhost:8000/reservations/{reservation_id}")
    assert delete_response.status_code == 200  # Успешное удаление

