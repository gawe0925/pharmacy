import random
import pandas as pd
from chemist.models import Product, DailySales


class SalesReport:
    def simulate_sales_data(date, df):
        # map weight base on popularity
        weight_map = {'extrem': 2.5, 'hot': 2, 'normal': 1.5, 'cold': 1}
        df['weight'] = df['popularity'].map(weight_map)

        # make a back up df
        df = df.copy()
        df['sold'] = 0

        # Randomly select the number of SKUs to sell today
        num_skus_to_sell = int(random.uniform(80, 180))

        def generate_sales_number(df, skus):
            # pick a list of random products but not repeat
            selected_skus = df['sku'].sample(n=skus, weights=df['weight'], replace=False).unique()
            # copy a new datafram from df
            return df[df['sku'].isin(selected_skus)].copy()
        
        daily_list = generate_sales_number(df, num_skus_to_sell)

        def generate_sales(row):
            stock_number = row['stock_o']

            if row['popularity'] == 'extrem':
                return random.randint(10, stock_number) if stock_number >= 70 else random.randint(0, stock_number)
            elif row['popularity'] == 'hot':
                if stock_number >= 50:
                    return random.randint(5, 50)
                return random.randint(0, stock_number) if stock_number > 0 else 0
            elif row['popularity'] == 'normal':
                if stock_number >= 20:
                    return random.randint(0, 20)
                return random.randint(0, stock_number) if stock_number > 0 else 0
            elif row['popularity'] == 'cold':
                if stock_number >= 5:
                    return random.randint(0, 5)
                return random.randint(0, stock_number) if stock_number > 0 else 0
            
        daily_list['sold'] = daily_list.apply(generate_sales, axis=1)

        for _, row in daily_list.iterrows():
            df.loc[df['sku'] == row['sku'], 'sold'] = row['sold']

        # weight field is only for simulation but nothing else
        df.drop(columns=['weight'], inplace=True)

        def update_stock_numbers(row):
            # stock_e = stock_o - sold
            return row['stock_o'] - row['sold']

        df['stock_e'] = df.apply(update_stock_numbers, axis=1)

        ps = Product.objects.filter(sku__in=df['sku'].to_list()).distinct()
        p_dict = {p.sku: p for p in ps}

        day_list = []
        for _, row in df.iterrows():
            product = p_dict.get(row['sku'])
            if product:
                day_list.append(
                    DailySales(
                        date=date,
                        product=product,
                        stock_o=row['stock_o'],
                        stock_e=row['stock_e'],
                        sold=row['sold'],
                        incoming_stock=row['incoming_stock']
                    )
                )

        DailySales.objects.bulk_create(day_list)
        print({"message": "DailySales have been created"})

        df['incoming_stock'] = 0

        return df