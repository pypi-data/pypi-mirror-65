from abc import ABC, abstractmethod
from .config_model import ConfigModel
from .query_model import QueryFactory


class ETL(ABC):
    """
     Example:
     Create your ETL and replace the 3 methods:
     >>> extract(), transform() and load()
     
     Then, call the method:
     >>> run()

    class MyETL(ETL):
        def __init__(self, a):
            super().__init__(a)
            self.a = a

        def extract(self):
            self.log("New extract")

        def transform(self):
            self.log("New transform")

        def load(self):
            self.log("New load")
    """

    def __init__(self, data='test_', test_mode=False, conector=None):
        self.data = data
        self.log = None
        self.error_list = []
        self.data_extracted = None
        self.data_transformed = None
        self.data_loaded = None
        self.test_mode = test_mode
        self.data_reference_dict = dict()
        self.data_raw = None
        self.df = dict()
        self.data_frame = None
        self.data_frame_global = None
        self.header = None
        self.status = []
        self.conector = conector  # Conectors(self.log)
        self.creds = self.conector.creds if conector else None
        self.service_sheets = self.conector.service_sheets if conector else None
        self.sql_conn = self.conector.conn if conector else None
        self.query = QueryFactory()
        self.config = ConfigModel(__file__)

    @abstractmethod
    def extract(self):
        self.data_extracted = self.data
        return self.data_extracted

    @abstractmethod
    def transform(self):
        self.data_transformed = self.data_extracted * 2

    @abstractmethod
    def load(self):
        self.data_loaded = self.data_transformed * 2

    def run(self):
        self.extract()
        self.transform()
        self.load()

    def start(self):
        if self.config:
            self.config.start()

    def get_error(self, error_msg):
        if self.log:
            self.log.exception(error_msg)
        self.error_list.append(error_msg)
