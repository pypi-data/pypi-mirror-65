import pandas as pd
import re, csv
import time
import argparse

parser = argparse.ArgumentParser(description="ext-sum.py is intended to be a small utillity script that gives a few greate stats on your daytrading results",)
parser.add_argument('file', metavar="f", nargs=1, help="path to your ETX capital histroy csv file")

args = parser.parse_args()

with open(args.file[0], mode="r+", encoding="utf-16-le") as orig:
  with open('.temp.csv', mode="w+", encoding="utf-16-le") as temp:
    lines = orig.readlines()
    lines[0] = lines[0].replace("marked\thandling\tspil\tvaluta\tÅben\tLuk\tF/T\tNetto F/T\tÅbnet\tLukket","marked\thandling\tspil\tvaluta\tÅben\tLuk\tF/T\tNetto F/T\tÅbnet\tLukket\tdummy")
    i = 0
    for line in lines:
      i += 1
      temp.write(line)

  #Load's data
  df_list = []
  chunksize=200
  #TODO consider using tqdm
  for df_chunk in pd.read_csv('.temp.csv', verbose=True, header=0, sep="\t", encoding="utf-16-le", chunksize=chunksize, quoting=csv.QUOTE_NONE):
    
    #Create a column for opening date, used to join on date
    df_chunk['opening_date'] = pd.to_datetime(df_chunk['Åbnet'], format="%d/%m/%Y %H:%M:%S")
    df_chunk['opening_date'] = df_chunk['opening_date'].map(lambda x: x.strftime("%Y-%m-%d"))

    df_list.append(df_chunk)

  #join all Dataframes
  df = pd.concat(df_list)
  del df_list



  df['points'] = df.apply(lambda x: x['Luk'] - x['Åben'] if x['handling'] == "Buy" else x['Åben'] - x['Luk'], axis=1)


  # df['long_points'] = df['Luk'].where(df['handling'] == "Buy") - df['Åben'].where(df['handling'] == "Buy")
  # df['short_points'] = df['Åben'].where(df['handling'] == "Sell") - df['Luk'].where(df['handling'] == "Sell")
  # df['points'] = df['short_points']+ df['long_points']



  #Get's the number of transactions pr. day
  print(df.groupby(['opening_date','marked']).agg(
    Trades=('handling', "count"),
    Result=('F/T', sum),
    points=('points', sum)
  ))

  #Get's the $Monyey result of the day
  # print(df.groupby('opening_date')['F/T'].sum())



  # print(df)
  
  #Get's the point result of the day

  # print(df.to_string())
