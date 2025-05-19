terraform {
  required_version = ">= 1.5.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.100.0"
    }
    random = {
      source = "hashicorp/random"
      version = ">= 3.5.0"
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id = var.subscription_id
}

#-------------------
# Resource Group
#-------------------
resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.location
  tags     = var.tags
}

#-------------------
# Storage Account, Blob Container, Queue
#-------------------
resource "azurerm_storage_account" "main" {
  name                     = var.storage_account_name
  resource_group_name      = azurerm_resource_group.main.name
  location                 = azurerm_resource_group.main.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
  min_tls_version          = "TLS1_2"
  tags                     = var.tags
}

resource "azurerm_storage_container" "main" {
  name                  = var.container_name
  storage_account_name  = azurerm_storage_account.main.name
  container_access_type = "private"
}

resource "azurerm_storage_queue" "main" {
  name                 = var.queue_name
  storage_account_name = azurerm_storage_account.main.name
}

#-------------------
# Cosmos DB
#-------------------
resource "azurerm_cosmosdb_account" "main" {
  name                = var.cosmosdb_account_name
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  offer_type          = "Standard"
  kind                = "GlobalDocumentDB"
  consistency_policy {
    consistency_level = "Session"
  }
  geo_location {
    location          = azurerm_resource_group.main.location
    failover_priority = 0
  }
  capabilities {
    name = "EnableServerless"
  }
  capabilities {
    name = "EnableNoSQLVectorSearch"
  }
  public_network_access_enabled = true
  tags = var.tags
}

resource "azurerm_cosmosdb_sql_database" "main" {
  name                = var.cosmosdb_database_name
  resource_group_name = azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
}

resource "azurerm_cosmosdb_sql_container" "documents" {
  name                = var.cosmosdb_container_name
  resource_group_name = azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
  database_name       = azurerm_cosmosdb_sql_database.main.name
  partition_key_paths = ["/id"]
}

resource "azurerm_cosmosdb_sql_container" "memory" {
  name                = "memory"
  resource_group_name = azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
  database_name       = azurerm_cosmosdb_sql_database.main.name
  partition_key_paths = ["/id"]
}

#-------------------
# Container Registry
#-------------------
resource "azurerm_container_registry" "main" {
  name                = var.container_registry_name
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  sku                 = "Standard"
  admin_enabled       = true
  tags                = var.tags
}

#-------------------
# Log Analytics Workspace
#-------------------
resource "azurerm_log_analytics_workspace" "main" {
  name                = var.log_analytics_workspace_name
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
  tags                = var.tags
}

#-------------------
# Application Insights
#-------------------
resource "azurerm_application_insights" "main" {
  name                = var.application_insights_name
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  application_type    = "web"
  workspace_id        = azurerm_log_analytics_workspace.main.id
  tags                = var.tags
}

#-------------------
# Azure AI Search
#-------------------
resource "azurerm_search_service" "main" {
  name                = var.search_service_name
  resource_group_name = azurerm_resource_group.main.name
  location            = azurerm_resource_group.main.location
  sku                 = "standard"
  replica_count       = 1
  partition_count     = 1
  tags                = var.tags
  public_network_access_enabled = true
}

#-------------------
# Azure Cognitive Services (OpenAI, Form Recognizer)
#-------------------
resource "azurerm_cognitive_account" "openai" {
  name                = var.openai_account_name
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  kind                = "OpenAI"
  sku_name            = "S0"
  tags                = var.tags
  identity {
    type = "SystemAssigned"
  }
  public_network_access_enabled = true
}

resource "azurerm_cognitive_account" "docintel" {
  name                = var.docintel_account_name
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  kind                = "FormRecognizer"
  sku_name            = "S0"
  tags                = var.tags
  public_network_access_enabled = true
}

#-------------------
# Managed Identity
#-------------------
resource "azurerm_user_assigned_identity" "main" {
  name                = var.identity_name
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  tags                = var.tags
}

#-------------------
# Container Apps Environment
#-------------------
resource "azurerm_container_app_environment" "main" {
  name                = var.container_apps_env_name
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.main.id
  tags                = var.tags
}

#-------------------
# Outputs
#-------------------
output "resource_group_name" {
  value = azurerm_resource_group.main.name
}
output "storage_account_name" {
  value = azurerm_storage_account.main.name
}
output "cosmosdb_account_name" {
  value = azurerm_cosmosdb_account.main.name
}
output "container_registry_name" {
  value = azurerm_container_registry.main.name
}
output "log_analytics_workspace_name" {
  value = azurerm_log_analytics_workspace.main.name
}
output "application_insights_name" {
  value = azurerm_application_insights.main.name
}
output "search_service_name" {
  value = azurerm_search_service.main.name
}
output "openai_account_name" {
  value = azurerm_cognitive_account.openai.name
}
output "docintel_account_name" {
  value = azurerm_cognitive_account.docintel.name
}
output "container_apps_env_name" {
  value = azurerm_container_app_environment.main.name
}
output "identity_name" {
  value = azurerm_user_assigned_identity.main.name
}
