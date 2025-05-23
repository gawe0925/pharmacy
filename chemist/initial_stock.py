import random
import pandas as pd


class InitialStocks:
    def initial_stock():
        # 品類、單位與規格
        PRODUCT_LIB = [
            # department,        category,           [name],                    [unit],           [sizes],      [cost range]        [mou]
            ("otc medicine",    "pain relief",      ["panadol paracetamol", "nurofen ibuprofen", "aspirin"], ["tablets"], [24, 48, 60], (7, 12), (12)),
            ("otc medicine",    "cold & flu",       ["vicks cough syrup", "otrivin nasal spray"], ["ml"], [100, 200], (8, 15), (6)),
            ("otc medicine",    "cold & flu",       ["codral cold tablets", "codral day and night tablets"], ["tablets"], [10, 20, 30], (7, 15), (12)),
            ("otc medicine",    "allergy",          ["zyrtec antihistamine", "claratyne", "telfast"], ["tablets"], [10, 30], (6, 12), (12)),

            ("vitamins & supplements", "vitamin c", ["bio c", "redoxon vitamin c", "nature's way vitamin c"], ["tablets"], [30, 60, 100], (12, 25), (3)),
            ("vitamins & supplements", "fish oil", ["blackmores fish oil", "swisse fish oil"], ["capsules"], [60, 100, 200], (25, 30), (3)),
            ("vitamins & supplements", "probiotics", ["life-space probiotic"], ["capsules"], [30, 60], (15, 22), (3)),

            ("personal care",   "oral care",        ["colgate toothpaste", "oral-b toothpaste"], ["g"], [75, 150, 250], (5, 15), (6)),
            ("personal care",   "skin care",        ["cetaphil moisturiser"], ["ml"], [100, 200, 500], (15, 28), (3)),
            ("personal care",   "personal hygiene", ["rexona deodorant", "palmolive body wash"], ["ml"], [100, 250, 400], (5, 18), (3)),

            ("sun & insect care", "sunscreen", ["banana boat spf50+", "cancer council sunscreen"], ["ml"], [100, 200, 400], (18, 25), (3)),
            ("sun & insect care", "after sun", ["sunsense after sun gel", "aloe vera after sun"], ["ml"], [100, 200], (8, 16), (3)),

            ("medical devices & supplies", "thermometer", ["omron digital thermometer"], ["piece"], [1], (7, 13), (1)),
            ("medical devices & supplies", "first aid", ["elastoplast bandage"], ["strips"], [10, 20, 30], (4, 10), (6)),

            ("baby & child",    "baby wipes",       ["huggies baby wipes", "curash baby wipes"], ["wipes"], [40, 80, 100], (6, 18), (3)),
            ("baby & child",    "infant formula",   ["aptamil gold", "s26 gold"], ["g"], [900], (30, 39), (1)),

            ("women’s health",  "sanitary pads",    ["libra pads", "always ultra thin"], ["pads"], [12, 16, 24, 30], (8, 18), (6)),
            ("women’s health",  "tampons",          ["tom organic tampons"], ["tampons"], [16, 32], (6, 13), (6)),
            ("women’s health",  "pregnancy test",   ["clearblue pregnancy test"], ["piece"], [1, 2], (18, 22), (1)),
        ]

        # set hot categories
        extrem_hot_categories = ["pain relief"]
        hot_categories = ["sunscreen", "after sun", "allergy"]
        cold_categories = ["infant formula", "thermometer", "probiotics", 
                           "fish oil", "pregnancy test",]
        hot_keywords = ["deodorant"]

        # way to determine popularity level
        def classify_popularity(cat, name):
            # base on categories
            if cat in extrem_hot_categories:
                return "extrem"
            elif cat in hot_categories:
                return "hot"
            elif cat in cold_categories:
                return "cold"
            # base on product's name
            elif any(word in name for word in hot_keywords):
                return "hot"
            # others
            else:
                return "normal"
        
        def gen_stock_by_po(po):
            if po == "extrem":
                return random.randint(60, 120)
            elif po == "hot":
                return  random.randint(30, 60)
            elif po == "normal":
                return  random.randint(10, 30)
            elif po == "cold":
                return  random.randint(1, 10)

        all_rows = []
        idx = 1
        while len(all_rows) < 400:
            for (dept, cat, prods, units, sizes, cost, mo) in PRODUCT_LIB:
                for name in prods:
                    size = random.choice(sizes)
                    unit = random.choice(units)
                    cost_price = round(random.uniform(cost[0], cost[1]), 2)
                    retail_price = round(cost_price * random.uniform(1.2, 1.6), 2)
                    popularity = classify_popularity(cat, name)
                    stock_o = gen_stock_by_po(popularity)

                    row = {
                        "sku": f"{name.split()[0][:3].upper()}{size}{unit[:1].upper()}-{idx:03d}",
                        "product_name": f"{name} {size} {unit}",
                        "category": cat,
                        "department": dept,
                        "unit": unit,
                        "cost_price": cost_price,
                        "retail_price": retail_price,
                        "popularity": popularity,
                        "stock_o": stock_o,
                        "stock_e": stock_o,
                        "sold": 0,
                        "sug_reorder": 0,
                        "mou": mo,
                        "incoming_stock": 0
                    }

                    all_rows.append(row)
                    idx += 1
                    if len(all_rows) >= 400:
                        break
                if len(all_rows) >= 400:
                    break
            if len(all_rows) >= 400:
                break

        df = pd.DataFrame(all_rows)

        return df