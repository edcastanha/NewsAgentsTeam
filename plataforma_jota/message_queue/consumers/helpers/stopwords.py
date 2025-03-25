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
            'bons', 'boas', 'mau', 'má', 'maus', 'más','tivéssemos', 'pelo', 'houverem', 'quando', 'elas', 'teriam', 'para', 'se', 'estivessem', 'teremos', 'forem', 'esta', 'fui', 'terão', 'tivera', 'foi', 'estava', 'minhas', 'ser', 'estávamos', 'fossem', 'tem', 'até', 'seremos', 'essa', 'esteve', 'suas', 'houveríamos', 'seríamos', 'estiveram', 'que', 'teu', 'de', 'seus', 'teria', 'já', 'terá', 'tive', 'terei', 'fosse', 'quem', 'tém', 'sua', 'estiverem', 'lhes', 'com', 'tenhamos', 'eu', 'fôssemos', 'tivesse', 'estivemos', 'entre', 'houve', 'lhe', 'um', 'me', 'nem', 'delas', 'houverá', 'estavam', 'está', 'qual', 'seriam', 'depois', 'pela', 'estivermos', 'estão', 'essas', 'tu', 'e', 'ou', 'às', 'estejamos', 'são', 'tivermos', 'minha', 'sejamos', 'houvéramos', 'era', 'tiverem', 'aquela', 'tínhamos', 'aos', 'meu', 'tenha', 'houver', 'hão', 'houveriam', 'esses', 'isso', 'não', 'eles', 'a', 'houvemos', 'temos', 'havemos', 'fôramos', 'nós', 'estivéssemos', 'estivesse', 'na', 'haja', 'estive', 'houvermos', 'sou', 'nosso', 'serão', 'seria', 'somos', 'será', 'tinha', 'estas', 'tiver', 'à', 'dela', 'tenho', 'teríamos', 'teus', 'tuas', 'do', 'serei', 'estamos', 'aqueles', 'foram', 'esteja', 'num', 'eram', 'hajamos', 'dele', 'haver', 'te', 'pelas', 'estejam', 'fora', 'houverão', 'sejam', 'estes', 'fomos', 'em', 'deles', 'estivéramos', 'houverei', 'meus', 'aquelas', 'tivemos', 'formos', 'dos', 'no', 'há', 'ele', 'houvesse', 'numa', 'tivéramos', 'as', 'nossa', 'vocês', 'por', 'estou', 'mesmo', 'sem', 'hajam', 'teve', 'tinham', 'tua', 'os', 'estivera', 'tiveram', 'você', 'houvera', 'hei', 'uma', 'nas', 'o', 'seu', 'ela', 'ao', 'nos', 'for', 'mas', 'vos', 'esse', 'aquilo', 'éramos', 'da', 'houveram', 'como', 'houvéssemos', 'tenham', 'isto', 'tivessem', 'é', 'este', 'estar', 'estiver', 'muito', 'das', 'houvessem', 'houveremos', 'aquele', 'pelos', 'houveria', 'seja', 'só', 'também', 'nossos', 'nossas', 'mais',
            'pelos', 'esses', 'ela', 'havemos', 'mais', 'para', 'estar', 'temos', 'fossem', 'forem', 'só', 'tem', 'dos', 'houvermos', 'a', 'esteve', 'num', 'seria', 'estávamos', 'na', 'sou', 'tivermos', 'hajamos', 'houverão', 'quando', 'teus', 'tinha', 'houveria', 'meus', 'teríamos', 'dela', 'hão', 'estas', 'da', 'tenham', 'até', 'à', 'seu', 'as', 'há', 'também', 'estavam', 'qual', 'houveremos', 'estava', 'seriam', 'fomos', 'do', 'eram', 'em', 'essa', 'estivesse', 'suas', 'tu', 'esteja', 'minha', 'pelas', 'terei', 'tiver', 'houveríamos', 'os', 'houve', 'houveram', 'teriam', 'isto', 'tinham', 'estes', 'estiverem', 'lhe', 'pela', 'éramos', 'seus', 'numa', 'quem', 'é', 'são', 'delas', 'nossas', 'vos', 'somos', 'hei', 'teu', 'este', 'nosso', 'estivermos', 'às', 'foi', 'tivéssemos', 'houvesse', 'teve', 'seja', 'tiveram', 'nas', 'houvéramos', 'e', 'estejamos', 'muito', 'tive', 'estivessem', 'nós', 'fosse', 'tivessem', 'com', 'seremos', 'tiverem', 'estamos', 'essas', 'estiver', 'formos', 'nos', 'fui', 'tivesse', 'tuas', 'sem', 'houverá', 'o', 'estivemos', 'tenha', 'entre', 'houvessem', 'tivéramos', 'das', 'aquilo', 'teria', 'nossa', 'eles', 'lhes', 'estivera', 'de', 'te', 'um', 'fôssemos', 'ou', 'houverei', 'meu', 'tém', 'terá', 'esse', 'estiveram', 'deles', 'me', 'tínhamos', 'ser', 'minhas', 'dele', 'no', 'houver', 'terão', 'por', 'houvemos', 'ao', 'aquele', 'houverem', 'estão', 'estivéssemos', 'haja', 'que', 'você', 'tivemos', 'sejam', 'era', 'houvera', 'aquelas', 'como', 'ele', 'nossos', 'serei', 'está', 'vocês', 'pelo', 'elas', 'houvéssemos', 'aos', 'aquela', 'isso', 'não', 'fôramos', 'se', 'tenhamos', 'tivera', 'foram', 'estejam', 'estou', 'eu', 'tua', 'teremos', 'esta', 'uma', 'já', 'depois', 'hajam', 'nem', 'for', 'haver', 'mesmo', 'será', 'seríamos', 'aqueles', 'houveriam', 'estive', 'tenho', 'sejamos', 'fora', 'sua', 'estivéramos', 'mas', 'serão',
            'houver', 'tua', 'houvemos', 'são', 'estamos', 'estou', 'num', 'aqueles', 'havemos', 'seja', 'estas', 'sua', 'para', 'teus', 'tiver', 'seríamos', 'estar', 'houveremos', 'estivesse', 'nossa', 'na', 'vocês', 'vos', 'entre', 'essas', 'tenho', 'no', 'por', 'serão', 'ou', 'que', 'pelas', 'o', 'seriam', 'eles', 'terá', 'fui', 'estivermos', 'da', 'fôssemos', 'tiveram', 'tivéssemos', 'dela', 'tu', 'esta', 'estávamos', 'numa', 'elas', 'mas', 'teve', 'teu', 'aquelas', 'aos', 'estiverem', 'os', 'estão', 'pelos', 'sem', 'nossos', 'estejamos', 'tivemos', 'tivera', 'tivéramos', 'ao', 'lhe', 'do', 'quando', 'forem', 'está', 'fossem', 'houveria', 'aquela', 'nosso', 'meu', 'terão', 'houverei', 'suas', 'houveriam', 'eram', 'deles', 'teriam', 'houveram', 'nos', 'se', 'houverem', 'nem', 'seria', 'esses', 'teríamos', 'somos', 'como', 'é', 'pelo', 'houveríamos', 'sejamos', 'será', 'seus', 'temos', 'qual', 'nas', 'hajam', 'um', 'estes', 'haja', 'tém', 'teria', 'também', 'eu', 'houve', 'à', 'aquele', 'estava', 'este', 'estivemos', 'formos', 'houvesse', 'fomos', 'minhas', 'estivéssemos', 'já', 'houverá', 'essa', 'tenha', 'ele', 'hajamos', 'minha', 'seu', 'tem', 'a', 'tenhamos', 'estejam', 'houvera', 'nossas', 'meus', 'das', 'em', 'muito', 'às', 'tinham', 'sejam', 'era', 'éramos', 'mesmo', 'estavam', 'estivéramos', 'houvéssemos', 'isso', 'estivessem', 'estiveram', 'tivermos', 'as', 'houvéramos', 'estive', 'houvermos', 'mais', 'tinha', 'tiverem', 'ela', 'esteja', 'até', 'com', 'delas', 'esse', 'hão', 'sou', 'seremos', 'fora', 'tivesse', 'fôramos', 'foram', 'há', 'terei', 'tive', 'houvessem', 'nós', 'fosse', 'lhes', 'pela', 'me', 'quem', 'dos', 'foi', 'serei', 'houverão', 'teremos', 'for', 'dele', 'tuas', 'haver', 'isto', 'ser', 'e', 'esteve', 'você', 'tínhamos', 'te', 'depois', 'estivera', 'estiver', 'tenham', 'uma', 'aquilo', 'de', 'hei', 'não', 'tivessem', 'só',
            'a', 'meu', 'aquele', 'mas', 'numa', 'tenha', 'fôssemos', 'nossos', 'seríamos', 'estavam', 'estivera', 'hajam', 'fomos', 'estejam', 'pelos', 'houvéramos', 'à', 'é', 'minhas', 'teríamos', 'também', 'sejamos', 'era', 'até', 'se', 'vocês', 'na', 'formos', 'estávamos', 'tenham', 'dos', 'nossa', 'ser', 'são', 'dele', 'quando', 'seu', 'houverá', 'tinham', 'tivermos', 'lhes', 'me', 'teve', 'estivermos', 'nosso', 'seus', 'tínhamos', 'não', 'essa', 'este', 'da', 'hão', 'e', 'hajamos', 'o', 'os', 'estas', 'esteve', 'estivéssemos', 'terão', 'tive', 'houverem', 'sem', 'seja', 'muito', 'eram', 'sejam', 'de', 'será', 'para', 'sua', 'tenhamos', 'aos', 'essas', 'terá', 'tinha', 'isso', 'no', 'tivessem', 'depois', 'houvera', 'éramos', 'estes', 'estive', 'nem', 'seremos', 'eu', 'uma', 'do', 'pelo', 'seria', 'aquelas', 'terei', 'estar', 'meus', 'nossas', 'mais', 'teremos', 'aqueles', 'pelas', 'tiveram', 'você', 'seriam', 'está', 'delas', 'houvemos', 'somos', 'teria', 'tivéssemos', 'nas', 'às', 'temos', 'teus', 'que', 'tu', 'aquilo', 'elas', 'houveríamos', 'tua', 'dela', 'tenho', 'houveram', 'haja', 'teriam', 'lhe', 'serão', 'quem', 'só', 'nos', 'em', 'estivéramos', 'estivesse', 'sou', 'houver', 'tem', 'houvéssemos', 'num', 'suas', 'ele', 'estivemos', 'tivéramos', 'estão', 'minha', 'ao', 'ou', 'houvessem', 'tivemos', 'isto', 'por', 'fui', 'as', 'esse', 'mesmo', 'com', 'houvermos', 'nós', 'houveremos', 'tivesse', 'tuas', 'tiver', 'houverei', 'há', 'estejamos', 'eles', 'esteja', 'fossem', 'teu', 'houvesse', 'haver', 'estiverem', 'tém', 'estou', 'estivessem', 'qual', 'tiverem', 'foi', 'foram', 'como', 'forem', 'houveriam', 'houveria', 'ela', 'um', 'esta', 'fora', 'fosse', 'esses', 'te', 'houverão', 'estava', 'houve', 'vos', 'for', 'hei', 'deles', 'das', 'pela', 'serei', 'já', 'fôramos', 'entre', 'tivera', 'havemos', 'estiveram', 'estamos', 'estiver', 'aquela'
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