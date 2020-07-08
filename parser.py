import pandas as pd
import re
import json
import math 

data = pd.read_excel('prod_types.xlsx')

q1_options = set()
q2 = []
q3 = []
q4 = []
q5 = []
q6 = []
q7 = []

{
    'description': 'text',
    'options': []
}

def process_q(val):
    # skip nan values
    if (isinstance(val, float) and math.isnan(val)) or \
            re.match("^ +$", val):
        return
    
    
    data = {
        'description': (val),
        'children': []
        }

    if re.match("^.*ESC.*$|^.*esc.*$", val):
        data['options'] = None
    
    elif re.match(".*inch", val):
        data['options'] = 'str'
        
    elif re.match(".*[S|s]ize", val)  \
            or re.match("Width|Thickness|Pitch|Quantity|litres|code|Height|Steps|.*Number|.*Numeric|Ratio|Length|.*Degrees|.*[N|n]o\.", val):
        data['options'] = 'num'
    
    elif re.match(".*=", val):
        opt_list = re.findall('[\w]{1,3}[ ]{0,1}=', val)
        data['options'] = [i.strip("= ") for i in opt_list]
    
    else: 
        data['options'] = 'str'
        
    return data

mapping = {}

# class RootNode():
#     branches = {}
#     def add_branch(self, node):
#         if not self.branches.get(node.name):
#             self.branches[node.name] = node
            
#     def add_child(self, node):
#         pass
    
# class BranchNode():
#     def __init__(self, name, department):
#         self.name = name
#         self.department = department
#         self.children = []

# class LeafNode():
#     def __init__(self, description, parent, level):
#         self.description = description
#         self.root = parent
#         self.level = level
#         self.parse_options()
        
#     def as_dict(self):
#         return {
#             'description': self.description,
#             'options': self.options,
#             'children': self.children,
#             'root': self.parent,
#             'level': self.level
#         }
        
    
#     def parse_options(self):
#         self.options = process_q(self.description)['options']
        
    

for i, item in data.iterrows():
    q1_options.add(item.product_type)
    mapping[item.product_type] = mapping.get(item.product_type, [])
    mapping[item.product_type].append(process_q(item.size_1_descr))
    
    q2.append(process_q(item.size_1_descr))
    q3.append(process_q(item.size_2_descr))
    q4.append(process_q(item.size_3_descr))
    q5.append(process_q(item.size_4_descr))
    q6.append(process_q(item.size_5_descr))
    q7.append(process_q(item.size_6_descr))
    
    
with open('q1.txt', 'w') as f:
    f.writelines([str(i) + '\n' for i in q1_options])
    
    
with open('q2.json', 'w') as f:
    json.dump(q2, f)
    
with open('q3.json', 'w') as f:
    json.dump(q3, f)
    
with open('q4.json', 'w') as f:
    json.dump(q4, f)
    
with open('q5.json', 'w') as f:
    json.dump(q5, f)
    
with open('q6.json', 'w') as f:
    json.dump(q6, f)
    
with open('q7.json', 'w') as f:
    json.dump(q7, f)