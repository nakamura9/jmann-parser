import pandas as pd


def get_data():
    data = pd.read_excel('all_prods.xlsx')
    l = []
    for i, row in data.iterrows():
        l.append(row.short_desc)
    
    return l

def main():
    pass

if __name__ == "__main__":
    main()