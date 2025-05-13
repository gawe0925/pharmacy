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
        df_0 = df.copy()

        # Randomly select the number of SKUs to sell today
        num_skus_to_sell = int(random.uniform(80, 180))

        # pick a list of random products
        selected_products = df.sample(n=num_skus_to_sell, 
                                    weights='weight')
        
        # copy a new datafram from df
        daily_list = selected_products.copy()

        def generate_sales(row):
            stock_number = row['stock_quantity']
            return random.randint(1, stock_number) if stock_number > 0 else 0
            
        daily_list['sold'] = daily_list.apply(generate_sales, axis=1)

        # merge daily sales df with origin df on 'sold' column
        sold_list = pd.merge(df_0.drop(columns=['sold']), daily_list[['sku', 'sold']], on='sku', how='left')
        
        # double check if sold numbers is equal to num_skus_to_sell
        if len(df_0) - sold_list['sold'].isna().sum() == num_skus_to_sell:
            sold_list['sold'] = sold_list['sold'].fillna(0)
        else:
            raise ValueError("numbers of sold not match to non sold number, might occur error!")
        
        def update_stock_numbers(row):
            return row['stock_quantity'] - row['sold']

        sold_list['stock_quantity'] = sold_list.apply(update_stock_numbers, axis=1)
        sold_list.loc[sold_list['sold'] > 0, 'sold'] = 0
        # set a file name with current date
        # file_name = f"{date}_stock_status.csv"
        # sold_list.to_csv(file_name, index=False)

        # objs = [Product(**row.to_dict()) for _, row in sold_list.iterrows()]
        # Product.objects.bulk_update(objs)
        # print("updated daily sold numbers")

        return sold_list