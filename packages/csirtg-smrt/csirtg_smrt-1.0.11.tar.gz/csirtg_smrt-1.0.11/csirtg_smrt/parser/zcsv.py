from csirtg_smrt.parser.delim import Delim
import re


class Csv(Delim):

    def __init__(self, *args, **kwargs):
        super(Csv, self).__init__(*args, **kwargs)

        self.pattern = re.compile(",")
        self.add_orig= True

Plugin = Csv
