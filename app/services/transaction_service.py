from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.models import Transaction

def create_transaction(db: Session, player_id, amount, transaction_type, reason):
    transaction = Transaction(player_id=player_id, amount=amount, transaction_type=transaction_type, reason=reason)
    db.add(transaction)