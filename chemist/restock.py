from datetime import date
from chemist.models import Product, IncomingOrder


class ReStcok:
    def renew_stock():
        today = date.today()

        products = Product.objects.filter(incoming_stock__gt=0)

        orders = IncomingOrder.objects.select_related('product').filter(
            product__in=products, arrived_check=False, 
            expected_arrival=today, quantity__gt=0)
        
        if not products:
            print({"message": "non incoming stocks need to be update"})
            return False
        if not orders:
            print({"message": "non current vaild coming order"})
            return False

        product_list = []
        order_list = []

        for order in orders:
            product = order.product
            product.stock_quantity += order.quantity
            product.incoming_stock -= order.quantity
            product_list.append(product)

            order.arrived_check = True
            order_list.append(order)

        Product.objects.bulk_update(product_list, ['stock_quantity'])
        print('updated Product table')
        IncomingOrder.objects.bulk_update(order_list, ['arrived_check'])
        print('updated IncomingOrder table')