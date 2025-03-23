import re
import logging
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from django.utils.text import slugify
from news_app.models import Tag
from collections import Counter

logger = logging.getLogger(__name__)

class TagExtractor:
    """
    Classe responsável por extrair tags/palavras-chave de notícias
    """
    
    def __init__(self):
        # Garantir que os recursos do NLTK estão disponíveis
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('punkt')
            nltk.download('stopwords')
        
        # Lista de stopwords em português
        self.stopwords = set(stopwords.words('portuguese'))
        # Adicionar mais stopwords específicas para o domínio
        self.stopwords.update(['é', 'ser', 'estar', 'ter', 'haver', 'fazer'])
        
    def preprocess_text(self, text):
        """
        Pré-processa o texto para extração de tags
        
        Args:
            text (str): Texto a ser processado
            
        Returns:
            str: Texto processado
        """
        if not text:
            return ""
            
        # Converter para minúsculas
        text = text.lower()
        
        # Remover caracteres especiais
        text = re.sub(r'[^\w\s]', ' ', text)
        
        # Remover espaços extras
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
        
    def extract_tags(self, title, content, max_tags=5):
        """
        Extrai tags de uma notícia com base no título e conteúdo
        
        Args:
            title (str): Título da notícia
            content (str): Conteúdo da notícia
            max_tags (int): Número máximo de tags a retornar
            
        Returns:
            list: Lista de objetos Tag
        """
        # Pré-processar texto
        processed_title = self.preprocess_text(title)
        processed_content = self.preprocess_text(content)
        
        # Dar peso maior ao título
        combined_text = f"{processed_title} {processed_title} {processed_content}"
        
        # Tokenizar
        tokens = word_tokenize(combined_text, language='portuguese')
        
        # Remover stopwords e palavras muito curtas
        filtered_tokens = [token for token in tokens if token not in self.stopwords and len(token) > 3]
        
        # Encontrar as palavras mais frequentes
        word_counter = Counter(filtered_tokens)
        most_common = word_counter.most_common(max_tags)
        
        # Se não houver palavras suficientes, retornar lista vazia
        if not most_common:
            return []
            
        # Extrair frases-chave (n-gramas)
        bigrams = self._extract_ngrams(combined_text, 2, max_tags)
        trigrams = self._extract_ngrams(combined_text, 3, max_tags)
        
        # Combinar palavras e frases
        tags_combined = []
        
        # Adicionar palavras individuais mais comuns
        for word, _ in most_common:
            if len(tags_combined) < max_tags:
                tags_combined.append(word)
        
        # Adicionar bigramas mais relevantes
        for bigram, _ in bigrams:
            if len(tags_combined) < max_tags and bigram not in tags_combined:
                tags_combined.append(bigram)
                
        # Adicionar trigramas mais relevantes
        for trigram, _ in trigrams:
            if len(tags_combined) < max_tags and trigram not in tags_combined:
                tags_combined.append(trigram)
        
        # Criar ou obter objetos Tag do banco de dados
        tag_objects = []
        for tag_text in tags_combined[:max_tags]:
            tag, created = Tag.objects.get_or_create(
                name=tag_text.capitalize(),
                slug=slugify(tag_text)
            )
            tag_objects.append(tag)
            
        return tag_objects
        
    def _extract_ngrams(self, text, n, max_ngrams=3):
        """
        Extrai n-gramas do texto
        
        Args:
            text (str): Texto a ser processado
            n (int): Tamanho do n-grama (2 para bigramas, 3 para trigramas)
            max_ngrams (int): Número máximo de n-gramas a retornar
            
        Returns:
            list: Lista de tuplas (n-grama, frequência)
        """
        tokens = word_tokenize(text, language='portuguese')
        
        # Filtrar tokens
        filtered_tokens = [token for token in tokens if token not in self.stopwords and len(token) > 3]
        
        # Gerar n-gramas
        ngrams = []
        for i in range(len(filtered_tokens) - n + 1):
            ngram = ' '.join(filtered_tokens[i:i+n])
            ngrams.append(ngram)
            
        # Contar frequências
        ngram_counter = Counter(ngrams)
        
        # Retornar os mais comuns
        return ngram_counter.most_common(max_ngrams)