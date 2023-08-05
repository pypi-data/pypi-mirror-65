import datetime
from .print_manager import *

class Log_Settings:
    display_logs = False

class Log_Manager:
    class Log:
        def __init__(self, text, is_error=False, code=""):
            self.time_stamp = datetime.datetime.now()
            self.text = text
            self.is_error = is_error
            self.code = code

        def out_format (self):
            code = ""
            if self.code != "": code = "({})".format(self.code)
            text = ("{} {} => <{}>".format(datetime.datetime.strftime(self.time_stamp, "%Y-%m-%d %H:%M:%S"), code,
                                           self.text))
            return text

        def print_log(self):
            if Log_Settings.display_logs:
                text = self.out_format()
                if self.is_error:
                    mcprint(text=text, color=Color.RED)
                else:
                    mcprint(text=text, color=Color.YELLOW)

    def __init__(self, developer_mode=False, logger_name = "Log"):
        self.logs = []
        self.developer_mode = developer_mode
        self.logger_name = logger_name

    def log(self, text, is_error=False, code=""):
        log = self.Log(text=text, is_error=is_error, code=code)
        self.logs.append(log)
        if(self.developer_mode):
            log.print_log()

    def print_logs(self):
        for log in self.logs:
            log.print_log()

    def clear_logs(self):
        self.logs.clear()

    def save_logs(self, path=None, mode="a"):
        if not path: path = "{}.log".format(self.logger_name)
        with open(path, mode) as output_file:
            for log in self.logs:
                output_file.write(log.out_format()+"\n")

class Main_Logger:
    log_manager = Log_Manager(logger_name="Log")

    def save_logs(path=None, mode="a"):
        Main_Logger.log_manager.save_logs(path=path, mode=mode)
