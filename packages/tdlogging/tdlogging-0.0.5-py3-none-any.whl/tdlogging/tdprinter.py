from operator import itemgetter


class TDPrinter:

    __title_padding = 4
    __side_padding = 1
    __name = "tdlogger"
    __symbols = {
        "top-left": "┎",
        "top-right": "┒",
        "bottom-left": "┖",
        "bottom-right": "┚",
        "left-right": "┃",
        "top-bottom": "─",
        "padding": " ",
    }

    def __init__(self, title=""):
        self.title = title
        self.width = 50
        self.messages = []

    def add_message(self, message: str) -> None:
        """
        Add a message to the TDPrinter
        :param message: the message to add
        :return:
        """
        self.messages.append(message)

    def add_dict_message(self, header: str, message: dict) -> None:
        """
        Add a dict message to the TDPrinter
        :param header: the header of message
        :param message: the message dict
        :return:
        """
        self.messages.append(header + ": {")
        for key in message:
            self.messages.append("    '{}': {}".format(key, message[key]))
        self.messages.append("}")

    def get_message(self) -> str:
        """
        Print the message inside the TDPrinter
        :return:
        """

        return_str = ""

        ### Get Box Width excluding side padding ###
        title_total_length = len(self.title) + self.__title_padding
        message_list_in_length = [len(i) for i in self.messages]

        message_max_width = 0
        if len(message_list_in_length) != 0:
            message_max_width = max(message_list_in_length)

        box_width = max(title_total_length, message_max_width, len(self.__name)) + self.__side_padding * 2

        ## Destructing Symbols ##
        top_left, top_right, \
        bottom_left, bottom_right, \
        left_right, top_bottom, \
        padding = itemgetter('top-left', 'top-right',
                             'bottom-left', 'bottom-right',
                             'left-right', 'top-bottom',
                             'padding')(self.__symbols)

        # Add top of the box
        return_str += top_left + (top_bottom * box_width) + top_right + "\n"

        ### Add Title ###
        title_left_padding = (box_width - title_total_length) / 2
        title_right_padding = int(title_left_padding + 0.5)
        title_left_padding = int(title_left_padding)

        return_str += left_right + (padding * title_left_padding) \
                      + "--" + self.title + "--" \
                      + (padding * title_right_padding) + left_right + "\n"

        ### Add messages ###
        for message in self.messages:
            return_str += left_right + padding \
                          + str(message) \
                          + (padding * (box_width - self.__side_padding - len(message))) \
                          + left_right + "\n"

        ### Add TDLOGGER Name
        return_str += left_right + (padding * (box_width - self.__side_padding - len(self.__name)))\
                      + self.__name \
                      + padding + left_right + "\n"

        ### Add Bottom of box ###
        return_str += bottom_left + (top_bottom * box_width) + bottom_right + "\n"

        return return_str

    @staticmethod
    def boxify(title, messages) -> str:
        """
        ###DEPRECATED###
        Print a pretty box around the title and messages
        :param title: Title of Box
        :param messages: Array of Messages
        :return: Boxified string
        """

        final = ""

        # Get width
        max_length = [len(i) for i in messages]
        max_length.append(len(title) + 4)
        width_without_padding = min(100, max(max(max_length) + 4, 40))

        # Print title
        side_length = (width_without_padding - 10) / 2
        header = "┎"
        if side_length % 2 == 0:
            header += "─" * int(side_length)
        else:
            header += "─" * int(side_length + 0.5)
        header += "TDLogger"
        header += "─" * int(side_length)
        header += "┒"
        final += header + "\n"

        title_length = len(title)
        line = "┃"
        side = ((width_without_padding - 6 - title_length) / 2)

        if side % 2 == 0:
            line += " " * int(side)
        else:
            line += " " * int(side + 0.5)
        line += "--"
        line += title
        line += "--"
        tmp = " " * int(side)
        line += tmp
        line += "┃"

        final += line + "\n"

        for line in messages:
            final += (("┃ " + line).ljust(width_without_padding - 1, " ") + "┃") + "\n"

        # Print bottom
        final += "┖" + "─" * (width_without_padding - 2) + "┚" + "\n"
        return final
