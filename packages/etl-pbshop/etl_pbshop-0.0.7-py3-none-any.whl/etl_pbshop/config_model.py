import os
import logging
from datetime import datetime
import time

logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)


class ConfigModel(object):
    def __init__(self, folder):
        # Private
        self.__start_time = -1
        self.__finish_time = -1
        self.__makespan = 0
        self.__test_mode = os.getenv("TEST_MODE", False)
        self.test = {
            "mode": self.__test_mode,
            "len": int(os.getenv("LEN_TEST_MODE", 10)),
            "insert": not self.__test_mode or 'insert' in str(self.__test_mode),
            "log": os.getenv("ENABLE_LOG", False),
        }

        self.DATE_TIME_FMT = "%Y-%m-%dT%H:%M:%S.%fZ"
        self.TIME_NOW_FMT = self.DATE_TIME_FMT
        self.NOW = str(datetime.now().strftime(self.TIME_NOW_FMT))
        self.WHO = os.getenv("USER")
        self.WHERE = os.getenv("PWD")
        self.RUNNING_ON_AZURE = True if not (self.WHO and self.WHERE) else False
        self.ROOT_FOLDER = folder.rsplit('/', maxsplit=1)[0]
        self.PROJECT_NAME = self.ROOT_FOLDER.rsplit('/', maxsplit=1)[1]

        self.SQLITE_DEBUG_FILE = "test_mode.db"

        # Credentials
        self.CREDENTIALS = os.path.join(self.ROOT_FOLDER, 'credentials')
        self.SECRETS_FILE = f'{self.CREDENTIALS}/credentials.json'
        self.SECRETS_FILE_PYGSHEETS = f'{self.CREDENTIALS}/client_secret.json'
        self.TOKEN_FILE = f'{self.CREDENTIALS}/token.pickle'

        self.CREDENTIALS_PREFIX = 'INTEGRACAO'
        self.environ_keys = [key for key in os.environ.keys() if key.startswith(self.CREDENTIALS_PREFIX)]
        self.ALL_CREDENTIALS = {
            "default": [{
                "id": 0,
                "client_id": "",
                "database_name": "",
                "token_url": "",
                "token_path": "",
                "token_value": "",
                "token_validity": "",
                "user": "",
                "pass": "",
                "method_url": "",
                "environment": "",
                "description": "",
            }],
            "google": [],
            "oracle": [],
            "mssqlapi": [],
            "pyodbc": [],
            "sqlalchemy": [],
            "microvix": [],
            "salesforce": [],
            "azure": []
        }

        self.load_all_credentials_from_environment()

        # Delete token file on change
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets',
                       'https://www.googleapis.com/auth/drive',
                       'https://www.googleapis.com/auth/drive.file',
                       'https://spreadsheets.google.com/feeds']

        # Database
        self.DB_TABLES = dict()

        self.SQL_QUERIES = dict()

        self.HEADER = dict()

        self.MAP_HEADERS = dict()

        self.GET = dict()

        self.STATUS_TO = dict()

        self.PRODUCTS = dict()

        self.SHEET_MODEL = ''

        """
        STRING
        """
        self.INTEGRATION_SPREADSHEET_ID = ''  # Ex: '1CZi1FrT5e5Djle9hQVkNbflkOsC_EV-581mpWUtkv0I'

        self.SHEETS_NAMES = ["", "Produtos", "query", "Product_teste"]

        self.RANGE_NAME = 'query!A:D'

        self.URL_GDOCS = 'https://docs.google.com/spreadsheets/d/'
        self.SPREEDSHEET_TYPE = 'application/vnd.google-apps.spreadsheet'
        self.SHEET_TO_BE_FOUND = ''
        self.QUERY = f"name='{self.SHEET_TO_BE_FOUND}' and trashed=false"
        # Sheet configurations
        self.SHEET_OUTPUT = {
            False: self.INTEGRATION_SPREADSHEET_ID,
            True: self.INTEGRATION_SPREADSHEET_ID  # trocar RANGE_NAME
        }
        # Logs Config
        self.LOGS_PATH = 'logs'
        self.LOGS_FILE = os.path.join(self.ROOT_FOLDER, f'{self.LOGS_PATH}/{self.PROJECT_NAME}_{self.NOW}.log')
        self.LOG_LEVEL = logging.DEBUG
        self.FORMAT = '%(levelname)s %(asctime)-15s %(funcName)-8s %(message)s'

        os.makedirs(self.LOGS_PATH, exist_ok=True)

        # Control
        self.MAX_RETRY = 4
        self.SLEEP_S = 2
        self.SLEEP_MAX = 100
        self.LEN_TEST_MODE = 30
        self.PATTERN = {"SEM_DADOS": "SEM DADOS",
                        "SEM_LOJA": "SEM LOJA"}
        self.EMPTY = ['', ' ', '-']

        self.EXTRA_CONFIG = dict()
        self.log = self.get_log()

    def get_log(self):
        if self.test["log"]:
            logging.basicConfig(filename=self.LOGS_FILE, level=self.LOG_LEVEL, format=self.FORMAT)
            logger = logging.getLogger(__name__)
            if self.test["log"] == 'azure' or self.RUNNING_ON_AZURE:
                from opencensus.ext.azure.log_exporter import AzureLogHandler
                logging.basicConfig(level=logging.INFO)
                logger = logging.getLogger(__name__)
                inst_key = self.get_credentials_value("azure", "token_value", "INSIGHTS")
                handler = AzureLogHandler(
                    connection_string=f'InstrumentationKey={inst_key}')
                logger.addHandler(handler)
            return logger
        return LogFake(logging, self.LOG_LEVEL)

    def start(self):
        self.log.info(f" Started at: {self.NOW} by {self.WHO} on {self.WHERE} or Azure: {self.RUNNING_ON_AZURE}")
        self.__start_time = time.time()

    def finish(self):
        self.__finish_time = time.time()
        self.__makespan = self.__finish_time - self.__start_time
        end_min = self.__makespan/60.0 if self.__makespan > 60 else 0
        self.log.info(f"Demorou {self.__makespan} segundos ({end_min} m)")

    def load_all_credentials_from_environment(self):
        default_keys = list(self.ALL_CREDENTIALS["default"][0].keys())
        default_keys.remove('id')
        connections_list = list(self.ALL_CREDENTIALS.keys())
        connections_list.remove('default')
        for system in connections_list:
            pattern_id = f'{self.CREDENTIALS_PREFIX}_{system}_'.upper()
            ids_list =[{'id': str(key[::-1])[0]} for key in self.environ_keys if key.startswith(pattern_id)]
            ids_list = list({frozenset(item.items()): item for item in ids_list}.values())
            for id in ids_list:
                this_id = [id]
                for item in default_keys:
                    pattern = f'{self.CREDENTIALS_PREFIX}_{system}_{item}_{id.get("id")}'.upper()
                    x = [{item: os.getenv(key)} for key in self.environ_keys if key.startswith(pattern)]
                    this_id += x
                self.ALL_CREDENTIALS[system].append(this_id)

    def get_credentials_value(self, system_name, key_name, env_name=None):
        if isinstance(key_name, list):
            ret = [self.get_credentials_value(system_name, key, env_name=env_name) for key in key_name]
            return ret
        elif isinstance(key_name, tuple):
            ret = {key: self.get_credentials_value(system_name, key, env_name=env_name) for key in key_name}
            return ret
        assert key_name in self.ALL_CREDENTIALS['default'][0], f"Chave {key_name} fora do padrão: {self.ALL_CREDENTIALS['default'][0].keys()}"
        env_name = "DEV" if self.test["mode"] and not env_name else env_name.upper()
        system = self.ALL_CREDENTIALS[system_name]
        for env in system:
            if env_name in set(map(lambda d: d.get('environment'), env)):
                try:
                    found = [x for x in set(map(lambda d: d.get(key_name), env)) if x is not None].pop()
                    return found
                except:
                    pass


