import pandas as pd
import time

# reading the data
start = time.time()

print("Loading data...")
data = pd.read_csv('common_2018.csv',sep=',', decimal='.')

data = data.groupby(['Data','UTM32N_Est','UTM32N_Nord'])[["IdSensore", "Valore"]]

for key, item in data:
    print(data.get_group(key))
    time.sleep(90)