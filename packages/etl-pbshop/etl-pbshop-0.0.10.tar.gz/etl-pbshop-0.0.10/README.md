# ETL Lib

![Upload Python Package](https://github.com/inovacaodigital/etl_pbshop_lib/workflows/Upload%20Python%20Package/badge.svg)
[![PyPI version](https://badge.fury.io/py/etl-pbshop.svg)](https://badge.fury.io/py/etl-pbshop)

This is a simple package built for Portobello Shop integrations, and now is available as ETL lib.
 
 Can be used with several services, like:
 * Oracle
 * Salesforce 
 * MSSQL Server
 * GSuite
 * Microvix
 * ODBC Drivers: PYODBC and SQLALCHEMY
 * And any REST services ...
 
 # Basic Usage 
 
 Use inheritance and rewrite the three main methods:
 
 ```python
from etl_pbshop import ETL, Connectors

class MyETL(ETL):

    def extract(self):
        # extract the needed data using Connectors
        pass

    def transform(self):
        # do some transformations
        pass

    def load(self):
        # upload your transformations
        pass
```

On the main caller, you can simply:

 ```python
if __name__ == '__main__':
    etl = MyETL()
    etl.config.start()
    try:
        etl.run()
        exit(0)
    except Exception as e:
        etl.get_error(f"ERROR on main: {str(e)}")
        raise e
    finally:
        etl.config.finish()
```