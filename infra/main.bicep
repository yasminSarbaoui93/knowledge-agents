targetScope = 'subscription'

@minLength(1)
@maxLength(64)
@description('Name of the the environment which is used to generate a short unique hash used in all resources.')
param environmentName string

@minLength(1)
@description('Primary location for all resources')
param location string
param aiResourceLocation string
@description('Id of the user or app to assign application roles')
param resourceGroupName string = ''
param containerAppsEnvironmentName string = ''
param storageAccountName string = ''
param containerName string = 'documents'
param queueName string = 'requests'
param containerRegistryName string = ''
param openaiName string = ''
param cosmosDbAccountName string = ''
param cosmosDatabaseName string = 'financialagents'
param cosmosContainerName string = 'documents'
param applicationInsightsDashboardName string = ''
param applicationInsightsName string = ''
param logAnalyticsName string = ''

var abbrs = loadJsonContent('./abbreviations.json')
var resourceToken = toLower(uniqueString(subscription().id, environmentName, location))
var tags = { 'azd-env-name': environmentName, 'app': 'ai-agents', 'tracing': 'yes' }
param searchIndexName string = 'search-index'
param completionDeploymentModelName string = 'gpt-4o'
param completionModelName string = 'gpt-4o'
param completionModelVersion string = '2024-08-06'
param smallcompletionDeploymentModelName string = 'gpt-4o-mini'
param smallcompletionModelName string = 'gpt-4o-mini'
param smallcompletionModelVersion string = '2024-07-18'
param embeddingDeploymentModelName string = 'text-embedding-3-large'
param embeddingModelName string = 'text-embedding-3-large'
param embeddingModelVersion string = '1'
param openaiApiVersion string = '2024-08-01-preview'
param openaiCapacity int = 50
param modelDeployments array = [
  {
    name: completionDeploymentModelName
    model: {
      format: 'OpenAI'
      name: completionModelName
      version: completionModelVersion
    }
  }
  {
    name: smallcompletionDeploymentModelName
    model: {
      format: 'OpenAI'
      name: smallcompletionModelName
      version: smallcompletionModelVersion
    }
  }
  {
    name: embeddingDeploymentModelName
    model: {
      format: 'OpenAI'
      name: embeddingModelName
      version: embeddingModelVersion
    }
  }
]

// Organize resources in a resource group
resource resourceGroup 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: !empty(resourceGroupName) ? resourceGroupName : '${abbrs.resourcesResourceGroups}${environmentName}'
  location: location
  tags: tags
}

// Container apps host (including container registry)
module containerApps './core/host/container-apps.bicep' = {
  name: 'container-apps'
  scope: resourceGroup
  params: {
    name: 'app'
    documentIntelName: docintel.outputs.accountName
    storageAccountName: storage.outputs.storageAccountName
    containerAppsEnvironmentName: !empty(containerAppsEnvironmentName) ? containerAppsEnvironmentName : '${abbrs.appManagedEnvironments}${resourceToken}'
    containerRegistryName: !empty(containerRegistryName) ? containerRegistryName : '${abbrs.containerRegistryRegistries}${resourceToken}'
    location: location
    logAnalyticsWorkspaceName: monitoring.outputs.logAnalyticsWorkspaceName
    applicationInsightsName: monitoring.outputs.applicationInsightsName
    identityName: '${abbrs.managedIdentityUserAssignedIdentities}api-agents'
    openaiName: openai.outputs.openaiName
    searchName: search.outputs.searchName
  }
}

// Azure OpenAI Model
module openai './ai/openai.bicep' = {
  name: 'openai'
  scope: resourceGroup
  params: {
    location: !empty(aiResourceLocation) ? aiResourceLocation : location
    tags: tags
    customDomainName: !empty(openaiName) ? openaiName : '${abbrs.cognitiveServicesAccounts}${resourceToken}'
    name: !empty(openaiName) ? openaiName : '${abbrs.cognitiveServicesAccounts}${resourceToken}'
    deployments: modelDeployments
    capacity: openaiCapacity
  }
}

module docintel './ai/docintel.bicep' = {
  name: 'docintel'
  scope: resourceGroup
  params: {
    location: !empty(aiResourceLocation) ? aiResourceLocation : location
    tags: tags
    name: !empty(openaiName) ? openaiName : '${abbrs.cognitiveServicesFormRecognizer}${resourceToken}'
  }
}

