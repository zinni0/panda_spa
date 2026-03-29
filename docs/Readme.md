# Abschlussbericht: Python Panda-Spa

## 1. Einleitung und Vision

### 1.1 Projektvision und Ziele
Das Projekt Panda Spa adressiert die administrative Verwaltung eines exklusiven Wellnesszentrums im Bambuswald. In dieser Domäne agiert ein Panda als alleiniger Manager, der sämtliche Buchungsprozesse, Dienstleistungskonfigurationen und Finanzanalysen über eine zentrale Management-Konsole steuert. Die Kunden (Waldtiere) interagieren nicht selbst mit dem System, sondern lassen ihre Termine direkt durch den Panda erfassen.

**Das Kernproblem:** Die manuelle Überwachung von Sicherheitsgrenzwerten (z. B. maximale Wassertemperaturen im Thermalbad) und die Koordination individueller Kundenpräferenzen bei einer wachsenden Anzahl an Dienstleistungen führt zu einer hohen kognitiven Belastung und Fehleranfälligkeit.

**Die Vision:** Die Entwicklung einer robusten Management-Applikation, die durch eine konfigurationsgesteuerte Architektur maximale Flexibilität bietet. Ziel ist es, ein System zu schaffen, das neue Wellness-Angebote allein durch Anpassung einer externen Konfigurationsdatei integriert, während die Einhaltung aller Geschäftsregeln durch automatisierte, technologische "Wächter" im Hintergrund garantiert wird.

### 1.2 Wissenschaftliche Herausforderung / Python-Spezifischer Aspekt
Der technische Fokus des Projekts liegt auf der **Metaprogrammierung**, einer Methode, bei der Programme ihre eigene Struktur analysieren und dynamisch anpassen können. Wissenschaftlich betrachtet lösen wir hier das Problem der strukturellen Redundanz und statischen Starrheit.

**Die Analogie im Projekt:** Der Panda führt eine "magische Bambusliste" (die Konfigurationsdatei). Jedes Mal, wenn er dort ein neues Angebot einträgt, "lernt" das System automatisch, wie dieses Angebot aussieht, welche Regeln dafür gelten und wie es validiert werden muss.

**Python-Spezifische Umsetzung:**
* **Introspektion:** Das System nutzt Pythons Fähigkeit, Klassen und Attribute zur Laufzeit zu analysieren.
* **Deskriptoren:** Um sicherzustellen, dass der Panda keine gefährlichen Werte (z. B. zu heiße Saunatemperaturen) eingibt, werden Deskriptoren als deklarative Validierungswächter eingesetzt. Dies trennt die technische Prüfung von der fachlichen Logik (*Separation of Concerns*).
* **Code-Generierung:** Durch Techniken der dynamischen Code-Erzeugung (z. B. via `type()` oder `compile()`) werden aus den Einträgen der Konfigurationsdatei reale Programmlogiken generiert, ohne den Quellcode der Anwendung modifizieren zu müssen.

### 1.3 Arbeitshypothese
> „Die Implementierung einer metaprogrammatischen Validierungsschicht mittels Python-Deskriptoren ermöglicht eine 100%ige Einhaltung der in einer externen Konfigurationsdatei definierten Sicherheitsgrenzwerte, während die zyklomatische Komplexität des Buchungscodes im Vergleich zu herkömmlichen If-Prüfungen um mindestens 30 % reduziert wird.“

---

## 2. Requirements Engineering

### 2.1 Kontextdiagramm
Das Panda Spa System ist als geschlossene, lokale Management-Lösung (Web-App) konzipiert. Es gibt keine direkten Schnittstellen für Endkunden; das System wird ausschließlich intern bedient.

* **Akteur (Panda Manager):** Der alleinige menschliche Nutzer. Er nimmt Kundenwünsche entgegen und interagiert über die Flask-basierte Web-Benutzeroberfläche mit dem System.
* **Externe Systeme / Datenquellen:**
    * **SQLite-Datenbank (`panda_spa.db`):** Persistente Speicherung von Nutzern, Buchungen und Finanztransaktionen.
    * **Konfigurationsdatei (`services.yaml`):** Externe Datenquelle für Dienstleistungsparameter (Preise, Dauer, Grenzwerte).

