import datetime as dt
import csv

START_BALANCE = 2117.57

EMERGENCY_BUFFER = 500

MONTHLY_BILLS = [
    # name, debit_amount, day_of_month
    ['capone min', 130.00, 2],
    ['citibank min', 35.00, 21],
    ['citizens min', 30.00, 6],
    ['comcast', 69.99, 13],
    ['disney', 13.99, 24],
    ['rent', 1010.00, 1],
    # ['std loan', 37.00, dt.date(0, 1, 0), dt.date(2022, 6, 1],  # TODO
    ['OVH cloud', 7.99, 3],
    ['xfinity mobile', 69.00, 7],
]

WEEKLY_BILLS = [
    # name, debit_amount, timedelta, starting_date
    ['payday', -1096.19, dt.timedelta(weeks=2), dt.date(2022, 5, 27)],
]

ONE_TIME_BILLS = []

TODAY = dt.date.today()


def main():
    bills = get_monthly_bills() + get_weekly_bills()
    bills.sort()
    put_csv(bills)


def get_monthly_bills():
    bills = []
    for bill in MONTHLY_BILLS:
        day = bill[2]
        for month in range(TODAY.month, TODAY.month + 15):
            this_month = (month - 1) % 12 + 1

            if month == this_month:
                year = TODAY.year
            else:
                year = TODAY.year + 1

            bill_date = dt.date(year, this_month, day)
            bills.append((bill_date, bill[1], bill[0]))

    return bills


def get_weekly_bills():
    bills = []
    last_date = dt.date(TODAY.year + 1, ((TODAY.month + 14) % 12 + 1), 1)
    for bill in WEEKLY_BILLS:
        cur_date = bill[3]
        while cur_date < last_date - bill[2]:
            cur_date += bill[2]

            if cur_date < TODAY:
                continue

            bills.append((cur_date, bill[1], bill[0]))

    return bills


def put_csv(bills):
    with open('bills.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(bills)


if __name__ == '__main__':
    main()
