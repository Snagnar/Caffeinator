import argparse
import logging
from src.rfid_reader import RFIDReader
from src.utils import set_logging
from src.wallet_communicator import WalletCommunicator
from src.ui_manager import UIManager

def on_uid(uid: str, wallet_communicator: WalletCommunicator, ui_manager: UIManager) -> None:
    user = wallet_communicator.user_from_uid(uid)
    logging.info(f"activating user: {user}")
    ui_manager.set_active_user(user)


def main(args: argparse.Namespace) -> None:
    set_logging(args.log_file, args.log_level, args.log_stdout)
    logging.info("Starting Coffeemaker cash register thingy")
    rfid = RFIDReader()
    wallet_communicator = WalletCommunicator()
    ui_manager = UIManager()

    ui_manager.on_logout(rfid.reset_last_uid)
    rfid.on_uid(on_uid, args=[wallet_communicator, ui_manager])
    rfid.start()
    ui_manager.ui_loop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Coffemaker cash register")
    parser.add_argument("--log-level", type=str, default="info",
                        choices=["debug", "info", "warning", "error", "critical"],
                        help="log level for logging message output")
    parser.add_argument("--log-interval", type=int, default=100, metavar="N",
                        help="how many batches to wait before logging training status")
    parser.add_argument("--log-file", type=str, default=None,
                        help="output file path for logging. default to stdout")
    parser.add_argument("--log-stdout", action="store_true", default=False,
                        help="toggles force logging to stdout. if a log file is specified, logging will be "
                        "printed to both the log file and stdout")
    args = parser.parse_args()
    main(args)

