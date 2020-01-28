class ResultGenerator:

    @classmethod
    def boost_result(cls, value):
        if value <= 0:
            return 0
        elif value <= 3:
            return 1
        elif value <= 7:
            return 2
        elif value <= 11:
            return 3
        else:
            return 4

    @classmethod
    def overcome_result(cls, value):
        if value <= 0:
            return 0
        elif value <= 3:
            return 1
        elif value <= 7:
            return 2
        elif value <= 11:
            return 3
        else:
            return 4

    @classmethod
    def get_result_text_from_value(cls, value):
        if value == 0:
            return "Action utterly, spectacularly fails."
        elif value == 1:
            return "Action fails, or succeeds with a major twist."
        elif value == 2:
            return "Action succeeds with a minor twist, or fails."
        elif value == 3:
            return "Action completely succeeds."
        elif value == 4:
            return "Action succeeds overwhelmingly."

