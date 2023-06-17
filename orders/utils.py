import datetime


def generateOrder_number(pk):
    current_date_time = datetime.datetime.now().strftime(
        "%Y%m%d%H%M%S"
    )  # 2022-06-13-11-20
    order_number = current_date_time + str(pk)
    return order_number
