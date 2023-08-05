from abc import ABC, abstractmethod

class CommonInterfaceAuth(ABC):
    """ Authorization API
    """
    
     
    def auth(self):
        """ Authorization API

        POST method which returns an 
        authorization token to be used by other calls. 
        """
        pass
