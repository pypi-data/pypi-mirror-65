from tdlogging.tdprinter import TDPrinter


class TDReader:
    @staticmethod
    def read_from_file(file_path: str) -> str:
        """
        Read the contents from a file
        :param file_path: the file path
        :return:
        """
        text = ""
        try:
            with open(file_path, 'r') as file:
                text = file.read()
        except:
            printer = TDPrinter("tdlogger.txt not specified")
            printer.add_message("Continuing with default configuration")
            print(printer.get_message())
        return text