module cosmodDb './core/data/cosmosdb.bicep' = {
  name: 'sql'
  scope: resourceGroup
  params: {
    location: location
    accountName: !empty(cosmosDbAccountName) ? cosmosDbAccountName : '${abbrs.cosmosDbAccount}${resourceToken}'
    databaseName: cosmosDatabaseName
    containerName: cosmosContainerName
    tags: tags
  }
}

module storage './core/data/storage.bicep' = {
  name: 'storage'
  scope: resourceGroup
  params: {
    storageAccountName: !empty(storageAccountName) ? storageAccountName : '${abbrs.storageAccounts}${resourceToken}'
    containerName: containerName
    queueName: queueName
  }
}

module search './ai/search.bicep' = {
  name: 'search'
  scope: resourceGroup
  params: {
    location: location
    tags: tags
    name: !empty(openaiName) ? openaiName : '${abbrs.searchSearchServices}${resourceToken}'
  }
}

// Monitor application with Azure Monitor
module monitoring './core/monitor/monitoring.bicep' = {
  name: 'monitoring'
  scope: resourceGroup
  params: {
    location: location
    tags: tags
    logAnalyticsName: !empty(logAnalyticsName) ? logAnalyticsName : '${abbrs.operationalInsightsWorkspaces}${resourceToken}'
    applicationInsightsName: !empty(applicationInsightsName) ? applicationInsightsName : '${abbrs.insightsComponents}${resourceToken}'
    applicationInsightsDashboardName: !empty(applicationInsightsDashboardName) ? applicationInsightsDashboardName : '${abbrs.portalDashboards}${resourceToken}'
  }
}

output AZURE_LOCATION string = location
output AZURE_TENANT_ID string = tenant().tenantId
output AZURE_RESOURCE_GROUP string = resourceGroup.name

output APPLICATIONINSIGHTS_CONNECTION_STRING string = monitoring.outputs.applicationInsightsConnectionString
output APPLICATIONINSIGHTS_NAME string = monitoring.outputs.applicationInsightsName
output AZURE_CONTAINER_ENVIRONMENT_NAME string = containerApps.outputs.environmentName
output AZURE_CONTAINER_REGISTRY_ENDPOINT string = containerApps.outputs.registryLoginServer
output AZURE_CONTAINER_REGISTRY_NAME string = containerApps.outputs.registryName
output COSMOSDB_ENDPOINT string = cosmodDb.outputs.endpoint
output COSMOSDB_DATABASE_NAME string = cosmosDatabaseName
output COSMOSDB_CONTAINER_NAME string = cosmosContainerName
output OPENAI_API_TYPE string = 'azure'
output AZURE_OPENAI_API_VERSION string = openaiApiVersion
output OPENAI_API_VERSION string = openaiApiVersion
output AZURE_OPENAI_API_KEY string = openai.outputs.openaiKey
output AZURE_OPENAI_ENDPOINT string = openai.outputs.openaiEndpoint
output AZURE_OPENAI_COMPLETION_MODEL string = completionModelName
output AZURE_OPENAI_COMPLETION_DEPLOYMENT_NAME string = completionDeploymentModelName
output AZURE_OPENAI_SMALL_COMPLETION_MODEL string = smallcompletionModelName
output AZURE_OPENAI_SMALL_COMPLETION_DEPLOYMENT_NAME string = smallcompletionDeploymentModelName
output AZURE_OPENAI_SMALL_COMPLETION_MODEL_VERSION string = smallcompletionModelVersion
output AZURE_OPENAI_EMBEDDING_MODEL string = embeddingModelName
output AZURE_OPENAI_EMBEDDING_DEPLOYMENT_NAME string = embeddingDeploymentModelName
output AZURE_AI_SEARCH_NAME string = search.outputs.searchName
output AZURE_AI_SEARCH_ENDPOINT string = search.outputs.searchEndpoint
output AZURE_AI_SEARCH_KEY string = search.outputs.searchAdminKey
output AZURE_AI_SEARCH_INDEX string = searchIndexName
output STORAGE_ACCOUNT_URL string = storage.outputs.storageAccountUrl
output BACKEND_API_URL string = 'http://localhost:8000'
output FRONTEND_SITE_NAME string = 'http://127.0.0.1:3000'
output KM_SERVICE_AUTHORIZATION string = containerApps.outputs.kmauthorization
output KM_SERVICE_URL string = containerApps.outputs.kmserviceurl

