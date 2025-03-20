# Desafio Técnico para Desenvolvedor Python - Jota

## Contexto:
O Jota recebe um grande volume de notícias de diversas fontes, incluindo agências internacionais, redes sociais e envios de usuários. Essas notícias precisam ser processadas, classificadas por assunto (poder, saúde, tributos, etc.) e disponibilizadas para a equipe editorial através de uma API REST. Além disso, a Jota deseja integrar o envio de notificações via WhatsApp para notícias urgentes.


## Com base nesse cenário, construa uma solução que:

### Receba Webhooks
* Implemente um endpoint que receba webhooks contendo as notícias em formato JSON.

### Armazene as Notícias em Fila
* Utilize um serviço de fila de mensagens para garantir que todas as notícias sejam processadas, mesmo em caso de picos de recebimento.

### Classifique as Notícias
* Projete e implemente um sistema de classificação de notícias utilizando Python e suas bibliotecas.

### Armazene as Notícias
* Utilize um banco de dados para armazenar as notícias classificadas, incluindo título, conteúdo, fonte, data, categoria e flag de urgência.

### Crie uma API REST
* Utilize o framework Django REST para criar uma API que permita à equipe editorial:
  - Acessar as notícias classificadas, filtrando por categoria, data e outros critérios.
  - Marcar notícias como urgentes.

### Implemente em Lambda
* Utilize funções Lambda para:
  - Processar as notícias da fila de mensagens.
  - Classificar as notícias.
  - Armazená-las no banco de dados.

### Agrupamento de Notícias por Temática
* A API deve categorizar automaticamente as notícias em temáticas como política, economia, saúde, tecnologia, esportes, entre outras.
* A classificação deve ser baseada na análise de palavras-chave contidas no título e no corpo do texto.
* A API deve permitir filtrar e listar notícias por temática, facilitando a navegação e organização do conteúdo.

## Escalabilidade
* A solução deve ser escalável para lidar com o crescente volume de notícias.

##  Segurança
* Implemente as melhores práticas de segurança ou explique o que usaria.

## Observabilidade
* Implemente mecanismos de observabilidade para monitorar o desempenho da solução e identificar gargalos.

## Requisitos:
* Utilizar Python 3.x e o framework Django 3.x ou superior.
* Implementar uma solução escalável, segura e observável.
* Documentar o código e a arquitetura da solução, incluindo diagramas e explicações claras.
* Versionar o código utilizando Git.
* Escrever testes unitários e de integração para garantir a qualidade do código.
* Utilizar Docker para containerizar os microsserviços.

## Entrega:
* O candidato deve entregar o código-fonte da solução em um repositório Git (ex: GitHub, GitLab, Bitbucket).
* O repositório deve incluir a documentação, instruções de deployment e scripts para automatizar o processo.
* O candidato deve apresentar a solução Rodando e responder a perguntas sobre a arquitetura, o código e as decisões tomadas durante o desenvolvimento na próxima fase.

## Observações:
* Este desafio foi projetado para avaliar as habilidades do candidato em Python, Django, Cloud e arquitetura de microsserviços.
* O candidato é livre para utilizar bibliotecas e ferramentas de sua preferência, desde que justifique suas escolhas.
* A criatividade, a capacidade de resolver problemas e a atenção aos detalhes serão altamente valorizadas.
* Qualquer dúvida sobre o requisito pode nos enviar. 



