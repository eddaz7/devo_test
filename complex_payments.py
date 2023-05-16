from datetime import datetime, timedelta

from utils import get_string_uuid, get_random_int


class ComplexPayments:

    def __init__(self, start_date: str, number_of_payments: int):
        self.start_date = start_date
        self.number_of_payments = number_of_payments

    def generate_payments(self):
        with open("complex_payments.csv", "w") as f:
            start_timestamp = datetime.strptime("2023-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")
            for i in range(self.number_of_payments):
                client_id = get_string_uuid()
                amount = get_random_int(4)
                timestamp = start_timestamp + timedelta(minutes=i)
                line = f"""{client_id},received,{amount},{timestamp.strftime("%Y-%m-%d %H:%M:%S")}"""
                f.write(f"{line}\n")
                timestamp = timestamp + timedelta(seconds=1)
                line = f"""{client_id},initiated,{amount},{timestamp.strftime("%Y-%m-%d %H:%M:%S")}"""
                f.write(f"{line}\n")
                timestamp = timestamp + timedelta(seconds=1)
                line = f"""{client_id},settled,{amount},{timestamp.strftime("%Y-%m-%d %H:%M:%S")}"""
                f.write(f"{line}\n")
                timestamp = timestamp + timedelta(seconds=1)
                line = f"""{client_id},finalized,{amount},{timestamp.strftime("%Y-%m-%d %H:%M:%S")}"""
                f.write(f"{line}\n")
