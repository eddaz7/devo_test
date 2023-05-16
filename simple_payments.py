from datetime import datetime, timedelta

from utils import get_string_uuid, get_random_int


class SimplePayments:

    def __init__(self, start_date: str, number_of_payments: int):
        self.start_date = start_date
        self.number_of_payments = number_of_payments

    def generate_one_event_payments_file(self, event: str):
        count = 0
        n = 100_000
        with open(f"simple_payments.csv", "w") as f:
            start_timestamp = datetime.strptime(self.start_date, "%Y-%m-%d %H:%M:%S")
            for i in range(self.number_of_payments):
                timestamp = start_timestamp + timedelta(minutes=i)
                timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                line = f"{get_string_uuid()},{event},{get_random_int(4)},{timestamp}"
                f.write(f"{line}\n")
                count += 1
                if count % n == 0:
                    print(f"{count} de {self.number_of_payments}")

    def generate_one_event_payments_list(self, event: str) -> list[str]:
        count = 0
        n = 100_000
        payments = []
        start_timestamp = datetime.strptime(self.start_date, "%Y-%m-%d %H:%M:%S")
        for i in range(self.number_of_payments):
            timestamp = start_timestamp + timedelta(minutes=i)
            timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            line = f"{get_string_uuid()},{event},{get_random_int(4)},{timestamp}"
            payments.append(line)
            count += 1
            if count % n == 0:
                print(f"{count} de {self.number_of_payments}")
        return payments

    def generate_multiple_event_payments(self):
        count = 0
        n = self.number_of_payments / 10
        with open(f"received.csv", "w") as received,\
             open(f"initiated.csv", "w") as initiated,\
             open(f"settled.csv", "w") as settled,\
             open(f"finalized.csv", "w") as finalized:
            start_timestamp = datetime.strptime(self.start_date, "%Y-%m-%d %H:%M:%S")
            for i in range(self.number_of_payments):
                global_timestamp = start_timestamp + timedelta(minutes=i)
                uuid = get_string_uuid()
                amount = get_random_int(4)

                # Received
                timestamp = global_timestamp + timedelta(seconds=5)
                str_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                line = f"{uuid},received,{amount},{str_timestamp}"
                received.write(f"{line}\n")

                # Initiated
                timestamp = timestamp + timedelta(seconds=5)
                str_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                line = f"{uuid},initiated,{amount},{str_timestamp}"
                initiated.write(f"{line}\n")

                # Settled
                timestamp = timestamp + timedelta(seconds=5)
                str_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                line = f"{uuid},settled,{amount},{str_timestamp}"
                settled.write(f"{line}\n")

                # Finalized
                timestamp = timestamp + timedelta(seconds=5)
                str_timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                line = f"{uuid},finalized,{amount},{str_timestamp}"
                finalized.write(f"{line}\n")

                count += 1
                if count % n == 0:
                    print(f"{count}/{self.number_of_payments}")


if __name__ == "__main__":
    sp = SimplePayments("2023-04-24 00:00:00", 10)
    sp.generate_one_event_payments_file("finalized")
