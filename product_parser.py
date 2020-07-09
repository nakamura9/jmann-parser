import pandas as pd

# NB table has ~29000 rows
# dataset has 21533 unique products

def get_data():
    data = pd.read_excel('all_prods.xlsx')
    l = []
    for i, row in data.iterrows():
        l.append(row.short_desc)
    
    return l

def get_unique_codes():
    data = pd.read_excel('all_prods.xlsx')
    dataset = set()
    for i, row in data.iterrows():
        dataset.add(row.short_desc)

    return dataset
def main():
    pass

if __name__ == "__main__":
    main()