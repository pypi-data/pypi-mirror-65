import pickle, hmac
class Universo:
    def __init__(self, name, path):
        self.name=name
        self.path=path
        self.id=self.getHMAC(self.name)
        self.mapa=self.getMap()
        self.indexes = self.getIndexes()
    def getIndexes(self):
        try:
            with open('%s/index_%s'%(self.path,self.id),'rb') as file:
                mapa=pickle.load(file)
                file.close()
            return mapa
        except Exception as ex:
            return {}
    def getHMAC(self, msg):
        hash_mac=hmac.new(self.name.encode('utf-8'))
        return hash_mac.hexdigest()
    def getMap(self):
        try:
            with open('%s/%s'%(self.path,self.id),'rb') as file:
                mapa=pickle.load(file)
                file.close()
            return mapa
        except Exception as ex:
            return {}
    def setMap(self, mapa):
        with open('%s/%s'%(self.path,self.id),'wb') as file:
            pickle.dump(mapa, file)
            file.close()
    def insert(self,conjunto, ente, **kargs):
        _id=self.save(ente)
        id_conjunto=self.getHMAC(conjunto)
        
        if id_conjunto in self.mapa:
            self.mapa[id_conjunto].append(_id)
        else: 
            self.mapa[id_conjunto]=[_id]
        if kargs.get('commit')==True:
            self.commit()
        return len(self.mapa[id_conjunto])
    def select (self, conjunto, query_function=None):
        id_conjunto=self.getHMAC(conjunto)
        
        if not id_conjunto in self.mapa: return []
        
        conjunto=self.mapa[id_conjunto]
        if not query_function:
            for ente_id in conjunto :
                yield (ente_id, self.getEnte(ente_id))
    def getEnte(self, _id):
        with open('%s/%d'%(self.path, _id),'rb') as file:
            ente=pickle.load(file)
            file.close()
            return ente
    def save(self, ente):
        _id=id(ente)
        with open("%s/%s"%(self.path,_id),'wb') as file:
            pickle.dump(ente, file)
            file.close()
        return _id
    def commit(self):
        self.setMap(self.mapa)
        
        