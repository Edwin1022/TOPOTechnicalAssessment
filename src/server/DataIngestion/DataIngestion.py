from abc import ABC, abstractmethod

class DataIngestion(ABC):
    def __init__(self):
        self.data = None

    @abstractmethod
    def load_data(self, file_path):
        pass

    @abstractmethod
    def create_processor(self):
        pass