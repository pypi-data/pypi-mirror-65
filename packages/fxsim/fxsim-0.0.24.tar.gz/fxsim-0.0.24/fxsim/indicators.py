class Indicator():

    def __init__(self, name, use_n_bars):
        self.use_n_bars = use_n_bars
        self.name = name
        self.data = []

    def compute(self, history):

        return (history.High)