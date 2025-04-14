from fastapi import FastAPI, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from sqlalchemy import cast, DateTime
from datetime import timedelta


import models
from models import Base
from database import engine, SessionLocal
from schemas import TableCreate, Table, ReservationCreate, Reservation


app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/tables/", response_model=Table)
def create_table(table: TableCreate, db: Session = Depends(get_db)) -> Table:
    """
    POST table
    :param table:
    :param db:
    :return:
    """
    db_table = models.Table(
        name=table.name,
        seats=table.seats,
        location=table.location
    )
    db.add(db_table)
    db.commit()
    db.refresh(db_table)
    print(type(db_table))
    return db_table

@app.get("/tables/", response_model=List[Table])
def get_table(db:Session = Depends(get_db)):
    """
    GET list table
    :param db:
    :return:
    """
    print(type(db.query(models.Table).all()))
    return db.query(models.Table).all()


@app.delete("/tables/{id}")
def delete_table(id: int, db: Session = Depends(get_db)):
    """
    DELETE table
    :param id:
    :param db:
    :return:
    """
    db_table = db.query(models.Table).filter(models.Table.id == id).first()

    if db_table is None:
        raise HTTPException(status_code=404, detail="Table not found")

    db.delete(db_table)
    db.commit()
    return {"ok": True}


@app.post("/reservations/", response_model=Reservation)
def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    """
    POST reservations, Check for the coincidence of the ID table and time
    :param reservation:
    :param db:
    :return:
    """
    conflicting_reservations = db.query(models.Reservation).filter(
        models.Reservation.table_id == reservation.table_id,
        models.Reservation.reservation_time < reservation.reservation_time + timedelta(minutes=reservation.duration_minutes),
        cast(models.Reservation.reservation_time, DateTime) + timedelta(minutes=reservation.duration_minutes) > reservation.reservation_time
    ).all()

    if conflicting_reservations:
        raise HTTPException(status_code=400, detail="Table is already booked for this time slot")

    db_reservation = models.Reservation(
        customer_name=reservation.customer_name,
        table_id=reservation.table_id,
        reservation_time=reservation.reservation_time,
        duration_minutes=reservation.duration_minutes
    )
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation

@app.get("/reservations/", response_model=List[Reservation])
def get_reserv(db:Session = Depends(get_db)):
    """
    GET reservations
    :param db:
    :return:
    """
    return db.query(models.Reservation).all()

@app.delete("/reservations/{id}")
def delete_reservations(id: int, db: Session = Depends(get_db)):
    """
    DELETE reservations
    :param id:
    :param db:
    :return:
    """
    db_reservation = db.query(models.Reservation).filter(models.Reservation.id == id).first()

    if db_reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")

    db.delete(db_reservation)
    db.commit()
    return {"ok": True}

