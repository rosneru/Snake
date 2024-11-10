from abc import ABC, abstractmethod


class GameObject(ABC):

    @abstractmethod
    def render(self):
        pass
