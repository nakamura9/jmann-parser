import pandas as pd
import re
import json
import math 
from product_parser import get_data as gd

NODES = 0

def process_q(val):
    # skip nan values
    if (isinstance(val, float) and math.isnan(val)) or \
            re.match("^ +$", val):
        return
    
    data = { 'description': (val) }

    if re.match("^.*ESC.*$|^.*esc.*$", val):
        data['options'] = None
    
    elif re.match(".*inch", val):
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
            full = curr.pattern + ' *' + full
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
            
        print(curr.full_pattern)
            
    print(NODES)
    with open('trie.json', 'w') as f:
        json.dump(root.as_dict(), f)

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
            
                            
if __name__ == '__main__':
    # main()
    test_parse_tree()
    
    
        