# src/advanced/grid.py
from decimal import Decimal
from src.binance_client import get_client
from src.utils import setup_logger, validate_symbol, validate_quantity, validate_price

logger = setup_logger()

def setup_grid(symbol: str, lower_price, upper_price, grid_size, total_quantity):
    symbol = validate_symbol(symbol)
    lower = validate_price(lower_price)
    upper = validate_price(upper_price)
    if upper <= lower:
        raise ValueError("upper_price must be > lower_price")
    grid_size = int(grid_size)
    total_quantity = validate_quantity(total_quantity)
    client = get_client()
    logger.info(f"Setting up grid for {symbol}: {lower} - {upper} with {grid_size} levels, total_qty={total_quantity}")

    # compute levels
    step = (Decimal(str(upper)) - Decimal(str(lower))) / Decimal(str(grid_size))
    qty_per_level = Decimal(str(total_quantity)) / Decimal(str(grid_size))

    created_orders = []
    for i in range(grid_size):
        price = (Decimal(str(lower)) + step * Decimal(i)).quantize(Decimal('0.0001'))
        # Place buy limit orders below market and corresponding sell limit orders above market could be placed by strategy.
        try:
            order = client.futures_create_order(
                symbol=symbol,
                side="BUY",
                type="LIMIT",
                timeInForce="GTC",
                quantity=float(qty_per_level),
                price=str(price)
            )
            created_orders.append(order)
            logger.info(f"Placed grid BUY limit at {price}: {order}")
        except Exception as e:
            logger.exception("Error placing grid order")
            raise
    return created_orders
