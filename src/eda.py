import pandas as pd

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 1000)

df = pd.read_csv("data/processed/master_university_dataset.csv")

print("################# SHAPE #######################")
print(df.shape)

print("\n################## COLUMNS ######################")
print(df.columns)

print("\n########################### INFO ###########################")
print(df.info())

print("\n################################# MISSING VALUES ##########################")
print(df.isnull().sum())

print("\n########################################## DESCRIBE ###########################")
print(df.describe().T)

print("\n############################## HEAD ##########################")
print(df.head())
