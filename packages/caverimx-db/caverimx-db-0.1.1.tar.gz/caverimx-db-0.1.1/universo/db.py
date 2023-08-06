import pickle, hmac
class Universo:
    def __init__(self, name, path):
        self.name=name
        self.path=path
        self.id=self.getHMAC(self.name)
        self.mapa=self.loadMap()
        self.indexes = self.loadIndexes()
    def loadIndexes(self):
        try:
            with open('%s/indexes_%s'%(self.path,self.id),'rb') as file:
                mapa=pickle.load(file)
                file.close()
            return mapa
        except Exception as ex:
            return {}
    def saveIndexes(self):
        with open('%s/indexes_%s'%(self.path, self.id), 'wb') as file:
            pickle.dump(self.indexes, file)
            file.close()
        
    def addIndex(self,id_conjunto, atributo, ente_id):
        if id_conjunto in self.indexes:
            if atributo in self.indexes[id_conjunto]:
                self.indexes[id_conjunto][atributo].append(ente_id)
            else:
                self.indexes[id_conjunto][atributo]=[ente_id]
        else: 
            index={atributo:[ente_id]}
            self.indexes[id_conjunto]=index
        
    def createIndex(self, conjunto, atributo, **kargs):
        id_conjunto=self.getHMAC(conjunto)
        indexed_entes={}
        entes = self.select(conjunto)
        for _id,ente in entes:
            if atributo in ente:
                if ente[atributo] in indexed_entes:
                    indexed_entes[ente[atributo]].append(_id)
                else:
                    indexed_entes[ente[atributo]]=[_id]
        if id_conjunto in self.indexes: self.indexes[id_conjunto][atributo]=indexed_entes
        else: self.indexes[id_conjunto]={atributo:indexed_entes}
        self.saveIndexes()
        
    def getHMAC(self, msg):
        hash_mac=hmac.new(self.name.encode('utf-8'))
        return hash_mac.hexdigest()
    def loadMap(self):
        try:
            with open('%s/%s'%(self.path,self.id),'rb') as file:
                mapa=pickle.load(file)
                file.close()
            return mapa
        except Exception as ex:
            return {}
    def saveMap(self, mapa):
        with open('%s/%s'%(self.path,self.id),'wb') as file:
            pickle.dump(mapa, file)
            file.close()
    def insert(self,conjunto, ente, **kargs):
        _id=self.save(ente)
        id_conjunto=self.getHMAC(conjunto)
        
        # Indexes
        for atributo in ente:
            self.addIndex(id_conjunto,atributo,_id)
            
        
        if id_conjunto in self.mapa:
            self.mapa[id_conjunto].append(_id)
        else: 
            self.mapa[id_conjunto]=[_id]
        if kargs.get('commit')==True:
            self.commit()
        
        return len(self.mapa[id_conjunto])
    def find(self, conjunto, criteria, **kargs):
        id_conjunto=self.getHMAC(conjunto)
        
        if not id_conjunto in self.indexes: return []
        
        indexes=self.indexes[id_conjunto]
        
        for atributo in self.indexes[id_conjunto] :
            if atributo in indexes and criteria[atributo] in indexes[atributo] :
                entes_id=indexes[atributo][criteria[atributo]]
                if kargs.get('limit'):
                    entes_id=entes_id[:kargs.get('limit')]
                
                for ente_id in entes_id:
                    yield (ente_id, self.getEnte(ente_id))
        
    def select (self, conjunto,**kargs):
        id_conjunto=self.getHMAC(conjunto)
        
        if not id_conjunto in self.mapa: return []
        
        conjunto=self.mapa[id_conjunto]
        if kargs.get('limit'):
            conjunto=conjunto[:kargs.get('limit')]
        if not kargs.get('query_function'):
            for ente_id in conjunto :
                yield (ente_id, self.getEnte(ente_id))
    def getEnte(self, _id):
        with open('%s/%s'%(self.path, _id),'rb') as file:
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
        self.saveMap(self.mapa)
        
        