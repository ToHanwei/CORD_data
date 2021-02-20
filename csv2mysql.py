import sys
import pymysql
import pandas as pd
from sqlalchemy import create_engine
  


class Connecter():
    """
    Convert DataFrame object to MySQL
    """
    def __init__(self, host, db, user, password):
        self.host = str(host)
        self.db = str(db)
        self.user = str(user)
        self.password = str(password)
        self.engine = ''

    def build_engin(self):
        """
        build engin
        """
        engstr = ("mysql+pymysql://"
                  +self.user+":"
                  +self.password+"@"
                  +self.host+"/"
                  +self.db+"?charset=utf8"
                 )
        self.engine = create_engine(engstr)
  

def main():
    csvFilePath = sys.argv[1]
    tableName = sys.argv[2]
    
    connecter = Connecter("10.15.50.100", "Alignment", "root", "Zhaolab@C809!!")
    connecter.build_engin()
    engine = connecter.engine
    
    data = pd.read_csv(csvFilePath)
    data.to_sql(tableName, con=engine,if_exists='replace',index=False)

if __name__ == "__main__":
    main()