### 2.2 Funktionale Anforderungen als Katalog
| ID | Anforderung | Status | Notizen |
|:---|:---|:---|:---|
| REQ-01 | Verwaltung von Spa-Dienstleistungen via Config | [x] 100 % | Services werden über `services.yaml` geladen. |
| REQ-02 | Automatisierte Validierung | [x] 100 % | Deskriptoren & Pydantic-Schemas. |
| REQ-03 | Manuelles Termin- und Buchungssystem | [x] 100 % | Speicherung via SQLAlchemy. |
| REQ-04 | Vermeidung von Terminüberschneidungen | [x] 100 % | Prüfung durch `BookingManager` (HTTP 409 bei Konflikt). |
| REQ-05 | Erfassung von Einnahmen | [x] 100 % | Abrechnung inkl. Rabatt und Trinkgeld. |
| REQ-06 | Erfassung von Ausgaben | [x] 100 % | Eingabe von Betriebsausgaben. |
| REQ-07 | Gewinnberechnung & Visualisierung | [x] 100 % | Dashboard inkl. Chart.js-Visualisierung. |
| REQ-08 | Metaprogrammatische Registrierung | [x] 100 % | Automatische Erfassung via `ServiceRegistryMeta`. |

### 2.3 Nicht-funktionale Anforderungen
* **Sicherheit (Security):** Fokus auf Datenintegrität durch Pydantic-Validierungslayer.
* **Wartbarkeit (Maintainability):** Strenge Schichtentrennung (Layered Architecture).
* **Zuverlässigkeit (Reliability):** Abfangen ungültiger Zustände durch Manager-Klassen und saubere Fehlermeldungen.

---

## 3. Architektur und Tech-Stack

### 3.1 Auswahl der Plattform
Wahl einer Flask-Web-Applikation für Plattformunabhängigkeit im Browser und Flexibilität durch HTML/CSS/JS gegenüber Desktop-GUIs.

### 3.2 Modularer Kern und Open-Closed Principle
1.  **Daten-Layer:** SQLite.
2.  **ORM-Layer:** SQLAlchemy.
3.  **Validierungs-Layer:** Pydantic.
4.  **Service-Layer:** Core-Geschäftslogik (Managers/Factories).
5.  **Frontend-Layer:** Flask-Templates.

### 3.3 Technologie-Stack
* **Flask:** Web-Framework & Routing.
* **SQLAlchemy:** ORM zur Abstraktion von SQL.
* **Pydantic:** Strikte Typisierung und Validierung.
* **PyYAML:** Laden der Konfigurationsdaten.

---

## 4. Design und Modellierung

### 4.1 Domänenmodell
* **User:** Die Waldtiere (Kunden).
* **SpaService:** Abstrakte Basis für Dienstleistungen (Sauna, Massage, etc.).
* **Booking:** Verbindung von User, Service und Zeitraum.
* **FinanceEntry:** Einnahmen (an Bookings geknüpft) und Ausgaben.

