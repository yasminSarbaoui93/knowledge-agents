variable "subscription_id" {
  description = "Azure Subscription ID."
  type        = string
}
variable "resource_group_name" {
  description = "Name of the resource group."
  type        = string
}

variable "location" {
  description = "Azure region for all resources."
  type        = string
}

variable "tags" {
  description = "Tags to apply to all resources."
  type        = map(string)
  default     = {}
}

variable "storage_account_name" {
  description = "Name of the storage account."
  type        = string
}

variable "container_name" {
  description = "Name of the blob container."
  type        = string
}

variable "queue_name" {
  description = "Name of the storage queue."
  type        = string
}

variable "cosmosdb_account_name" {
  description = "Name of the Cosmos DB account."
  type        = string
}

variable "cosmosdb_database_name" {
  description = "Name of the Cosmos DB database."
  type        = string
}

variable "cosmosdb_container_name" {
  description = "Name of the Cosmos DB container."
  type        = string
}

variable "container_registry_name" {
  description = "Name of the Azure Container Registry."
  type        = string
}

variable "log_analytics_workspace_name" {
  description = "Name of the Log Analytics workspace."
  type        = string
}

variable "application_insights_name" {
  description = "Name of the Application Insights instance."
  type        = string
}

variable "search_service_name" {
  description = "Name of the Azure Cognitive Search service."
  type        = string
}

variable "openai_account_name" {
  description = "Name of the Azure OpenAI account."
  type        = string
}

variable "docintel_account_name" {
  description = "Name of the Azure Form Recognizer account."
  type        = string
}

variable "identity_name" {
  description = "Name of the user-assigned managed identity."
  type        = string
}

variable "container_apps_env_name" {
  description = "Name of the Container Apps environment."
  type        = string
}
