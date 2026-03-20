import importlib
import pkgutil
import re # brauchen wir für Umwandlung service_name in service_tag

from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import func

from panda_spa.config import ConfigLoader
from panda_spa.core import BookingFormData, BookingManager, services
from panda_spa.db import SessionLocal, Base, engine, models
from panda_spa.db.models.finance import FinanceEntry #wenn es finance crud gibt brauchen wir das nicht mehr
from panda_spa.db.crud import get_bookings, delete_bookings
from panda_spa.validation import ServiceRegistryMeta

for loader, name_pkg, is_pkg in pkgutil.iter_modules(services.__path__):
    importlib.import_module(f"{services.__name__}.{name_pkg}")

for loader, name_pkg, is_pkg in pkgutil.iter_modules(models.__path__):
    importlib.import_module(f"{models.__name__}.{name_pkg}")

app = Flask(__name__, template_folder="web/templates", static_folder="web/static")
#test
# Tierarten (werden später aus DB geladen?) -> Absprechen
species_list = [
    "Panda",
    "Fuchs",
    "Reh",
    "Hase",
    "Waschbär"
]

"""
Ersetzen z.B. mit:
get_species()
get_services()
get_bookings()
create_booking()
delete_booking()
"""


# -----------------------------
# ROUTEN
# -----------------------------

@app.route("/")
def home():
    """Startseite -> Neue Buchung"""
    return redirect(url_for("new_booking"))


@app.route("/new-booking", methods=["GET", "POST"])
def new_booking():
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

            return redirect(url_for("manage_bookings"))

    return render_template(
        "booking_new.html",
        species_list=species_list,
        services=list(ServiceRegistryMeta.get_registry().keys()),
        error=error
    )


@app.route("/manage-bookings")
def manage_bookings():
    """Zeigt alle Buchungen sortiert nach Datum und Uhrzeit"""
    with SessionLocal() as db:
        sorted_bookings = get_bookings(db)
        return render_template(
            "bookings_manage.html",
            bookings=sorted_bookings
        )


@app.route("/delete-booking/<int:booking_id>")
def delete_booking(booking_id):
    """Löscht eine Buchung"""
    with SessionLocal() as db:
        status, msg = delete_bookings(db, booking_id)
        print(f"{status}: {msg}")

    return redirect(url_for("manage_bookings"))


@app.route("/new-income/<int:booking_id>", methods=["GET", "POST"])
def new_income(booking_id):
    """
    Erstellt eine Abrechnung für eine Buchung
    """

    with SessionLocal() as db:

        # Buchung laden
        booking = db.get(models.Booking, booking_id)
        if not booking:
            return "Booking not found", 404

        # Preis aus config laden (Namen müssen passen → MIT RICHARD ABSPRECHEN)
        service_key = re.sub(r'(?<!^)(?=[A-Z])', '_', booking.service_name).lower()

        # Finance CRUD wäre wahrscheinlich sinnvoller
        base_price = ConfigLoader.get(
            f"spa_services.{service_key}.price",
            default=0
        )

        if request.method == "POST":

            discount = float(request.form.get("discount") or 0)
            tip = float(request.form.get("tip") or 0)
            note = request.form.get("note")

            total = base_price - discount + tip

            # FinanceEntry erstellen (Einnahme)
            finance_entry = FinanceEntry(
                type="income",
                amount=total,
                description=f"{booking.service_name}|{booking.user.name}|discount={discount}|tip={tip})|Note={note}"
            )

            # Finance CRUD wäre wahrscheinlich sinnvoller
            db.add(finance_entry)
            booking.service_name += " (BEZAHLT)"
            db.commit()

            # Braucht es dann noch eine Finance Entry für Ausgabe (Jede Dienstleistung kostet ja (oder machen wir ohne
            # Kosten pro Dienstleistung?))?

            return redirect(url_for("manage_bookings"))

        return render_template(
            "income_new.html",
            booking=booking,
            base_price=base_price
        )


@app.route("/finances")
def finances():
    # Finance CRUD wäre wahrscheinlich sinnvoller
    with SessionLocal() as db:
        total_income = db.query(func.sum(FinanceEntry.amount)) \
                           .filter(FinanceEntry.type == "income") \
                           .scalar() or 0

        total_expense = db.query(func.sum(FinanceEntry.amount)) \
                            .filter(FinanceEntry.type == "expense") \
                            .scalar() or 0

        profit = total_income - total_expense

        return render_template(
            "finances.html",
            total_income=round(total_income, 2),
            total_expense=round(total_expense, 2),
            profit=round(profit, 2)
        )


@app.route("/new-expense", methods=["GET", "POST"])
def new_expense():
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

        return redirect(url_for("finances"))

    return render_template("expense_new.html")


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("DB wurde erstellt mit Tabellen")

    ConfigLoader.load()

    app.run(debug=True)