``` mermaid
classDiagram
    %% Metaprogramming & Validation
    class ServiceRegistryMeta {
        <<Metaclass>>
        -_registry: Dict
        +__new__()
        +get_registry()
    }

    class RangeValueDescriptor {
        <<Descriptor>>
        -_config_path: str
        +__get__()
        +__set__()
    }

    %% Database Models (SQLAlchemy)
    class User {
        +int id
        +String name
        +String species
        +String favorite_service_name
    }

    class Booking {
        +int id
        +int user_id
        +String service_name
        +DateTime start_time
        +DateTime end_time
        +bool is_paid
    }

    class FinanceEntry {
        +int id
        +String type
        +float amount
        +String description
        +DateTime date
        +int booking_id
    }

    %% Core Services (Domain Logic)
    class SpaService {
        <<Abstract>>
        <<metaclass: ServiceRegistryMeta>>
        #float _price
        #int _duration
        +name() str
        +get_description() str
        +to_dict() dict
    }

    class ThermalBath {
        <<RangeValueDescriptor>> _temperature
    }
    class Sauna {
        <<RangeValueDescriptor>> _temperature
    }
    class AromaTherapy {
        <<RangeValueDescriptor>> _intensity
    }
    class Massage

    %% Relationships
    User "1" -- "*" Booking : tätigt
    Booking "1" -- "0..1" FinanceEntry : generiert Einnahme
    
    SpaService <|-- ThermalBath
    SpaService <|-- Sauna
    SpaService <|-- AromaTherapy
    SpaService <|-- Massage

    ThermalBath ..> RangeValueDescriptor : validiert Temperatur
    Sauna ..> RangeValueDescriptor : validiert Temperatur
    AromaTherapy ..> RangeValueDescriptor : validiert Intensität

```

### 4.2 Verhaltens- und Interaktionsdiagramme
* **State:** Lebenszyklus einer Buchung (Offen -> Bezahlt -> Gelöscht).
* **Activity:** Validierung -> Zeitprüfung -> Persistierung.
* **Sequence:** Fluss von der UI über den `BookingManager` zur `SpaServiceFactory` bis zur DB.

```
stateDiagram-v2
    [*] --> Offen : Panda erstellt Termin (is_paid = False)
    
    Offen --> Bezahlt : Panda rechnet ab (FinanceEntry 'income' erstellt)
    
    Offen --> Gelöscht : Panda storniert Termin (delete_booking)
    Bezahlt --> Gelöscht : Panda storniert Termin oder Transaktion
    
    Gelöscht --> [*]
```

``` mermaid

flowchart TD
    Start([Start: Panda gibt Buchungsdaten im Frontend ein]) --> ValPydantic["Pydantic Schema Validierung"]
    ValPydantic --> CheckFormal{"Formalien korrekt? <br> z.B. Endzeit > Startzeit"}
    
    CheckFormal -->|Nein| ErrorUI["Fehlermeldung im HTML rendern"]
    
    CheckFormal -->|Ja| Factory["SpaServiceFactory lädt Service & Dauer aus YAML"]
    Factory --> CalcTime["BookingManager berechnet Endzeit"]
    CalcTime --> DBCheck["BookingManager prüft DB auf Überschneidung"]
    
    DBCheck --> Conflict{"Termin-Konflikt?"}
    
    Conflict -->|Ja| Error409["Fehler 409: 'Zeitraum belegt' zurückgeben"]
    Error409 --> ErrorUI
    
    Conflict -->|Nein| CreateUser["create_user() in DB ausführen"]
    CreateUser --> CreateBooking["create_booking() in DB ausführen"]
    CreateBooking --> Success(["Erfolg: Weiterleitung zu /manage-bookings"])

```

### 4.3 Design Patterns
* **Factory Pattern:** Zentrale Erstellung von Dienstleistungsobjekten.
* **Registry & Metaclass:** Automatische Klassenerfassung.
* **Descriptor Pattern:** Kapselung der Validierungslogik für Attribute.
* **MVC:** Trennung von Model, View und Controller.

