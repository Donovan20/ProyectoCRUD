import pymysql
from pymysql import cursors

class Conexion:
    __instance = None
    __conexion = None
    def __new__(cls):
        if Conexion.__instance == None and Conexion.__conexion == None:
            Conexion.__instance = super(Conexion,cls).__new__(cls)
        return Conexion.__instance

    def __init__(self):
        self.bd = 'crud'
        self.user = 'root'
        self.ps = ''
        self.address = 'localhost'
        self.conectar()
    
    def conectar(self):
        if Conexion.__conexion == None:
            Conexion.__conexion = pymysql.connect(self.address,self.user,self.ps,self.bd)

    def getCon(self):
        return Conexion.__conexion

    def select(self, query):
        cur = Conexion.__conexion.cursor()
        cur.execute(query)
        resultado = cur.fetchall()
        return resultado

    def insert(self,query):
        cur = Conexion.__conexion.cursor()
        resultado = cur.execute(query)
        if resultado:
            Conexion.__conexion.commit()
            return True
        else:
            return False
            
    def update(self,query):
        cur = Conexion.__conexion.cursor()
        resultado = cur.execute(query)
        if resultado:
            Conexion.__conexion.commit()
            return True
        else:
            return False

    def delete(self,query):
        cur = Conexion.__conexion.cursor()
        resultado = cur.execute(query)
        if resultado:
            Conexion.__conexion.commit()
            return True
        else:
            return False
    
    def desconectar(self):
        Conexion.__conexion.close()
        Conexion.__instance = None
        Conexion.__conexion = None