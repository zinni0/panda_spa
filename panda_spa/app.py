import importlib
import pkgutil

from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import func

from panda_spa.config import ConfigLoader
from panda_spa.core import BookingFormData, BookingManager, services, SpaServiceFactory, \
    FinanceFormData, FinanceManager
from panda_spa.db import SessionLocal, Base, engine, models
from panda_spa.db.crud import delete_transaction, get_booking_by_id, get_bookings, \
    delete_bookings
# wenn es finance crud gibt brauchen wir das nicht mehr
from panda_spa.db.models.finance import FinanceEntry
from panda_spa.validation import ServiceRegistryMeta

for loader, name_pkg, is_pkg in pkgutil.iter_modules(services.__path__):
    importlib.import_module(f"{services.__name__}.{name_pkg}")

for loader, name_pkg, is_pkg in pkgutil.iter_modules(models.__path__):
    importlib.import_module(f"{models.__name__}.{name_pkg}")

app = Flask(__name__, template_folder="web/templates", static_folder="web/static")

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
        sorted_bookings = get_bookings(db)

    return render_template(
        "bookings_manage.html",
        bookings=sorted_bookings
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
                base_price=base_price
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
            # Konrad, hier musst du nochmal ran, hier fehlt die Anzeige von Errors
            raise RuntimeError(error)

        return redirect(url_for("render_manage_bookings"))


@app.route("/finances")
def render_finances():
    filter_type = request.args.get("type") or "all"
    # Finance CRUD wäre wahrscheinlich sinnvoller (Filterfunktionen)
    with SessionLocal() as db:
        total_income = db.query(func.sum(FinanceEntry.amount)) \
                           .filter(FinanceEntry.type == "income") \
                           .scalar() or 0

        total_expense = db.query(func.sum(FinanceEntry.amount)) \
                            .filter(FinanceEntry.type == "expense") \
                            .scalar() or 0

        profit = total_income - total_expense

        query = db.query(FinanceEntry)  # Wir brauchen auch getTransaction, also einzeln!

        if filter_type in ["income", "expense"]:
            query = query.filter(FinanceEntry.type == filter_type)

        transactions = query.order_by(FinanceEntry.date).all()

    return render_template(
        "finances.html",
        total_income=round(total_income, 2),
        total_expense=round(total_expense, 2),
        profit=round(profit, 2),
        transactions=transactions,
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
        return render_template("expense_new.html")

    with SessionLocal() as db:
        form_data = FinanceFormData(
            type="expense",
            amount=float(request.form.get("amount") or 0),
            description=(request.form.get("note") or "No description")
        )

        status_code, error = FinanceManager.create_transaction(db, form_data)

        if status_code != 200:
            # Konrad, hier musst du nochmal ran, hier fehlt die Anzeige von Errors
            raise RuntimeError(error)

        return redirect(url_for("render_finances"))


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("DB wurde erstellt mit Tabellen")

    ConfigLoader.load()

    app.run(debug=True)
