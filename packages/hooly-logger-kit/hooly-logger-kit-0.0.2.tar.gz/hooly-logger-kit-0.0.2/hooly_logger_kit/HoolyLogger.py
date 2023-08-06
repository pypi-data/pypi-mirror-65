from datetime import datetime

COLOR = {
    'blue': '\033[94m',
    'default': '\033[99m',
    'grey': '\033[90m',
    'yellow': '\033[93m',
    'black': '\033[90m',
    'cyan': '\033[96m',
    'green': '\033[92m',
    'magenta': '\033[95m',
    'white': '\033[97m',
    'red': '\033[91m',
    'end': '\033[0m'
}


class HoolyLogger:

    @staticmethod
    def get_time_stamp():
        date_time_obj = datetime.now()
        time_stamp_str = date_time_obj.strftime("%d-%m-%Y %H:%M:%S")
        return time_stamp_str

    @classmethod
    def server(cls, message: str):
        # Change color text
        current_time = f"{COLOR['white']}[ {cls.get_time_stamp()} ]{COLOR['end']}"
        type_log = f"{COLOR['black']}[SERVER] {COLOR['end']}"
        message = f"{COLOR['green']}{message}"

        message_formatted = f" {current_time} {type_log} {message}"
        print(message_formatted)

    @classmethod
    def info(cls, message: str):
        # Change color text
        current_time = f"{COLOR['white']}[ {cls.get_time_stamp()} ]{COLOR['end']}"
        type_log = f"{COLOR['black']}[INFO] {COLOR['end']}"
        message = f"{COLOR['green']}{message}"

        message_formatted = f" {current_time} {type_log} {message}"
        print(message_formatted)

    @classmethod
    def debug(cls, message: str):
        # Change color text
        current_time = f"{COLOR['white']}[ {cls.get_time_stamp()} ]{COLOR['end']}"
        type_log = f"{COLOR['black']}[DEBUG] {COLOR['end']}"
        message = f"{COLOR['blue']}{message}"

        message_formatted = f" {current_time} {type_log} {message}"
        print(message_formatted)

    @classmethod
    def warn(cls, message: str):
        # Change color text
        current_time = f"{COLOR['white']}[ {cls.get_time_stamp()} ]{COLOR['end']}"
        type_log = f"{COLOR['black']}[WARN] {COLOR['end']}"
        message = f"{COLOR['yellow']}{message}"

        message_formatted = f" {current_time} {type_log} {message}"
        print(message_formatted)

    @classmethod
    def error(cls, message: str):
        # Change color text
        current_time = f"{COLOR['white']}[ {cls.get_time_stamp()} ]{COLOR['end']}"
        type_log = f"{COLOR['white']}[ERROR] {COLOR['end']}"
        message = f"{COLOR['red']}{message}"

        message_formatted = f" {current_time} {type_log} {message}"
        print(message_formatted)
