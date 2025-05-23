import pandas as pd
from datetime import date, timedelta
from chemist.daily_sales import SalesReport
from chemist.initial_stock import InitialStocks
from chemist.models import Product, IncomingOrder
from chemist.order_suggestion import OrderSuggestion



class MyPharmacy:

    def common_fuctions(self, date, df):
        # generate daily sales data and store in DailySales
        daily_report = SalesReport.simulate_sales_data(date, df)
        # generate reorder suggestions
        suggestions = OrderSuggestion.restock_report(daily_report)

        return suggestions
    
    def init_pharmacy(self, in_d):
        print('initial pharmacy stocks')
        # through initial_stock function return df of initial stocks
        stock_list = InitialStocks.initial_stock()
        
        stock_objs = [Product(**row.to_dict()) for _, row in stock_list.iterrows()]

        Product.objects.bulk_create(stock_objs)
        print('Inital stock has been generated')
        return self.common_fuctions(in_d, stock_list)

    def non_order(self, in_d):
        """
        when user/admin not submit or make a new order, then will go through here
        """
        exist_products_list = (Product.objects.all()).values()
        current_stock_df = pd.DataFrame(exist_products_list)
        current_stock_df.drop(columns=['id'], inplace=True)
        print(f'{in_d} _ with no new orders')
        return self.common_fuctions(in_d, current_stock_df)

    def with_new_order(self, df, in_d):
        print('updating exist pharmacy')
        """
        df means the user/admin has reordered some stocks and 
        pass-in order list(excel) with product's reordering quantity number

        through df will update Product's incoming_stock field and 
        generate IncomingOrder table to record each day's order
        """

        df.loc[df['sold'] > 0, 'sold'] = 0
        df.loc[df['sug_reorder'] > 0, 'sug_reorder'] = 0
        
        products = Product.objects.filter(sku__in=df['sku'].tolist())
        product_dict = {product.sku: product for product in products}

        incoming_order_objs = []

        def generate_order_number(product):
            date_str = in_d.strftime('%Y%m%d')
            sku = product.sku.upper()[:5]
            return f"ORD-{date_str}-{sku}"

        for _, row in df.iterrows():
            product = product_dict.get(row['sku'])

            if product:
                incoming_order_objs.append(
                    IncomingOrder(
                        product=product,
                        quantity=row['incoming_stock'],
                        order_date=in_d,
                        expected_arrival=in_d + timedelta(days=2),
                        supplier='A',
                        order_number=generate_order_number(product)
                    )
                )

        IncomingOrder.objects.bulk_create(incoming_order_objs)
        print('IncomingOrder has been created')
        
        return self.common_fuctions(in_d, df)
