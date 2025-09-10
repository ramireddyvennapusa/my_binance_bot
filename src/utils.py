# src/utils.py
import logging
from logging.handlers import RotatingFileHandler
from decimal import Decimal, InvalidOperation

LOGFILE = "bot.log"

def setup_logger():
    logger = logging.getLogger("binance_bot")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = RotatingFileHandler(LOGFILE, maxBytes=5_000_000, backupCount=3)
        fmt = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        handler.setFormatter(fmt)
        logger.addHandler(handler)
    return logger

def validate_symbol(symbol: str):
    if not symbol or not isinstance(symbol, str):
        raise ValueError("Symbol must be a non-empty string (e.g., BTCUSDT)")
    return symbol.upper()

def validate_quantity(q):
    try:
        qd = Decimal(str(q))
    except InvalidOperation:
        raise ValueError("Quantity must be numeric")
    if qd <= 0:
        raise ValueError("Quantity must be > 0")
    return float(qd)

def validate_price(p):
    try:
        pd = Decimal(str(p))
    except InvalidOperation:
        raise ValueError("Price must be numeric")
    if pd <= 0:
        raise ValueError("Price must be > 0")
    return float(pd)