``` mermaid

sequenceDiagram
    autonumber
    actor Panda

    box "Frontend Layer" #LightCyan
    participant UI as Flask UI (app.py)
    end

    box "Validation Layer" #LightYellow
    participant Schema as BookingSchema
    end

    box "Service Layer" #MistyRose
    participant Manager as BookingManager
    participant Factory as SpaServiceFactory
    end

    box "Data Layer" #Lavender
    participant DB as Database (SQLite)
    end

    Panda->>UI: POST /new-booking (Formulardaten)
    activate UI
    
    UI->>Schema: Validiere Eingaben (Formalien)
    activate Schema
    
    alt Eingaben ungültig
        Schema-->>UI: ValidationError
        UI-->>Panda: Zeige Formular mit Fehlerhinweis
    else Eingaben gültig
        Schema-->>UI: Validierte Daten
        deactivate Schema
        
        UI->>Manager: create_booking(db, form_data)
        activate Manager
        
        Manager->>Factory: create(data.service)
        activate Factory
        Note right of Factory: Lädt Dauer & Preis<br/>dynamisch aus services.yaml
        Factory-->>Manager: Service-Instanz
        deactivate Factory
        
        Manager->>DB: _find_bookings(start, end)
        activate DB
        
        alt Konflikt gefunden
            DB-->>Manager: Bestehende Buchung (Overlap)
            Manager-->>UI: Status 409 + Fehlermeldung
            UI-->>Panda: Zeige Fehler "Termin belegt"
        else Kein Konflikt
            DB-->>Manager: None (Freier Zeitraum)
            
            Manager->>DB: create_user()
            DB-->>Manager: Neues User-Objekt
            
            Manager->>DB: create_booking()
            DB-->>Manager: Neues Booking-Objekt
            deactivate DB
            
            Manager-->>UI: Status 200 (Success)
            deactivate Manager
            UI-->>Panda: Redirect zu "Buchungen verwalten"
        end
    end
    deactivate UI

```

---

## 5. Wissenschaftliche Problemstellung (Jupyter Notebook)

### 5.1 Methodik der Untersuchung
Vergleich zwischen traditionellem OOP-Ansatz (imperative If-Prüfungen) und metaprogrammatischem Ansatz (Deskriptoren).

### 5.2 Analyseergebnisse
* **Reduktion von Boilerplate:** Über 80 % weniger modellspezifischer Validierungscode durch Deskriptoren.
* **Typsicherheit:** Zuverlässiges Abfangen von Fehlern (z. B. falsche Datentypen) vor der Verarbeitung.
* **OCP:** Neue Klassen werden ohne manuellen Register-Aufruf sofort erkannt.

---

## 6. Implementierung und Qualitätssicherung

### 6.1 Code-Struktur
Konsequente Nutzung von Clean-Code-Prinzipien, englischen Namenskonventionen und ausführlichen Docstrings.

### 6.2 Test-Konzept
* **Unit-Tests:** Prüfung von Pydantic-Schemas und Deskriptoren via `pytest`.
* **Integration-Tests:** Validierung des Zusammenspiels von Config, Registry und Buchungslogik.

### 6.3 CI-Pipeline
GitHub Actions für:
* **Automatisierte Tests:** `pytest` bei jedem Push.
* **Statische Analyse:** `pylint` (Quality-Gate: Score > 9.5/10).

---

## 7. Software-Qualität nach ISO 25010
* **Wartbarkeit (9/10):** Durch Metaprogrammierung und strikte Schichtenarchitektur.
* **Zuverlässigkeit (9/10):** Durch doppelte Validierungsebene (Pydantic & Deskriptoren).
* **Benutzbarkeit (8/10):** Fokus auf intuitive Formulare und grafische Auswertungen.
* **Sicherheit (8/10):** SQL-Injection-Schutz durch ORM und sicheres YAML-Loading.

---

## 8. Projektabschluss und Reflexion

### 8.1 Methodik
Agile Entwicklung in drei Phasen. Wichtiger Pivot: Verzicht auf Asynchronität zugunsten geringerer Komplexität für ein Single-User-System.

### 8.2 Selbstreflexion
Der Einsatz von KI diente als Sparringspartner für die theoretische Fundierung und das CSS-Design. Die kritische Prüfung der KI-Vorschläge vertiefte das Verständnis für Pythons Interna (Metaklassen).

### 8.3 Nutzungsanweisung
1.  `pip install -r requirements.txt`
2.  `python -m panda_spa.app`
3.  Browser: `http://127.0.0.1:5000`

### 8.4 Pitch-Video
Das Video ergänzt diesen Bericht durch eine Live-Demo der UI und Visualisierung der Forschungsergebnisse.
