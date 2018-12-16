from os import environ

class DatabaseConnection:
    tables = ('users',)
    
    @classmethod
    def connect(table: str):
        if table not in DatabaseConnection.tables:
            return
        
        credentials = {'users': 'root', 'password': environ['dbpasswd'], 'database': 'noheaven', 'host': '127.0.0.1'}
    
                                          



