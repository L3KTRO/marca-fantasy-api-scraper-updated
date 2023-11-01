import json

file = "./mis_ligas/012793678/news.json"
filemanager = "./mis_ligas/012793678/5154794_PabloRB7.json"

filemanager_content = json.loads(open(filemanager, "r").read())

content = json.loads(open(file, "r").read())
nick = "PabloRB7"
filtrada = list(filter(lambda item: nick in item["msg"], content))

types = {
    "BUY": 100,
    "SELL": 200,
    "CLAUSE": 210,
    "PSOE": 300,
    "POSITIVE_YIELD": 400,
    "NEGATIVE_YIELD": 500
}

class Operation():
    def __init__(self, msg) -> None:
        self.msg = msg
        self.list = msg.split(" ")

    def type(self):
        if self.list[0] == nick:
            match self.list[2]:
                case "comprado":
                    return types["BUY"]
                case "vendido":
                    return types["SELL"]
                case "ganado":
                    return types["PSOE"]
                case "cedido":
                    return types["POSITIVE_YIELD"]
        else:
            match self.list[2]:
                case "cedido":
                    return types["NEGATIVE_YIELD"]
                case _:
                    return types["CLAUSE"]
        
    def price(self) -> int:
        match self.type():
            case 300: # PSOE
                return int(str(self.list[3]).replace(".", ""))
            case _:
                return int(str(self.list[-2]).replace(".", ""))
    
    def player(self):
        if self.type() == types["PSOE"]:
            return None
        
        return self.list[4]
    
    def passive(self):
        match self.type():
            case 300: # PSOE
                return None
            case 210: # CLAUSE
                return self.list[0]
            case _: # OTHER
                return self.list[-4]
        

initial = 100000000
por_pfsy = filemanager_content["teamPoints"] * 100000

saldo = initial + por_pfsy
valor_equipo = int(filemanager_content["teamValue"])

for item in filtrada:
    if item["title"] == "Operación de mercado" or item["title"] == "11 ideal":
        op = Operation(item["msg"])
        match op.type():
            case 100:
                saldo -= op.price()
            case 200:
                saldo += op.price()
            case 210:
                saldo += op.price()
            case 300:
                saldo += op.price()
            case 400:
                saldo += op.price()
            case 500:
                saldo -= op.price()

print(f"Saldo potencial (sin contar clausulas): {saldo:,} €")
print(f"Valor total (valor de equipo + saldo potencial): {(saldo+valor_equipo):,} €")