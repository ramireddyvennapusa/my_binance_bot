# src/advanced/twap.py
import time
from src.binance_client import get_client
from src.utils import setup_logger, validate_symbol, validate_quantity

logger = setup_logger()

def execute_twap(symbol: str, side: str, total_quantity, chunks=5, interval_seconds=10):
    symbol = validate_symbol(symbol)
    quantity = validate_quantity(total_quantity)
    side = side.upper()
    if side not in ("BUY","SELL"):
        raise ValueError("side must be BUY or SELL")
    client = get_client()

    qty_per_chunk = float(quantity) / int(chunks)
    results = []
    logger.info(f"Starting TWAP: {symbol} {side} total={quantity} chunks={chunks} interval={interval_seconds}s")
    for i in range(int(chunks)):
        logger.info(f"TWAP chunk {i+1}/{chunks}: qty={qty_per_chunk}")
        try:
            res = client.futures_create_order(
                symbol=symbol,
                side=side,
                type="MARKET",
                quantity=qty_per_chunk
            )
            results.append(res)
        except Exception as e:
            logger.exception("Error placing TWAP chunk order")
            raise
        if i < chunks-1:
            time.sleep(interval_seconds)
    logger.info("TWAP completed")
    return results
