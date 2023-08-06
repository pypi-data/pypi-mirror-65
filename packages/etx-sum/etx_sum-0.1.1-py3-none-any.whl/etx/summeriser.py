import pandas as pd
import re, csv
import time

class Summary:
  def __init__(self, filePath):
    self.filePath = filePath

  def summarize(self):
    with open(self.filePath, mode="r+", encoding="utf-16-le") as orig:
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

      #Get's the number of transactions pr. day
      print(df.groupby(['opening_date','marked']).agg(
        Trades=('handling', "count"),
        Result=('F/T', sum),
        points=('points', sum)
      ))
