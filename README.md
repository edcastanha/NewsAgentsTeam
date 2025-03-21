# AgentsTeamNews

Atores, artefatos, internos e externos, que interagem com a plataforma para processamento. Integrada via API para entrega de notícias.

<hr/>

## Documentação Arquitetural - Sistema de Processamento de Notícias

### 1. Diagrama de Contexto do Sistema

Este diagrama representa o nível mais alto do modelo C4, fornecendo uma visão geral do sistema de processamento de notícias do Jota e suas interações com entidades externas.

![C4 - Contexto do Sistema](./documentos/img/C4-Context.png)


**Entidades:**

* **Editorial Team (Equipe Editorial):** Representa os usuários humanos que interagem com o sistema para acessar e gerenciar as notícias classificadas. Eles consomem as informações através da API REST.
* **News Sources (Fontes de Notícias):** Abrange as diversas fontes externas que enviam notícias para o sistema. Isso inclui agências internacionais, redes sociais e envios de usuários. A comunicação ocorre através de webhooks.
* **WhatsApp Service:** Representa o serviço externo do WhatsApp utilizado para o envio de notificações de notícias urgentes.
* **Jota News Processing System (Sistema de Processamento de Notícias do Jota):** O Sistema em si, o qual estamos modelando. Ele é composto por diversos componentes internos.

**Relacionamentos:**

* As **Fontes de Notícias** enviam notícias para o **Webhook Receiver** através de webhooks.
* O **Webhook Receiver** publica as notícias recebidas na  **Message Queue** .
* O **News Processor** consome as notícias da  **Message Queue** .
* O **News Processor** invoca o **News Classifier** para classificar as notícias.
* O **News Classifier** retorna as notícias classificadas para o  **News Processor** .
* O **News Processor** armazena as notícias classificadas no  **News Database** .
* A **Equipe Editorial** acessa as notícias classificadas através da  **API REST** .
* A **API REST** recupera as notícias classificadas do  **News Database**  e atualiza categoria de Urgencia.
* A **API REST** interagir com o **Message Queue** para acionar o envio de notificações de notícias urgentes.
* O **WhatsApp Notifier consome do **Message Queue****  para enviar notificações de notícias urgentes para o  **WhatsApp Service** .

---
