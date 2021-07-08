import Main2 
import ReadMuonsFromCSV as reader

output = Main2.MuonGen2(100,'Outputer.csv')

data = reader.ReadMuonsFromCSV('Outputer.csv')
print(data)

