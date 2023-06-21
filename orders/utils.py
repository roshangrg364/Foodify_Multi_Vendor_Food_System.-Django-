import datetime
import simplejson as json


def generateOrder_number(pk):
    current_date_time = datetime.datetime.now().strftime(
        "%Y%m%d%H%M%S"
    )  # 2022-06-13-11-20
    order_number = current_date_time + str(pk)
    return order_number


def get_total_by_vendor_id(order, vendorid):
    total_data = json.loads(
        order.total_data
    )  # json format {"vendor_id":{subtotal:[{"tax_type":"GST","tax_percentage":13,"tax_amount":300]}
    data = total_data.get(str(vendorid))
    sub_total = 0
    tax = 0
    tax_data = []
    for key, val in data.items():
        sub_total += float(key)
        tax_data = val
    for tax_value in tax_data:
        tax += float(tax_value["tax_amount"])

    grand_total = sub_total + tax

    data = {
        "tax_data": tax_data,
        "sub_total": sub_total,
        "total_tax": tax,
        "grand_total": grand_total,
    }
    return data
