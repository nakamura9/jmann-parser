import pandas as pd
import re
import json
import math 
from product_parser import get_data as gd, get_unique_codes
from models import Item, Base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///db.sqlite3')
Base.metadata.bind = engine
 
DBSession = sessionmaker(bind=engine)
session = DBSession()

NODES = 0
# fixes 
# - limit spaces to 3 - Done
# - groups should have 0 or more matches not one or more 
# - any description with e.g. must be \w - Done

def process_q(val):
    # skip nan values
    if (isinstance(val, float) and math.isnan(val)) or \
            re.match("^ +$", val):
        return
    
    data = { 'description': (val) }

    if re.match("^.*ESC.*$|^.*esc.*$", val):
        data['options'] = None
    
    elif re.match(".*inch", val) or re.match('.*e\.g.*', val):
        data['options'] = r'(\w+)'
        
    elif re.match(".*[S|s]ize", val)  \
            or re.match("Width|Thickness|Pitch|Quantity|.*litres|code|Height|Steps|Number|Numeric|Ratio|Length|.*Degrees|.*[N|n]o\.", val):
        data['options'] = r'(\d+\.?\d+)'
    
    elif re.match(".*=", val):
        opt_list = re.findall('[\w]{1,3}[ ]{0,1}=', val)
        opt_list = [i.strip("= ") for i in opt_list]
        data['options'] =  "(" + "|".join(opt_list) + ")"
    
    else:
        print('else: ', val)
        data['options'] = r'(\w+)'
        
    return data

class Node():
    def __init__(self, pattern, description):
        global NODES
        self.children = []
        self.pattern = pattern
        self.parent = None
        self.description = description
        NODES += 1
        
    def add_child(self, node):
        self.children.append(node)
        node.parent = self
        
    @property 
    def full_pattern(self):
        curr = self.parent
        full = self.pattern
        while curr is not None:
            full = curr.pattern + ' {0,3}' + full
            curr = curr.parent
            
        return full
    
    def as_dict(self):
        
        return {
            'children': [child.as_dict() for child in self.children],
            'pattern': self.full_pattern,
            'parent': self.parent.pattern if self.parent else None,
            'description': self.description
        }       
    

def main():
    data = pd.read_excel('prod_types.xlsx')
    root = Node(r'^(\d{2})', 'Root Node')
    for i, item in data.iterrows():
        #r'[A-Z]{3,4}'
        lvl_1 = Node("(" + str(item.product_type) + ")", item.product_type)
        root.add_child(lvl_1)
        levels = [
            item.size_1_descr,
            item.size_2_descr,
            item.size_3_descr,
            item.size_4_descr,
            item.size_5_descr,
            item.size_6_descr,
        ]
        curr = lvl_1
        for lvl in levels:
            data = process_q(lvl)
            if not data or data['options'] is None:
                break
            temp = Node(data['options'], data['description'])
            curr.add_child(temp)
            temp.parent = curr
            
            curr = temp
            
    with open('trie.json', 'w') as f:
        json.dump(root.as_dict(), f)


def find_node(val):
    tree = None
    result = []
    with open('trie.json', 'r') as f:
        tree = json.load(f)
        
    print('finding')
    best_match = tree['pattern']
    def node_finder(nodes, best_match, value, res):
        for node in nodes:
            m = re.match(node['pattern'], value)
            if m:
                best_match = node['pattern']
                if re.match(best_match + '$', value):
                    print(node['pattern'])
                    res.append(node)
                    return 
                node_finder(node['children'], best_match, value, res)

    node_finder(tree['children'], best_match, val, result)

    return result[0] if len(result) > 0 else None

def test_parse_tree():
    dataset = gd()
    tree = None
    tokens = {}
    with open('trie.json', 'r') as f:
        tree = json.load(f)
            
    def find_matches(nodes, best_match, value, tokenizer):
        for node in nodes:
            m = re.match(node['pattern'], value)
            if m:
                best_match = node['pattern']
                if re.match(best_match + '$', value):
                    tokenizer[value] = m.groups()
                    return best_match
                find_matches(node['children'], best_match, value, tokenizer)
        
    for item in dataset:
        best_match = tree['pattern']
        best_match = find_matches(tree['children'], best_match, item, tokens)
        
    with open('expanded_descriptions.json', 'w') as f:
        tree = json.dump(tokens, f)
        
    for token in tokens:
        length = len(tokens[token])
        
        session.add(Item(
            name=token or 'None',
            department= tokens[token][0] if length > 0 else None,
            product_type=tokens[token][1] if length > 1 else "Name",
            q1=tokens[token][2] if length > 2 else None,
            q2=tokens[token][3] if length > 3 else None,
            q3=tokens[token][4] if length > 4 else None,
            q4=tokens[token][5] if length > 5 else None,
            q5=tokens[token][6] if length > 6 else None,
            q6=tokens[token][7] if length > 7 else None,
            ))
        
        
    session.commit()
            
def find_unmatched():
    dataset = get_unique_codes()
    unmatched = []
    matched = None
    with open('expanded_descriptions.json', 'r') as f:
        matched = json.load(f)

    for code in dataset:
        if not matched.get(code, None):
            unmatched.append(code)
            
    with open('unmatched.txt', 'w') as fp:
          fp.writelines(str(i) +'\n' for i in unmatched)
            
                            
if __name__ == '__main__':
    # main()
    # test_parse_tree()
    # find_unmatched()
    pass
    
    
        