import importlib
import os
import pkgutil
import sys

from flask import Flask, render_template, request, redirect, url_for

repo_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, repo_root)

from config import ConfigLoader
from core import (
    BookingFormData,
    BookingManager,
    services,
    SpaServiceFactory,
    FinanceFormData,
    FinanceManager
)
from db import SessionLocal, Base, engine, models
from db.crud import (
    delete_transaction,
    get_booking_by_id,
    get_bookings,
    delete_bookings,
    get_transactions
)
from validation import ServiceRegistryMeta

for loader, name_pkg, is_pkg in pkgutil.iter_modules(services.__path__):
    importlib.import_module(f"{services.__name__}.{name_pkg}")

for loader, name_pkg, is_pkg in pkgutil.iter_modules(models.__path__):
    importlib.import_module(f"{models.__name__}.{name_pkg}")

app = Flask(
    __name__,
    template_folder=os.path.join(repo_root, "web", "templates"),
    static_folder=os.path.join(repo_root, "web", "static")
)

species_list = [
    "Panda",
    "Fuchs",
    "Reh",
    "Hase",
    "Waschbär"
]


# -----------------------------
# ROUTEN
# -----------------------------

@app.route("/")
def render_home():
    """Startseite -> Neue Buchung"""
    return redirect(url_for("render_new_booking"))


@app.route("/new-booking", methods=["GET", "POST"])
def render_new_booking():
    if not request.method == "POST":
        return render_template(
            "booking_new.html",
            species_list=species_list,
            services=list(ServiceRegistryMeta.get_registry().keys()),
            error=None
        )

    with SessionLocal() as db:
        form_data = BookingFormData(
            name=request.form.get("name"),
            species=request.form.get("species"),
            date=request.form.get("date"),
            time=request.form.get("time"),
            service=request.form.get("service")
        )

        status_code, error = BookingManager.create_booking(db, form_data)

        if status_code != 200:
            return render_template(
                "booking_new.html",
                species_list=species_list,
                services=list(ServiceRegistryMeta.get_registry().keys()),
                error=error
            )

        return redirect(url_for("render_manage_bookings"))


@app.route("/manage-bookings")
def render_manage_bookings():
    """Zeigt alle Buchungen sortiert nach Datum und Uhrzeit"""
    with SessionLocal() as db:
        ordered_bookings = get_bookings(db)

    return render_template(
        "bookings_manage.html",
        bookings=ordered_bookings
    )


@app.route("/delete-booking/<int:booking_id>")
def render_delete_booking(booking_id):
    """Löscht eine Buchung"""
    with SessionLocal() as db:
        status, msg = delete_bookings(db, booking_id)
        print(f"{status}: {msg}")

    return redirect(url_for("render_manage_bookings"))


@app.route("/new-income/<int:booking_id>", methods=["GET", "POST"])
def render_new_income(booking_id):
    """
    Erstellt eine Abrechnung für eine Buchung
    """

    with SessionLocal() as db:
        booking = get_booking_by_id(db, booking_id)
        if not booking:
            return "Booking not found", 404

        service = SpaServiceFactory.create(booking.service_name)
        base_price = service.to_dict().get("price")

        if not request.method == "POST":
            return render_template(
                "income_new.html",
                booking=booking,
                base_price=base_price,
                error=None
            )

        discount = float(request.form.get("discount") or 0)
        tip = float(request.form.get("tip") or 0)

        form_data = FinanceFormData(
            type="income",
            amount=(base_price + tip) - discount,
            description=(request.form.get("note") or "No description")
        )

        status_code, error = FinanceManager.create_transaction(db, form_data, booking_id)

        if status_code != 200:
            return render_template(
                "income_new.html",
                booking=booking,
                base_price=base_price,
                error=error
            )

        return redirect(url_for("render_manage_bookings"))


@app.route("/finances")
def render_finances():
    filter_type = request.args.get("type") or "all"

    with SessionLocal() as db:
        transactions = get_transactions(db)

        total_income = sum(t.amount for t in transactions if t.type == "income")
        total_expense = sum(t.amount for t in transactions if t.type == "expense")
        profit = total_income - total_expense

        ordered_transactions = get_transactions(db, filter_type)

    return render_template(
        "finances.html",
        total_income=round(total_income, 2),
        total_expense=round(total_expense, 2),
        profit=round(profit, 2),
        transactions=ordered_transactions,
        active_filter=filter_type
    )


@app.route("/delete-transaction/<int:transaction_id>")
def render_delete_transaction(transaction_id):
    with SessionLocal() as db:
        status, msg = delete_transaction(db, transaction_id)
        print(f"{status}: {msg}")

    return redirect(url_for("render_finances"))


@app.route("/new-expense", methods=["GET", "POST"])
def render_new_expense():
    """
    Neue Betriebsausgabe erstellen
    """

    if not request.method == "POST":
        return render_template(
            "expense_new.html",
            error=None
        )

    with SessionLocal() as db:
        form_data = FinanceFormData(
            type="expense",
            amount=float(request.form.get("amount") or 0),
            description=(request.form.get("note") or "No description")
        )

        status_code, error = FinanceManager.create_transaction(db, form_data)

        if status_code != 200:
            return render_template(
                "expense_new.html",
                error=error
            )

        return redirect(url_for("render_finances"))


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("DB wurde erstellt mit Tabellen")

    ConfigLoader.load()

    app.run(debug=True)
