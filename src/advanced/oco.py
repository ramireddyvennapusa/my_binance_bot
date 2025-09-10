# src/advanced/oco.py
# OCO on futures (simulate by placing TP limit and SL stop-market; poll for fills)
import time
from src.binance_client import get_client
from src.utils import setup_logger, validate_symbol, validate_quantity, validate_price

logger = setup_logger()

POLL_INTERVAL = 2.0

def place_oco(symbol: str, side: str, quantity, take_profit_price, stop_loss_price):
    symbol = validate_symbol(symbol)
    quantity = validate_quantity(quantity)
    take_profit_price = validate_price(take_profit_price)
    stop_loss_price = validate_price(stop_loss_price)
    side = side.upper()
    if side not in ("BUY","SELL"):
        raise ValueError("side must be BUY or SELL")

    client = get_client()
    logger.info(f"Placing OCO (simulated): {symbol} {side} qty={quantity}, TP={take_profit_price}, SL={stop_loss_price}")

    # Determine order sides: If initial is BUY, TP is SELL; if initial is SELL, TP is BUY
    tp_side = "SELL" if side == "BUY" else "BUY"
    sl_side = "SELL" if side == "BUY" else "BUY"

    try:
        # Place take-profit limit order
        tp_order = client.futures_create_order(
            symbol=symbol,
            side=tp_side,
            type="LIMIT",
            quantity=quantity,
            price=str(take_profit_price),
            timeInForce="GTC"
        )
        logger.info(f"TP order placed: {tp_order}")

        # Place stop-market order for stop loss
        sl_order = client.futures_create_order(
            symbol=symbol,
            side=sl_side,
            type="STOP_MARKET",
            stopPrice=str(stop_loss_price),
            closePosition=False,
            quantity=quantity
        )
        logger.info(f"SL order placed: {sl_order}")

        tp_id = tp_order.get("orderId")
        sl_id = sl_order.get("orderId")

        # Poll orders for fills - in real implementation use websocket/callback
        while True:
            time.sleep(POLL_INTERVAL)
            tp_status = client.futures_get_order(symbol=symbol, orderId=tp_id)
            sl_status = client.futures_get_order(symbol=symbol, orderId=sl_id)
            logger.info(f"TP status: {tp_status.get('status')}; SL status: {sl_status.get('status')}")
            if tp_status.get("status") == "FILLED":
                # Cancel SL
                client.futures_cancel_order(symbol=symbol, orderId=sl_id)
                logger.info("TP filled -> cancelled SL")
                return {"filled": "TP", "tp": tp_status, "sl": sl_status}
            if sl_status.get("status") == "FILLED":
                # Cancel TP
                client.futures_cancel_order(symbol=symbol, orderId=tp_id)
                logger.info("SL filled -> cancelled TP")
                return {"filled": "SL", "tp": tp_status, "sl": sl_status}
            # Continue polling
    except Exception as e:
        logger.exception("Error placing OCO orders")
        raise
