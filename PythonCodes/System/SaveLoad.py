import json
import PythonCodes.Chunk as Chunk
from cryptography.fernet import Fernet

class SaveLoad:

    def saveGame(self,chunk):
        value = {
            "chunkInfo" : chunk.toDic()
        }
        value = json.dumps(value).encode("utf-8")
        key = Fernet.generate_key()
        f = Fernet(key)
        encodeValue = f.encrypt(value)
        saveValue = {
            "key" : str(key,encoding="utf-8"),
            "saveData" : str(encodeValue,encoding="utf-8")
        }
        with open('./Saves/save.txt',"w") as file:
            json.dump(saveValue,file)

    def loadGame(self):
        value = ""
        with open('./Saves/save.txt',"r") as file:
            value = file.read()
        jsonValue = json.loads(value)

        key = jsonValue["key"]
        f = Fernet(key)
        loadData = jsonValue["saveData"]
        loadData = f.decrypt(loadData)
        return loadData