import abc

class MessagingConnectionManager(abc.ABC):
    """
    Interface abstrata para gerenciadores de conexão de mensageria.
    """
    def __init__(self):
        self._connection = None
        self._channel = None

    @abc.abstractmethod
    def get_connection(self):
        """Retorna a conexão com o serviço de mensageria."""
        pass

    @abc.abstractmethod
    def get_channel(self):
        """Retorna o canal de comunicação com o serviço de mensageria."""
        pass

    @abc.abstractmethod
    def _connect(self):
        """Estabelece a conexão com o serviço de mensageria."""
        pass

    @abc.abstractmethod
    def close_connection(self):
        """Fecha a conexão com o serviço de mensageria."""
        pass
