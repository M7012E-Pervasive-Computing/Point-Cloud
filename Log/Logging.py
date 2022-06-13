_DEFAULT = '\033[99m'
_GREEN = '\033[92m'
_YELLOW = '\033[93m'
_RED = '\033[91m'
_BLUE = '\033[94m'

class Log():

    @staticmethod
    def info(message: str): 
        print(f"[INFO]  {message}")

    @staticmethod
    def warn(message: str): 
        print(f"[WARN]  {message}")

    @staticmethod
    def error(message: str): 
        print(f"[ERROR] {message}")

    @staticmethod
    def debug(message: str): 
        print(f"[DEBUG] {message}")
    


