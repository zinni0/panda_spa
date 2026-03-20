import importlib
import pkgutil

from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import func

from panda_spa.config import ConfigLoader
from panda_spa.core import BookingFormData, BookingManager, services, SpaServiceFactory
from panda_spa.db import SessionLocal, Base, engine, models
from panda_spa.db.crud import delete_transaction, get_booking_by_id, set_booking_paid, get_bookings, \
    delete_bookings
from panda_spa.db.models.finance import \
    FinanceEntry  # wenn es finance crud gibt brauchen wir das nicht mehr
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
    error = None

    if request.method == "POST":
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

    return render_template(
        "booking_new.html",
        species_list=species_list,
        services=list(ServiceRegistryMeta.get_registry().keys()),
        error=error
    )


@app.route("/manage-bookings")
def render_manage_bookings():
    """Zeigt alle Buchungen sortiert nach Datum und Uhrzeit"""
    with SessionLocal() as db:
        sorted_bookings = get_bookings(
            db)  # Sorting doch egal oder? get_bookings ist doch schon sortiert(?)
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

        if request.method == "POST":
            discount = float(request.form.get("discount") or 0)
            tip = float(request.form.get("tip") or 0)
            note = request.form.get("note")

            total = base_price - discount + tip

            # FinanceEntry erstellen (Einnahme)
            finance_entry = FinanceEntry(
                type="income",
                amount=total,
                description=f"{booking.service_name}|{booking.user.name}|Rabatt={discount}|Trinkgeld={tip}|Notiz={note}"
            )

            # Finance CRUD wäre wahrscheinlich sinnvoller
            db.add(finance_entry)
            db.commit()

            set_booking_paid(db, booking_id)

            return redirect(url_for("render_manage_bookings"))

        return render_template(
            "income_new.html",
            booking=booking,
            base_price=base_price
        )


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
        delete_transaction(db, transaction_id)

    return redirect(url_for("render_finances"))


@app.route("/new-expense", methods=["GET", "POST"])
def render_new_expense():
    """
    Neue Betriebsausgabe erstellen
    """

    if request.method == "POST":
        with SessionLocal() as db:
            amount = float(request.form.get("amount") or 0)
            note = request.form.get("note")

            # Validierung ergänzen? → RICHARD ABSPRACHE

            finance_entry = FinanceEntry(
                type="expense",
                amount=amount,
                description=note or "No description"
            )

            db.add(finance_entry)
            db.commit()

        return redirect(url_for("render_finances"))

    return render_template("expense_new.html")


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("DB wurde erstellt mit Tabellen")

    ConfigLoader.load()

    app.run(debug=True)
