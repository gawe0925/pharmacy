import pandas as pd
from datetime import date, timedelta
from chemist.daily_sales import SalesReport
from chemist.initial_stock import InitialStocks
from chemist.order_suggestion import OrderSuggestion
from chemist.models import Product, IncomingOrder, DailySales


class MyPharmacy:

    def common_fuctions(self, date, df):
        # simulate_sales_data will generate daily sales data
        daily_report = SalesReport.simulate_sales_data(date, df)

        daily_objs = [DailySales(**row.to_dict(), date=date) for _, row in daily_report.iterrows()]

        DailySales.objects.bulk_create(daily_objs)
        print(f'DailySales:{date}_has been created')

        suggestions = OrderSuggestion.restock_report(daily_report)

        file_name = f'{date}_order_suggestion.xlsx'
        return suggestions.to_excel(file_name, index=False)
    
    def pharmacy(self, input_df):
        today = date.today()
        products = Product.objects.all()
        
        if not products:
            print('initial pharmacy stocks')
            # through initial_stock function return df of initial stocks
            stock_list = InitialStocks.initial_stock()
            
            stock_objs = [Product(**row.to_dict()) for _, row in stock_list.iterrows()]

            Product.objects.bulk_create(stock_objs)
            print('Inital stock has been generated')
            print("My Pharmacy day - 1")
            return self.common_fuctions(today, stock_list)

        else:
            print('updating exist pharmacy')
            """
            df means the user/admin has reordered some stocks and 
            pass-in order list(excel) with product's reordering quantity number

            through df will update Product's incoming_stock field and 
            generate IncomingOrder table to record each day's order
            """
            if input_df:
                df = pd.read_excel(input_df)
                df.loc[df['sold'] > 0, 'sold'] = 0
                df.loc[df['sug_reorder'] > 0, 'sug_reorder'] = 0
                stock_objs = [Product(**row.to_dict()) for _, row in df.iterrows()]
                # update Product's incoming_stock field
                Product.objects.bulk_update(stock_objs)
                print(f"{today}_ incoming_stock have been updated")

                # create IncomingOrder table
                ps = Product.objects.filter(incoming_stock__gt=0)

                def incomingorder_objs(p):
                    def generate_order_number(product):
                        date_str = date.today().strftime('%Y%m%d')
                        sku = product.sku.upper()[:5]
                        return f"ORD-{date_str}-{sku}"
                    
                    return IncomingOrder(
                        product=p,
                        quantity=p.incoming_stock,
                        order_date=today,
                        expected_arrival=today + timedelta(days=2),
                        supplier='A',
                        order_number=generate_order_number(p)
                    )
                
                order_list = list(map(incomingorder_objs, ps))
                IncomingOrder.objects.bulk_create(order_list)
                print('IncomingOrder have been created')

            else:
                """
                when user/admin not submit or make a new order, then will go through here
                """
                exist_products_list = (Product.objects.all()).values()
                current_stock_df = pd.DataFrame(exist_products_list)
                stock_df = current_stock_df.drop(columns=['id'], inplace=True)
                print(f'{today} _ with no new orders')
                return self.common_fuctions(today, stock_df)
