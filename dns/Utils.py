from dnslib import DNSLabel


class Utils:
    @staticmethod
    def label(label: str) -> DNSLabel:
        return DNSLabel(label)

    @staticmethod
    def label_to_str(label):
        if type(label) is DNSLabel:
            return Utils.label_to_str(str(label))
        elif type(label) is str:
            if len(label) > 0 and label.endswith("."):
                return label[:-1]

    @staticmethod
    def mail_to_label(label : str):
        label = label.lower().replace("@",".")
        return DNSLabel(label)

    @staticmethod
    def list_to_label(*args):
        label = ""
        for arg in args:
            label = label + arg + "."
        return label
