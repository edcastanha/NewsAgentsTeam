import re
import os

def load_stopwords_from_file(filepath="stopwords_pt.txt"):
    """Carrega stopwords de um arquivo de texto, uma palavra por linha."""
    stopwords = set()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                word = line.strip()
                if word:
                    stopwords.add(word)
    except FileNotFoundError:
        print(f"Arquivo de stopwords '{filepath}' não encontrado. Usando lista padrão.")
        stopwords = set([
            'a', 'à', 'ao', 'aos', 'aquela', 'aquelas', 'aquele', 'aqueles', 'aquilo',
            'as', 'assim', 'com', 'como', 'da', 'das', 'de', 'dela', 'delas', 'dele',
            'deles', 'depois', 'do', 'dos', 'e', 'ela', 'elas', 'ele', 'eles', 'em',
            'entre', 'era', 'eram', 'éramos', 'essa', 'essas', 'esse', 'esses', 'esta',
            'estas', 'este', 'estes', 'isto', 'já', 'lhe', 'lhes', 'mais', 'mas', 'me',
            'mesmo', 'meu', 'meus', 'minha', 'minhas', 'muito', 'na', 'nas', 'não',
            'nas', 'nem', 'no', 'nos', 'nossa', 'nossas', 'nosso', 'nossos', 'num',
            'numa', 'o', 'os', 'para', 'pela', 'pelas', 'pelo', 'pelos', 'por',
            'porque', 'qual', 'quais', 'quando', 'que', 'quem', 'são', 'se', 'seja',
            'sejam', 'sem', 'ser', 'será', 'serão', 'seria', 'seriam', 'seu', 'seus',
            'sua', 'suas', 'também', 'te', 'tem', 'tém', 'tinha', 'tinham', 'tínhamos',
            'teu', 'teus', 'tua', 'tuas', 'um', 'uma', 'umas', 'uns', 'você', 'vocês',
            'vos', 'seu', 'sua', 'seus', 'suas', 'nos', 'lhes', 'me', 'mim', 'comigo',
            'ti', 'contigo', 'ele', 'ela', 'nós', 'vós', 'eles', 'elas', 'dele', 'dela',
            'deles', 'delas', 'isto', 'aquilo', 'aquele', 'aquela', 'aqueles', 'aquelas',
            'isso', 'esse', 'essa', 'esses', 'essas', 'o', 'a', 'os', 'as', 'ao', 'aos',
            'do', 'dos', 'da', 'das', 'de', 'em', 'na', 'nas', 'por', 'com', 'para',
            'perante', 'sob', 'sobre', 'trás', 'através', 'durante', 'mediante', 'salvo',
            'segundo', 'senão', 'exceto', 'fora', 'afora', 'logo', 'ora', 'já', 'ainda',
            'sempre', 'nunca', 'jamais', 'apenas', 'só', 'somente', 'também', 'mesmo',
            'aliás', 'outrossim', 'ademais', 'além disso', 'assim', 'dessa forma',
            'desse modo', 'desta maneira', 'feito isso', 'em seguida', 'então', 'logo após',
            'por conseguinte', 'portanto', 'assim sendo', 'dessa sorte', 'destarte',
            'em vista disso', 'de acordo com', 'conforme', 'segundo', 'como', 'tal qual',
            'tanto quanto', 'assim como', 'bem como', 'não só... mas também', 'quer... quer',
            'seja... seja', 'ou... ou', 'nem... nem', 'mas', 'porém', 'contudo',
            'todavia', 'entretanto', 'no entanto', 'apesar disso', 'não obstante',
            'em contrapartida', 'ao contrário', 'pelo contrário', 'ali', 'aqui', 'acolá',
            'lá', 'cá', 'onde', 'aonde', 'donde', 'para onde', 'de onde', 'em que lugar',
            'qual', 'quais', 'quanto', 'quanta', 'quantos', 'quantas', 'que', 'quem',
            'cujo', 'cuja', 'cujos', 'cujas', 'o qual', 'a qual', 'os quais', 'as quais',
            'um', 'uma', 'uns', 'umas', 'algum', 'alguma', 'alguns', 'algumas', 'nenhum',
            'nenhuma', 'nenhuns', 'nenhumas', 'todo', 'toda', 'todos', 'todas', 'muito',
            'muita', 'muitos', 'muitas', 'pouco', 'pouca', 'poucos', 'poucas', 'vários',
            'várias', 'diverso', 'diversa', 'diversos', 'diversas', 'certo', 'certa',
            'certos', 'certas', 'qualquer', 'quaisquer', 'cada', 'ambos', 'ambas',
            'outro', 'outra', 'outros', 'outras', 'próprio', 'própria', 'próprios',
            'próprias', 'mesmo', 'mesma', 'mesmos', 'mesmas', 'grande', 'pequeno',
            'primeiro', 'último', 'melhor', 'pior', 'maior', 'menor', 'bom', 'boa',
            'bons', 'boas', 'mau', 'má', 'maus', 'más'
        ])
    return stopwords

def preprocess_text(text):
    text = text.lower()
    # Remover pontuação
    text = re.sub(r'[^\w\s]', '', text)
    # Remover stopwords
    stopwords_pt = load_stopwords_from_file()
    words = text.split()
    filtered_words = [word for word in words if word not in stopwords_pt]
    return " ".join(filtered_words)