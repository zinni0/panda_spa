import logging
from typing import Tuple

from sqlalchemy.orm import Session

from . import set_booking_paid
from ..models.finance import FinanceEntry
from schema import TransactionSchema

logger = logging.getLogger(__name__)


def create_transaction(db: Session, transaction: TransactionSchema) -> FinanceEntry:
    """
    Create a new financial transaction in the database

    :param db: SQLAlchemy session object
    :param transaction: Transaction data to create
    :return: The newly created FinanceEntry object
    """
    db_transaction = FinanceEntry(
        type=transaction.transaction_type,
        amount=transaction.amount,
        description=transaction.description,
        date=transaction.date,
        booking_id=transaction.booking_id
    )

    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)

    return db_transaction


def get_transactions(db: Session, filter_type: str = None):
    """
    Return all transactions ordered by date

    :param db: SQLAlchemy session object
    :param filter_type: Optional filter for query
    :return: List of FinanceEntry objects
    """
    query = db.query(FinanceEntry)

    if filter_type in ["income", "expense"]:
        query = query.filter(FinanceEntry.type == filter_type)

    return query.order_by(FinanceEntry.date).all()


def delete_transaction(db: Session, transaction_id: int) -> Tuple[str, str]:
    """
    Delete a transaction by its ID

    :param db: SQLAlchemy session object
    :param transaction_id: ID of the transaction to delete
    :return: Tuple containing status ('success' or 'error') and a message
    """
    transaction = db.query(FinanceEntry).get(transaction_id)

    if not transaction:
        logger.warning("Transaction %s not found", transaction_id)
        return "error", "Transaction not found"

    booking = transaction.booking

    db.delete(transaction)

    if booking:
        set_booking_paid(db, booking.id, False)

    db.commit()
    logger.info("Transaction %s deleted", transaction_id)
    return "success", f"Transaction {transaction_id} deleted"
