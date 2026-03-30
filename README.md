# panda_spa

## 🚀 Startup Guide

Folge diesen Schritten, um das Projekt lokal zu starten:

### 1. Repository klonen

### 2. Virtuelle Umgebung erstellen (optional, aber empfohlen)

```bash
python -m venv venv

# Aktivieren der virtuellen Umgebung

# Windows

venv\Scripts\activate

# macOS / Linux

source
venv / bin / activate
```

### 3. Abhängigkeiten installieren

```bash
pip install -r requirements.txt
```

### 4. Anwendung starten

```bash
python - m panda_spa.app
```

Hinweis: Es wird keine .env Datei benötigt. Alle Konfigurationen sind bereits im Projekt enthalten.

## 🧩 Neue Services hinzufügen

### 🔤 Naming & Casing Konventionen

In diesem Projekt werden feste Casing-Regeln verwendet, die **zwingend eingehalten werden müssen**, da die automatische
Service-Erkennung darauf basiert.

* **Snake Case** → für Dateien, Variablen und Config-Keys

    * Beispiele:

        * `thermal_bath.py`
        * `thermal_bath`
        * `spa_services.thermal_bath.temperature`

* **PascalCase** → für Klassennamen

    * Beispiel:

        * `ThermalBath`

👉 **Wichtig:**

* Dateiname, YAML-Key und Config-Pfad müssen exakt zusammenpassen
* Abweichungen wie `thermalBath` oder `Thermal_Bath` führen zu Fehlern

---

Um einen neuen Service zu erstellen, folge diesen Schritten:

### 1. Neue Datei anlegen

Erstelle unter `core/services` eine neue Python-Datei, z. B.:

```bash
thermal_bath.py
```

⚠️ **Wichtig:** Das Casing (Schreibweise) muss exakt eingehalten werden!

---

### 2. Klasse erstellen

Die Klasse muss von `SpaService` erben.

---

### 3. Attribute definieren

Jeder Service benötigt mindestens:

* `price`
* `duration`

Zusätzlich können beliebige weitere Attribute definiert werden.

---

### 4. Pflichtmethoden implementieren

Folgende Methoden müssen implementiert werden:

* `get_description()`
* `to_dict()`

#### Beispiel:

```python
from typing import Dict, Any

from validation import RangeValueDescriptor

from .spa_service import SpaService


class ThermalBath(SpaService):
    _temperature = RangeValueDescriptor(
        config_path="spa_services.thermal_bath.temperature"
    )

    def __init__(self, price: float, duration: int, temperature: int):
        super().__init__(price=price, duration=duration)
        self._temperature = temperature

    def get_description(self) -> str:
        return f"Thermal bath at {self._temperature}°C"

    def to_dict(self) -> Dict[str, Any]:
        base = super().to_dict()
        base["temperature"] = self._temperature
        return base
```

---

### 5. Service in der Config registrieren

In der Datei `config/services.yaml` muss der neue Service unter `spa_services` eingetragen werden:

```yaml
thermal_bath:
  temperature:
    min: 30
    max: 40
  price: 56.99
  duration: 45
  extra:
    temperature: 38
```

⚠️ **Wichtig:** Auch hier muss das Casing exakt stimmen!

---

### 6. Optional: API-Simulation über `extra`

Unter `extra` können Werte definiert werden, die eine API simulieren und dynamische Werte für Descriptoren liefern.

---

### 7. Optional: Descriptor konfigurieren

Descriptoren können mit einem Config-Pfad versehen werden:

```python
_temperature = RangeValueDescriptor(
    config_path="spa_services.thermal_bath.temperature"
)
```

---

## ⚠️ Wichtige Hinweise

* Casing muss überall exakt eingehalten werden
* Tippfehler unbedingt vermeiden

❗ Andernfalls kann es zu unerwarteten Fehlern kommen oder die automatische Service-Erkennung funktioniert nicht korrekt