class Status(object):
    SUCCESS = 'Sucesso'
    FAIL = 'Falha'
    INCONSISTENT = 'Inconsistencia'


class LogFake(object):
    def __init__(self, logger, level=logging.DEBUG):
        self.logger = logger
        self.level = level

    def debug(self, msg):
        if self.level <= logging.DEBUG:
            print(f"DEBUG: \t{self.timeit()}\t {msg}")
            self.logger.debug(msg)

    def info(self, msg):
        if self.level <= logging.INFO:
            print(f"INFO: \t{self.timeit()}\t {msg}")
            self.logger.info(msg)

    def warning(self, msg):
        if self.level <= logging.WARNING:
            print(f"WARNING: \t{self.timeit()}\t {msg}")
            self.logger.warning(msg)

    def error(self, msg):
        if self.level <= logging.ERROR:
            print(f"ERROR: \t{self.timeit()}\t {msg}")
            self.logger.error(msg)

    def exception(self, msg):
        if self.level <= logging.ERROR:
            print(f"EXCEPTION: \t{self.timeit()}\t {msg}")
            self.logger.exception(msg)

    def critical(self, msg):
        if self.level <= logging.CRITICAL:
            print(f"CRITICAL: \t{self.timeit()}\t {msg}")
            self.logger.critical(msg)

    def fatal(self, msg):
        if self.level <= logging.FATAL:
            print(f"FATAL: \t{self.timeit()}\t {msg}")
            self.logger.fatal(msg)

    @staticmethod
    def timeit():
        return str(datetime.now())
