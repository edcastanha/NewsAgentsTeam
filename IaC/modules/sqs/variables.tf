variable "sqs_queue_name" {
  description = "O nome da fila SQS"
  type        = string
  default     = "minha-fila-sqs"
}

variable "delay_seconds" {
  description = "O tempo de atraso para mensagens na fila SQS"
  type        = number
  default     = 0
}

variable "max_message_size" {
  description = "O tamanho máximo da mensagem na fila SQS"
  type        = number
  default     = 262144
}

variable "message_retention_seconds" {
  description = "O tempo de retenção da mensagem na fila SQS"
  type        = number
  default     = 345600
}

variable "receive_wait_time_seconds" {
  description = "O tempo de espera para receber mensagens na fila SQS"
  type        = number
  default     = 0
}

variable "visibility_timeout_seconds" {
  description = "O tempo de visibilidade da mensagem na fila SQS"
  type        = number
  default     = 30
}
