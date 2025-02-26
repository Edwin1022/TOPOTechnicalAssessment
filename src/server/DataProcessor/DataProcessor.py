from abc import ABC, abstractmethod

class DataProcessor(ABC):
    def __init__(self, data):
        self.data = data

    @abstractmethod
    def process_data(self):
        pass

    @abstractmethod
    def get_data_type(self):
        pass