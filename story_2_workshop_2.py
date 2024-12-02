import pandas as pd
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules


data = {'ID':[1,2,3,4,5,6],
       'Onion':[1,0,0,1,1,1],
       'Potato':[1,1,0,1,1,1],
       'Burger':[1,1,0,0,1,1],
       'Milk':[0,1,1,1,0,1],
       'Beer':[0,0,1,0,1,0]}
# print(data)

df = pd.DataFrame(data)
# print(df)

df = df[['ID', 'Onion', 'Potato', 'Burger', 'Milk', 'Beer' ]].astype(bool)
# print(df)

frequent_itemsets = apriori(df[['Onion', 'Potato', 'Burger', 'Milk', 'Beer' ]], min_support=0.50, use_colnames=True)
# print(frequent_itemsets)

num_itemsets = 1
rules = association_rules(frequent_itemsets,num_itemsets, metric='lift', min_threshold=1)
# print(rules)

rules [ (rules['lift'] >1.125)  & (rules['confidence']> 0.8)  ]

