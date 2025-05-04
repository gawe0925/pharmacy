import pandas as pd

class order_suggestion():
    def restock_report(date, df):

        def update_stock_numbers(row):
            return row['stock_quantity'] - row['sold']

        df['stock_quantity'] = df.apply(update_stock_numbers, axis=1)

        def restock_amount(row):
            if row['popularity'] == 'extrem':
                # extrem popular products recommending order times 12 of mou
                return row['mou'] * 12 if row['stock_quantity'] // 60 == 0 else 0 
            elif row['popularity'] == 'hot':
                # popular products recommending order times 5 of mou
                return row['mou'] * 5 if row['stock_quantity'] // 10 == 0 else 0
                # popular products recommending order times 2 of mou
            elif row['popularity'] == 'normal':
                return row['mou'] if row['stock_quantity'] < 6 else 0
            else:
                # for cold popularity
                return row['mou'] if row['stock_quantity'] < 2 else 0

        # generate reorder suggestions
        df['recommending_stock_number'] = df.apply(restock_amount, axis=1)
        # mark of sold columns
        df.loc[df['sold'] > 0, 'sold'] = 0
        # Sort the DataFrame by the recommending_stock_number column in descending order
        df_sorted = df.sort_values(by='recommending_stock_number', ascending=False)

        file_name = f"{date}_order_suggestion.csv"
        df_sorted.to_csv(file_name, index=False)