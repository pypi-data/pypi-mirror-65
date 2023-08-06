import pandas as pd

class Simulator():

    def __init__(self, df,*args, **kwargs):

        self.indicators = []
        self.data_history = {}
        self.df = pd.read_csv(df)
        self.actual_bar = 0
        self.compiled = False

    def step(self, hist=None):

        if not hist:
            hist = self.data_history

        self.actual_data = self.df.iloc[self.actual_bar,:] #Read actualbar data
        self.compiled_data = {}

        for col in self.df.columns:
            self.data_history[col].append(self.actual_data[col]) #Append actualbar data to history
            self.compiled_data[col] = self.actual_data[col] #Append actualdata to step return

        for indicator in self.indicators:
            res = indicator.compute(hist)

            self.data_history[indicator.name].append(res) #Append actual indicator values to history
            self.compiled_data[indicator.name] = res  #Append actual indicators return to step return

        self.actual_bar+=1
        return self.compiled_data

    def add(self, indicator):
        self.indicators.append(indicator)

    def compile(self, buffersize):
        #Get the init point to start by getting the max number of prev bars from the indicators
        if len(self.indicators)>0:
            maxes = max([ind.use_n_bars for ind in self.indicators])
            self.max_prev = maxes
        else:
            self.max_prev = 0

        self.actual_bar = self.max_prev

        #Create init data
        ini_data = self.df.iloc[:self.max_prev,:].to_dict(orient="list")
        #Initilize data history
        for indicator in self.indicators:
            ini_data[indicator.name] = []
            self.data_history[indicator.name] = []
        for dat in ini_data:
            self.data_history[dat] = []

        for n in range(buffersize):
            self.step(ini_data)



