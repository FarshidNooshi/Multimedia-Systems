from .utils.log_business import MyLogger


class Function:
    def __init__(self, name, log_path):
        self.logger = MyLogger(name, log_path)

    def function(self, param, param1):
        pass
