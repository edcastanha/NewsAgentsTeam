# Lista de Tarefas

Este documento contém a lista de tarefas a serem executadas neste projeto.

## Tarefas

- [X] Definir o escopo do projeto.
- [X] Identificar os recursos necessários.
- [X] Configurar o ambiente de desenvolvimento.
- [X] Criar o repositório do projeto (Git).
- [-] Desenvolver a funcionalidade principal.
- [ ] Implementar testes unitários.
- [ ] Realizar testes de integração.
- [ ] Escrever a documentação do projeto.
- [ ] Preparar a apresentação do projeto.
- [ ] Revisar o código.



## Notas

* As tarefas serão atualizadas conforme o progresso do projeto.
* Prioridades podem ser adicionadas posteriormente.
* Detalhes adicionais podem ser adicionados a cada tarefa.

---

**Legenda:**

*`[ ]`: Tarefa pendente (não iniciada).
*`[x]`: Tarefa concluída.
*`[-]`: Tarefa em andamento.



jota_news_processor/
├── docker/
│   ├── Dockerfile.api               # Dockerfile para API principal
│   ├── Dockerfile.receiver          # Dockerfile para consumer receiver
│   ├── Dockerfile.classifier        # Dockerfile para consumer classifier
│   └── nginx/                       # Configurações do Nginx para produção
│       └── nginx.conf
├── docker-compose.yml               # Configuração do ambiente de desenvolvimento
├── requirements.txt                 # Dependências do projeto
├── manage.py                        # Script principal do Django
├── core_dj/                         # Módulo principal do Django
│   ├── __init__.py
│   ├── settings.py                  # Configurações do Django
│   ├── urls.py                      # Configuração de URLs
│   ├── asgi.py                      # ASGI config
│   └── wsgi.py                      # WSGI config
├── webhook/                         # App para recebimento de webhooks
│   ├── __init__.py
│   ├── views.py                     # Views para receber webhooks
│   ├── urls.py                      # URLs da webhook
│   └── tests/                       # Testes para webhook
├── news/                            # App principal para gerenciar notícias
│   ├── __init__.py
│   ├── models.py                    # Modelos para notícias, categorias, etc.
│   ├── serializers.py               # Serializadores para API REST
│   ├── views.py                     # ViewSets para API REST
│   ├── admin.py                     # Configuração do admin
│   ├── urls.py                      # URLs da API
│   └── tests/                       # Testes para o app de notícias
├── classifier/                      # Módulo de classificação de notícias
│   ├── __init__.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── category_classifier.py   # Lógica para classificação de categorias
│   │   ├── tag_extractor.py         # Lógica para extração de tags
│   │   └── urgency_detector.py      # Lógica para detecção de urgência
│   └── tests/                       # Testes para classificador
├── queue/                           # Módulo para gerenciamento de filas
│   ├── __init__.py
│   ├── publisher.py                 # Publicador de mensagens
│   ├── consumers/
│   │   ├── __init__.py
│   │   ├── receiver.py              # Consumidor para receber notícias
│   │   └── classifier.py            # Consumidor para classificação
│   └── tests/                       # Testes para o módulo de filas
└── scripts/                         # Scripts utilitários
    ├── consumer_receiver.py         # Script para executar o consumidor receiver
    └── consumer_classifier.py       # Script para executar o consumidor classifier