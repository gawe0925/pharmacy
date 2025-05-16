

class OrderSuggestion:
    def restock_report(df):

        def update_stock_numbers(row):
            # stock_e = stock_o - sold
            return row['stock_o'] - row['sold']

        df['stock_e'] = df.apply(update_stock_numbers, axis=1)

        def restock_amount(row):
            if row['popularity'] == 'extrem':
                if row['stock_e'] + row['incoming_stock'] <= 20:
                    return row['mou'] * 20
                elif row['stock_e'] + row['incoming_stock'] <= 50:
                    return row['mou'] * 16
                elif row['stock_e'] + row['incoming_stock'] <= 70:
                    return row['mou'] * 10
                else:
                    return 0
            elif row['popularity'] == 'hot':
                if row['stock_e'] + row['incoming_stock'] <= 20:
                    return row['mou'] * 5
                elif row['stock_e'] + row['incoming_stock'] <= 30:
                    return row['mou'] * 4
                else:
                    return 0
            elif row['popularity'] == 'normal':
                return row['mou'] * 2 if row['stock_e'] + row['incoming_stock'] < 6 else 0
            else:
                # for cold popularity
                return row['mou'] if row['stock_e'] + row['incoming_stock'] < 2 else 0

        # generate reorder suggestions
        df['sug_reorder'] = df.apply(restock_amount, axis=1)

        # sort DataFrame by stock_e in ascending order
        df_sorted = df.sort_values(by='stock_e', ascending=True)

        return df_sorted