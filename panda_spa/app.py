import importlib
import pkgutil

from flask import Flask, render_template, request, redirect, url_for

from panda_spa import models
from panda_spa.core import BookingFormData, BookingManager, services, ConfigLoader
from panda_spa.core.crud import get_bookings
from panda_spa.core.database import SessionLocal, Base, engine
from panda_spa.validation import ServiceRegistryMeta

for loader, name_pkg, is_pkg in pkgutil.iter_modules(services.__path__):
    importlib.import_module(f"{services.__name__}.{name_pkg}")

for loader, name_pkg, is_pkg in pkgutil.iter_modules(models.__path__):
    importlib.import_module(f"{models.__name__}.{name_pkg}")

app = Flask(__name__)

# -----------------------------
# MOCK DATA (später DB ersetzen)
# -----------------------------

# Tierarten (werden später aus DB geladen)
species_list = [
    "Panda",
    "Fuchs",
    "Reh",
    "Hase",
    "Waschbär"
]

# Buchungen (temporär)
bookings = []

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
                    services=list(ServiceRegistryMeta.registry.keys()),
                    error=error
                )
            else:
                return redirect(url_for("manage_bookings"))

    return render_template(
        "booking_new.html",
        species_list=species_list,
        services=list(ServiceRegistryMeta.registry.keys()),
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


@app.route("/delete-booking/<int:index>")
def delete_booking(index):
    """Löscht eine Buchung"""
    if 0 <= index < len(bookings):
        bookings.pop(index)

    return redirect(url_for("manage_bookings"))


@app.route("/finances")
def finances():
    """Finanzseite (noch leer)"""
    return render_template("finances.html")


if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("DB wurde erstellt mit Tabellen")

    ConfigLoader.load()

    app.run(debug=True)
