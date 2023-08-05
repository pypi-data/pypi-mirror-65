import logging
import sys
import time

import click
from investing import Investing
from sendtext import SendText

__version__ = "0.0.3"


def run(
    instrument: Investing,
    send_message: SendText,
    lower: float,
    upper: float,
    threshold: float,
) -> tuple:
    instrument.fetch()
    logger.debug("Fetched page successfully.")

    price = instrument.price()
    logger.debug(f"Price of {instrument.name} is ${price}.")

    if price >= upper or price <= lower:
        logger.info(f"Price {price} breached price band [{lower}, {upper}].")
        logger.debug(f"Resetting price band with threshold value {threshold}.")
        upper = price * (1 + threshold / 10000)
        lower = price * (1 - threshold / 10000)
        logger.info(f"Resetting price band to [{lower}, {upper}].")
        logger.debug("Sending text.")
        send_message.send(f"{instrument.name} price is {price}.")

    return (lower, upper)


@click.command(
    context_settings=dict(help_option_names=["-h", "--help"]),
    options_metavar="[options...]",
)
@click.argument("to_num", metavar="[to number]")
@click.argument("from_num", metavar="[from number]")
@click.argument("market", metavar="[market]")
@click.argument("contract", metavar="[contract]")
@click.argument("priceband", metavar="[priceband]")
@click.option("--symbol", "-s", help="Contract symbol. [default: contract]")
@click.option(
    "--threshold", "-t", help="Threshold in bps.", default=100.0, show_default=True
)
@click.option(
    "--interval",
    "-i",
    help="Interval to perform check (mins).",
    default=1.0,
    show_default=True,
)
@click.option(
    "--sub-market", "-m", help="E.g. crypto is market and bitcoin is sub market."
)
@click.option("--debug", "-d", is_flag=True, help="Print debug messages.")
def main(
    to_num,
    from_num,
    interval,
    threshold,
    symbol=None,
    market=None,
    contract=None,
    priceband=None,
    sub_market=None,
    debug=None,
):
    """Utiltiy script to notify if instrument price fluctuates out of price band.
    """
    if debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Logging set to debug")

    lower, upper = list(map(float, priceband.split("-")))

    if sub_market:
        end_point = market + "/" + sub_market + "/" + contract
    else:
        end_point = market + "/" + contract

    logger.debug(f"{end_point} end point will be queried.")

    instrument = Investing(end_point, symbol)
    text_client = SendText(from_num, to_num)

    while True:
        try:
            lower, upper = run(instrument, text_client, lower, upper, threshold)
            time.sleep(60 * interval)
        except KeyboardInterrupt:
            logger.info("Caught interrupt, exiting...")
            sys.exit()


if __name__ == "__main__":
    log_handler = logging.StreamHandler()
    log_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s [%(levelname)5s] %(funcName)4s() - %(message)s",
            "%Y-%m-%d %H:%M:%S",
        )
    )
    logger = logging.getLogger(__name__)
    logger.addHandler(log_handler)
    logger.setLevel(logging.INFO)

    main()
