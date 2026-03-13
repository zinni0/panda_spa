from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for

from panda_spa.core.config_loader import ConfigLoader
from panda_spa.core.services import * # pylint: disable=unused-import
from panda_spa.validation.metaclasses import ServiceRegistryMeta

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

        name = request.form.get("name")
        species = request.form.get("species")
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

        # Prüfen ob Termin in Vergangenheit liegt
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
    ConfigLoader.load()

    app.run(debug=True)
