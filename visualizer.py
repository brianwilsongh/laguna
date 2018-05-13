import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np

style.use('ggplot')

stats = {
'Day':[1,2,3,4,5,6,7],
'Cats':[23,73,32,74,24,45,23],
'Food':[3,7,3,6,4,2,1]
}

df = pd.DataFrame(stats).set_index('Day')

# print(df)
# print(df['Cats'])
# print(df['Cats'].tolist()) #reference 1 col
# print(df[['Cats', 'Food']])
# print(np.array(df[['Cats', 'Food']]))

df2 = pd.DataFrame(np.array(df[['Cats', 'Food']]))
# print(df2)

fifty = pd.read_html('https://simple.wikipedia.org/wiki/List_of_U.S._states')
print(fifty[0])
for abbv in fifty[0][1][1:]:
    print(abbv)

























