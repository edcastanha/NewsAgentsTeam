```
@startuml
!theme plain

' System Context Diagram
title System Context Diagram - Jota News Processingactor "Editorial Team" as EditorialTeam
actor "News Sources" as NewsSources
actor "WhatsApp Service" as WhatsApppackage "Jota News Processing System" {
  [Webhooks] as WebhookReceiver
  [Message Queue] as MessageQueue
  [News Processor] as NewsProcessor
  [News Classifier] as NewsClassifier
  [News Database] as NewsDatabase
  [REST API] as RestAPI
  [WhatsApp Notifier] as WhatsAppNotifier
}EditorialTeam -- RestAPI : Accesses classified news
NewsSources -- WebhookReceiver : Sends news via webhook
WebhookReceiver -- MessageQueue : Publishes raw news
MessageQueue -- NewsProcessor : Consumes raw news
NewsProcessor -- NewsClassifier : Invokes for classification
NewsClassifier -- NewsProcessor : Returns classified news
NewsProcessor -- NewsDatabase : Stores classified news
RestAPI -- NewsDatabase : Retrieves classified news
RestAPI -- EditorialTeam : Provides classified news
RestAPI -- WhatsAppNotifier : Triggers urgent news notification
NewsDatabase -- WhatsAppNotifier : Checks for urgent news
WhatsAppNotifier -- WhatsApp : Sends urgent news notifications@enduml
```
