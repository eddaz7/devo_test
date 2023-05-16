import time
import uuid
from datetime import datetime
import sys
import random

from devo.sender import Sender, SenderConfigSSL

from utils import get_random_int, get_string_uuid
from simple_payments import SimplePayments


def init_connection() -> Sender:
    """
    Initialize the connection to Devo
    """

    engine_config = SenderConfigSSL(address=("collector-eu.devo.io", 443),
                                    key="payments_hub@signalit.key", cert="payments_hub@signalit.crt",
                                    chain="chain.crt")

    con = Sender(engine_config)

    return con


def event_generator(con: Sender) -> None:
    """
    Sends the events in an infinite loop, waits sleep_time_seconds to send the next batch.
    Comment or uncomment the different event sender to send what you want.
    """
    sleep_time_seconds = 0.1
    tag = "my.app.streaming.test1"
    count = 0
    while True:
        send_single_payment(con, tag)
        # full_payment(con, tag)
        # send_discrepancies

        # for logging
        time.sleep(sleep_time_seconds)
        count += 1
        if count % 10_000 == 0:
            print(count)


def send_single_payment(con: Sender, tag: str):
    """
    Sends one single payment choosing from the events list at random.
    """
    events = ["received", "initiated", "settled", "finalized"]
    currentDateAndTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    con.send(tag=tag, msg=f"{str(uuid.uuid4())},{random.choice(events)},{get_random_int(4)},{currentDateAndTime}")


def send_full_payment(con: Sender, tag: str) -> None:
    """
    Sends one full payment with the same id
    """
    client_id = get_string_uuid()
    amount = get_random_int(4)
    sleep_list = [x for x in range(10)]
    con.send(tag=tag, msg=f"{client_id},received,{amount},{time.time()}")
    time.sleep(0.1)
    con.send(tag=tag, msg=f"{client_id},initiated,{amount},{time.time()}")
    time.sleep(0.1)
    con.send(tag=tag, msg=f"{client_id},settled,{amount},{time.time()}")
    time.sleep(0.1)
    con.send(tag=tag, msg=f"{client_id},finalized,{amount},{time.time()}")


def send_discrepancies(con: Sender, disc_table_1_tag: str, disc_table_2_tag: str) -> None:
    """
    Sends 7 payments to one table and 7 to the other table. 3 payments are duplicated
    """
    sp = SimplePayments("2023-04-23 00:00:00", 10)
    payments = sp.generate_one_event_payments_list("finalized")
    table1 = payments[:7]
    table2 = payments[3:]
    for payment in table1:
        con.send(tag=disc_table_1_tag, msg=payment)
    for payment in table2:
        con.send(tag=disc_table_2_tag, msg=payment)
    print("10 payments sent")


def run_loop(con: Sender) -> None:
    """
    Exit with ctrl+C
    """
    try:
        print("Sending events...")
        event_generator(con)
    except KeyboardInterrupt:
        print("Connection closed")
        con.close()
        sys.exit()


if __name__ == "__main__":
    con = init_connection()
    run_loop(con)