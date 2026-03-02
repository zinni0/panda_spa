from core.database import Base, engine
from models.user import User
from models.booking import Booking
from models.finance import FinanceEntry


Base.metadata.create_all(bind=engine)
print("DB wurde erstellt mit Tabellen")