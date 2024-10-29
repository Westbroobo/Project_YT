"""
Filename:3-3.vehicle_merge.py
Author: Westbroobo
Date: 2024/9/27
"""

import pandas as pd
import textwrap

df_input = pd.read_excel('./Vehicle_2.xlsx')

df_input['Model_Engine'] = df_input['Model'] + '\n' + df_input['Engine'].apply(lambda x: textwrap.indent(x, '    '))
df_input = df_input[['Product Id', 'Make', 'Model_Engine']]
df_input = df_input.groupby(['Product Id', 'Make'], as_index=False, sort=False).agg({'Model_Engine': list})
df_input['Model_Engine'] = df_input['Model_Engine'].apply(lambda x: '\n'.join(x))

df_input['Vehicle'] = df_input['Make'] + '\n' + df_input['Model_Engine'].apply(lambda x: textwrap.indent(x, '    '))
df_input = df_input[['Product Id', 'Vehicle']]
df_input = df_input.groupby('Product Id', as_index=False, sort=False).agg({'Vehicle': list})
df_input['Vehicle'] = df_input['Vehicle'].apply(lambda x: '\n'.join(x))

df_input.to_excel('./Vehicle.xlsx', index=False)
