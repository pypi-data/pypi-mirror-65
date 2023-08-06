from abc import ABCMeta, abstractmethod


class Strategy(metaclass=ABCMeta):
    def start(self):
        # Data Collection
        collected_data = self.collect()
        
        # Data Analysis
        analysed_data = self.analyse(collected_data)
        
        # Behave
        return self.behave(analysed_data)
    
    @abstractmethod
    def collect(self):
        pass
    
    @abstractmethod
    def analyse(self, collected_data):
        pass
    
    @abstractmethod
    def behave(self, analysed_data):
        pass

