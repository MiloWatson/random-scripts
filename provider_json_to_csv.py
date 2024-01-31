import pandas as pd

with open('provider.json', encoding='utf-8') as f:
    df = pd.read_json(f)

df.to_csv('providers.csv', encoding='utf-8', index=False)
