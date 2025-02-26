from abc import ABC, abstractmethod

class Visualization(ABC):
    def __init__(self, data):
        self.data = data

    @abstractmethod
    def plot(self):
        pass