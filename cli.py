# cli.py
import argparse
import os
from src.utils import setup_logger
from src.market_orders import place_market_order
from src.limit_orders import place_limit_order
from src.advanced.stop_limit import place_stop_limit
from src.advanced.oco import place_oco
from src.advanced.twap import execute_twap
from src.advanced.grid import setup_grid

logger = setup_logger()

def main():
    parser = argparse.ArgumentParser(prog="binance-futures-bot", description="CLI for Binance USDT-M Futures Order Bot")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # market
    p_market = sub.add_parser("market", help="Place market order")
    p_market.add_argument("symbol")
    p_market.add_argument("side", choices=["BUY","SELL"])
    p_market.add_argument("quantity")

    # limit
    p_limit = sub.add_parser("limit", help="Place limit order")
    p_limit.add_argument("symbol")
    p_limit.add_argument("side", choices=["BUY","SELL"])
    p_limit.add_argument("quantity")
    p_limit.add_argument("price")

    # stop-limit
    p_stop = sub.add_parser("stop_limit", help="Place stop-limit order")
    p_stop.add_argument("symbol")
    p_stop.add_argument("side", choices=["BUY","SELL"])
    p_stop.add_argument("quantity")
    p_stop.add_argument("stop_price")
    p_stop.add_argument("limit_price")

    # oco
    p_oco = sub.add_parser("oco", help="Place simulated OCO (TP + SL) - polling based")
    p_oco.add_argument("symbol")
    p_oco.add_argument("side", choices=["BUY","SELL"])
    p_oco.add_argument("quantity")
    p_oco.add_argument("take_profit")
    p_oco.add_argument("stop_loss")

    # twap
    p_twap = sub.add_parser("twap", help="Execute TWAP")
    p_twap.add_argument("symbol")
    p_twap.add_argument("side", choices=["BUY","SELL"])
    p_twap.add_argument("quantity")
    p_twap.add_argument("--chunks", type=int, default=5)
    p_twap.add_argument("--interval", type=int, default=10)

    # grid
    p_grid = sub.add_parser("grid", help="Setup simple grid")
    p_grid.add_argument("symbol")
    p_grid.add_argument("lower")
    p_grid.add_argument("upper")
    p_grid.add_argument("grid_size", type=int)
    p_grid.add_argument("total_quantity")

    args = parser.parse_args()
    try:
        if args.cmd == "market":
            res = place_market_order(args.symbol, args.side, args.quantity)
            print(res)
        elif args.cmd == "limit":
            res = place_limit_order(args.symbol, args.side, args.quantity, args.price)
            print(res)
        elif args.cmd == "stop_limit":
            res = place_stop_limit(args.symbol, args.side, args.quantity, args.stop_price, args.limit_price)
            print(res)
        elif args.cmd == "oco":
            res = place_oco(args.symbol, args.side, args.quantity, args.take_profit, args.stop_loss)
            print(res)
        elif args.cmd == "twap":
            res = execute_twap(args.symbol, args.side, args.quantity, chunks=args.chunks, interval_seconds=args.interval)
            print(res)
        elif args.cmd == "grid":
            res = setup_grid(args.symbol, args.lower, args.upper, args.grid_size, args.total_quantity)
            print(f"Placed {len(res)} orders")
    except Exception as e:
        logger.exception("CLI command failed")
        print("Error:", str(e))

if __name__ == "__main__":
    main()
