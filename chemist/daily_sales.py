import random
import pandas as pd


class SalesReport:
    def simulate_sales_data(date, df):
        # set hot categories
        extrem_hot_categories = ["pain relief"]
        hot_categories = ["sunscreen", "after sun", "allergy"]
        cold_categories = ["infant formula", "thermometer", "probiotics", 
                           "fish oil", "pregnancy test",]
        hot_keywords = ["deodorant"]

        # way to determine popularity level
        def classify_popularity(row):
            # base on categories
            if row['category'] in extrem_hot_categories:
                return "extrem"
            elif row['category'] in hot_categories:
                return "hot"
            elif row['category'] in cold_categories:
                return "cold"
            # base on product's name
            elif any(world in row['product_name'] for world in hot_keywords):
                return "hot"
            # others
            else:
                return "normal"

        # mark up popularity
        df['popularity'] = df.apply(classify_popularity, axis=1)

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
            stock_number = row['stock_quantity']
            return random.randint(0, stock_number) if stock_number > 0 else 0
            
        daily_list['sold'] = daily_list.apply(generate_sales, axis=1)

        for _, row in daily_list.iterrows():
            df.loc[df['sku'] == row['sku'], 'sold'] = row['sold']

        # weight field is only for simulation but nothing else
        df.drop(columns=['weight'], inplace=True)

        return df