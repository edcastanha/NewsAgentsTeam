import re
import logging

logger = logging.getLogger(__name__)

class UrgencyDetector:
    """
    Classe responsável por detectar se uma notícia é urgente com base
    em seu conteúdo e título.
    """
    
    # Palavras-chave que indicam urgência
    URGENCY_KEYWORDS = [
        'urgente', 'breaking', 'última hora', 'alerta', 'emergência',
        'imediato', 'agora', 'acaba', 'acontecendo', 'decisão',
        'aprovado', 'rejeitado', 'votação', 'rompimento', 'crise'
    ]
    
    # Expressões regulares para identificar indicadores de urgência
    URGENCY_PATTERNS = [
        r'(?i)^urgent[e]?:', 
        r'(?i)^breaking:',
        r'(?i)^última hora:',
        r'(?i)^alerta:',
        r'(?i)\bacaba de\b',
        r'(?i)\bneste momento\b',
        r'(?i)\bagora\b'
    ]
    
    def detect_urgency(self, title, content):
        """
        Detecta se uma notícia é urgente
        
        Args:
            title (str): Título da notícia
            content (str): Conteúdo da notícia
            
        Returns:
            bool: True se a notícia for urgente, False caso contrário
        """
        if not title and not content:
            return False
            
        # Verificar padrões no título
        if title:
            # Verificar padrões através de regex
            for pattern in self.URGENCY_PATTERNS:
                if re.search(pattern, title):
                    logger.info(f"Notícia marcada como urgente pelo padrão: {pattern}")
                    return True
            
            # Verificar palavras-chave no título (tem maior peso)
            title_lower = title.lower()
            for keyword in self.URGENCY_KEYWORDS:
                if keyword in title_lower:
                    logger.info(f"Notícia marcada como urgente pela palavra-chave no título: {keyword}")
                    return True
        
        # Verificar no conteúdo
        if content:
            # Verificar apenas no primeiro parágrafo do conteúdo
            first_paragraph = content.split('\n')[0] if '\n' in content else content
            first_paragraph = first_paragraph.lower()
            
            # Verificar padrões
            for pattern in self.URGENCY_PATTERNS:
                if re.search(pattern, first_paragraph):
                    logger.info(f"Notícia marcada como urgente pelo padrão no conteúdo: {pattern}")
                    return True
            
            # Verificar palavras-chave
            for keyword in self.URGENCY_KEYWORDS:
                if keyword in first_paragraph:
                    logger.info(f"Notícia marcada como urgente pela palavra-chave no conteúdo: {keyword}")
                    return True
        
        return False