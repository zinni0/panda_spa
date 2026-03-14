import importlib
import pkgutil
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for

from panda_spa import models
from panda_spa.core import services
from panda_spa.core.config_loader import ConfigLoader
from panda_spa.core.crud.user import create_user
from panda_spa.core.database import SessionLocal, Base, engine
from panda_spa.schema.user import UserSchema
from panda_spa.validation.metaclasses import ServiceRegistryMeta

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
        db = SessionLocal()

        try:
            name = request.form.get("name")
            species = request.form.get("species")

            user_schema = UserSchema(
                name=name,
                species=species,
                favorite_service=None
            )

            user = create_user(db, user_schema)
            print(user.id)

            date = request.form.get("date")
            time = request.form.get("time")
            service = request.form.get("service")

            # Datum + Zeit kombinieren
            booking_datetime = datetime.strptime(
                f"{date} {time}",
                "%Y-%m-%d %H:%M"
            )

            # aktuelle Zeit
            now = datetime.now()

            # Prüfen, ob Termin in Vergangenheit liegt
            if booking_datetime < now:
                error = "Buchung darf nicht in der Vergangenheit liegen"
            else:
                booking = {
                    "name": name,
                    "species": species,
                    "date": date,
                    "time": time,
                    "service": service
                }

                bookings.append(booking)

            return redirect(url_for("manage_bookings"))
        finally:
            db.close()

    return render_template(
        "booking_new.html",
        species_list=species_list,
        services=list(ServiceRegistryMeta.registry.keys()),
        error=error
    )


@app.route("/manage-bookings")
def manage_bookings():
    """Zeigt alle Buchungen sortiert nach Datum und Uhrzeit"""

    sorted_bookings = sorted(
        bookings,
        key=lambda b: (b["date"], b["time"])
    )

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
