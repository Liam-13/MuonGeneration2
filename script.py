import MuonGen 
import ReadMuonsFromCSV2 as reader

output = MuonGen.MuonGen2(100,'Outputer.csv')

data = reader.ReadMuonsFromCSV2('Outputer.csv')
print(data)

