import re
import logging
from collections import Counter
from django.utils.text import slugify
from news_app.models import Category, Subcategory

logger = logging.getLogger(__name__)

class CategoryClassifier:
    """
    Classe responsável por classificar notícias em categorias e subcategorias
    com base no conteúdo e título.
    
    Esta implementação usa uma abordagem baseada em palavras-chave e frequência
    para determinar a categoria mais provável para uma notícia.
    """
    
    # TODO - Dicionário de palavras-chave para cada categoria
    CATEGORY_KEYWORDS = {
        'poder': [
            'congresso', 'senado', 'câmara', 'deputados', 'stf', 'supremo', 
            'presidente', 'lula', 'bolsonaro', 'ministro', 'governo', 'planalto',
            'executivo', 'judiciário', 'legislativo', 'eleição', 'eleições',
            'político', 'políticos', 'política', 'governador', 'prefeito'
        ],
        'tributos': [
            'imposto', 'tributo', 'tributário', 'fiscal', 'receita federal',
            'IR', 'imposto de renda', 'IRPF', 'IRPJ', 'PIS', 'COFINS', 'ICMS',
            'ISS', 'IPI', 'reforma tributária', 'contribuinte', 'sonegação',
            'fiscal', 'arrecadação', 'tributo', 'tributação', 'carga tributária'
        ],
        'saúde': [
            'saúde', 'médico', 'hospital', 'enfermeiro', 'SUS', 'plano de saúde',
            'doença', 'pandemia', 'covid', 'vacina', 'tratamento', 'paciente',
            'ministério da saúde', 'medicamento', 'remédio', 'cirurgia', 'diagnóstico'
        ],
        'trabalhista': [
            'trabalho', 'emprego', 'desemprego', 'CLT', 'trabalhador', 'sindicato',
            'greve', 'férias', 'décimo terceiro', 'FGTS', 'aposentadoria', 'INSS',
            'previdência', 'salário', 'demissão', 'contratação', 'terceirização',
            'trabalhista', 'carteira assinada'
        ]
    }
    
    # Dicionário de subcategorias e suas palavras-chave
    SUBCATEGORY_KEYWORDS = {
        'aposta da semana': [
            'aposta', 'semana', 'previsão', 'análise', 'expectativa'
        ],
        'matinal': [
            'matinal', 'manhã', 'hoje', 'diário', 'resumo'
        ]
    }
    
    def __init__(self):
        # Garantir que as categorias existem no banco de dados
        self._ensure_categories_exist()
        
    def _ensure_categories_exist(self):
        """
        Garante que as categorias básicas existem no banco de dados
        """
        for category_name in self.CATEGORY_KEYWORDS.keys():
            Category.objects.get_or_create(
                name=category_name.capitalize(),
                slug=slugify(category_name)
            )
            
        # Garantir que subcategorias existem
        tributos = Category.objects.get(slug='tributos')
        Subcategory.objects.get_or_create(
            name='Aposta da Semana',
            slug='aposta-da-semana',
            category=tributos
        )
        
        # Subcategoria matinal pode pertencer a qualquer categoria
        for category in Category.objects.all():
            Subcategory.objects.get_or_create(
                name='Matinal',
                slug='matinal',
                category=category
            )
    
    def preprocess_text(self, text):
        """
        Pré-processa o texto para classificação
        
        Args:
            text (str): Texto a ser processado
            
        Returns:
            str: Texto processado em minúsculas e sem caracteres especiais
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
        
    def classify_category(self, title, content):
        """
        Classifica uma notícia em uma categoria com base no título e conteúdo
        
        Args:
            title (str): Título da notícia
            content (str): Conteúdo da notícia
            
        Returns:
            tuple: (category, subcategory, confidence) onde categoria e subcategoria
                   são objetos do modelo e confidence é um valor entre 0 e 1
        """
        # Pré-processar texto
        processed_title = self.preprocess_text(title)
        processed_content = self.preprocess_text(content)
        
        # Combinar título e conteúdo, dando mais peso ao título
        combined_text = f"{processed_title} {processed_title} {processed_content}"
        
        # Contagem de palavras-chave para cada categoria
        category_scores = {}
        for category_name, keywords in self.CATEGORY_KEYWORDS.items():
            score = 0
            for keyword in keywords:
                count = combined_text.count(keyword)
                score += count
            category_scores[category_name] = score
        
        # Encontrar categoria com maior pontuação
        if not category_scores or max(category_scores.values()) == 0:
            return None, None, 0.0
            
        best_category_name = max(category_scores.items(), key=lambda x: x[1])[0]
        
        # Calcular confiança da classificação (normalizado entre 0 e 1)
        total_score = sum(category_scores.values())
        best_score = category_scores[best_category_name]
        confidence = best_score / total_score if total_score > 0 else 0.0
        
        # Buscar objeto da categoria
        try:
            category = Category.objects.get(slug=slugify(best_category_name))
        except Category.DoesNotExist:
            logger.error(f"Categoria {best_category_name} não encontrada no banco de dados")
            return None, None, 0.0
            
        # Verificar subcategorias
        subcategory = self.classify_subcategory(processed_title, processed_content, category)
        
        return category, subcategory, confidence
        
    def classify_subcategory(self, processed_title, processed_content, category):
        """
        Classifica uma notícia em uma subcategoria
        
        Args:
            processed_title (str): Título pré-processado
            processed_content (str): Conteúdo pré-processado
            category (Category): Objeto da categoria
            
        Returns:
            Subcategory: Objeto da subcategoria ou None se não classificado
        """
        # Combinar título e conteúdo
        combined_text = f"{processed_title} {processed_content}"
        
        # Contagem de palavras-chave para subcategorias
        subcategory_scores = {}
        for subcategory_name, keywords in self.SUBCATEGORY_KEYWORDS.items():
            score = 0
            for keyword in keywords:
                count = combined_text.count(keyword)
                score += count
            subcategory_scores[subcategory_name] = score
        
        # Encontrar subcategoria com maior pontuação
        if not subcategory_scores or max(subcategory_scores.values()) == 0:
            return None
            
        best_subcategory_name = max(subcategory_scores.items(), key=lambda x: x[1])[0]
        
        # Se a pontuação for baixa, considerar que não tem subcategoria
        if subcategory_scores[best_subcategory_name] < 2:
            return None
            
        # Buscar objeto da subcategoria
        try:
            return Subcategory.objects.get(
                slug=slugify(best_subcategory_name),
                category=category
                )
        except Subcategory.DoesNotExist:
            # Se não existir esta subcategoria para esta categoria, retornar None
            return None
        
