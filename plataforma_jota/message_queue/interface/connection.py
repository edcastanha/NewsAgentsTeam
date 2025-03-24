import logging

logger = logging.getLogger(__name__)

class MessagingConnectionManager:
    """
    Classe base para gerenciar a conexão com sistemas de mensageria.
    """
    def __init__(self):
        self._connection = None
        self._channel = None

    def get_connection(self):
        """Retorna a conexão com o sistema de mensageria."""
        raise NotImplementedError("Este método deve ser implementado nas subclasses.")

    def get_channel(self):
        """Retorna o canal de comunicação do sistema de mensageria."""
        raise NotImplementedError("Este método deve ser implementado nas subclasses.")

    def close_connection(self):
        """Fecha a conexão com o sistema de mensageria, se necessário."""
        raise NotImplementedError("Este método deve ser implementado nas subclasses.")
