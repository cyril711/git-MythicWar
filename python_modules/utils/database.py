from PyQt5 import QtSql, QtCore




class DatabaseManager (QtCore.QObject):
    def __init__(self,database_name,in_place=False):
        super(DatabaseManager).__init__()
        self.database_name = database_name
        self.database = None
        self.verbose = False
        self.in_place = in_place
        
    def createConnection (self):
        self.database = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        if self.in_place :
            self.database.setDatabaseName(self.database_name)
        else:
            temp_filename = "totor.txt"
            try : 
                
                if not QtCore.QFile.remove(temp_filename):
                    QtCore.qDebug("not able to remove file")
            except OSError:
                pass
            try:

                if not QtCore.QFile.copy(self.database_name,temp_filename):
                    QtCore.qDebug("copy impossible")    
                else:
                    print ('copy reussit de ',self.database_name,temp_filename)
            except IOError :
                QtCore.qDebug("not able to copy file")
                pass
            self.database.setDatabaseName(temp_filename)
        if not self.database.open():
            QtCore.qDebug("Database not OPen")
    
    def __del__(self):
        self.database.close()
        
    def _delete (self,from_, condition):
        query = QtSql.QSqlQuery(self.database)
        query_str = "DELETE FROM "+ str(from_)
        if condition != None: 
            query_str+=" WHERE "+ str(condition)

        query_str+=";"                
        if self.verbose == True :
            QtCore.qDebug(query_str)    
        query.exec_(query_str)
        return query
                    
    def insert (self,table_name,record):
        query = QtSql.QSqlQuery(self.database)
        query_str = "INSERT INTO "+str(table_name)+" ( "
        value = ""
        attrib = ""
        first = True
        for key in record.keys() : 
            if not first : 
                attrib += ", "
                value += ", "
            attrib+=str(key)
            value+="?"
            first = False
        query_str+= str(attrib)+" ) VALUES ( "
        query_str+= str (value)+ " );"
        query.prepare(query_str)
        for value in record.values():
            query.addBindValue(value)

        if self.verbose == True :
            QtCore.qDebug(query_str)
        if not query.exec_():
            QtCore.qDebug("Sqlite request failure")
            
    def select (self,fields,from_,unique=False,condition=None, sort=None):
        query = QtSql.QSqlQuery(self.database)
        query_str = "SELECT "+str(fields)+" FROM "+ str(from_)
        if condition != None: 
            query_str+=" WHERE "+ str(condition)

        if sort != None :
            query_str+=" ORDER BY "+ str(sort)
        if unique == False :
            query_str+=" ;"
        else : 
            query_str+=" LIMIT 1 ;"                
        if self.verbose == True :
            QtCore.qDebug(query_str)    
        query.exec_(query_str)
        return query
        

    def update (self,table_name,attributes,condition= None):
        if len(attributes)!= 0:
            query = QtSql.QSqlQuery(self.database)
            query_str = "UPDATE "+str(table_name)+" SET "
            attrib = ""
            first = True
            for key in attributes.keys():
                if not first :
                    attrib+= ", "
                attrib+=str(key)+"=?"
                first = False
            query_str+=attrib
            if condition != None : 
                query_str+=" WHERE "+str(condition)
            query_str+=" ;"       
            query.prepare(query_str)
            for value in attributes.values():
                query.addBindValue(value)
    
            if self.verbose == True :
                QtCore.qDebug(query_str)
    #             for value in attributes.values():
    #                 value = '"'+str(value)+'"'                
    #                 print (value)
           # q_str = 'UPDATE gm_perso SET RepresentativPic= "images/La_Guerre_Mythique/Grec/Hephaistos/Picture/Cyclopes_Forgerons/Zuali/Zuali.jpg", Leader= "False", Latitude= "48.858093", Longitude= "2.294694", Level="0", Place="0" WHERE IDPerso=1114 ;'
            if not query.exec_():
                QtCore.qDebug(query.lastError().text())


    def createTable (self,table_name,attribs):
        query = QtSql.QSqlQuery(self.database)
        query_str = "CREATE TABLE "+ str(table_name)+ " ( "+ str(attribs)+ " ) ;"        
        if self.verbose == True :
            QtCore.qDebug(query_str)
        if not query.exec_():
            QtCore.qDebug("Sqlite request failure")

    def execute (self,requete):    
        query = QtSql.QSqlQuery(self.database)
        if self.verbose == True :
            QtCore.qDebug(requete)
        if not query.exec_(requete):
            QtCore.qDebug("Sqlite request failure")
            
    def databaseName (self):
        return self.database_name
    
    def setVerbose (self, value):
        self.verbose = value
        