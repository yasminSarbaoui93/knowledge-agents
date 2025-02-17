param openAiName string
param principalId string

// https://learn.microsoft.com/en-us/azure/role-based-access-control/built-in-roles
// Cognitive Services OpenAI User
var openAiUserRole = subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '5e0bd9bd-7b93-4f28-af87-19fc36ad61bd')

resource openaiuser 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: openai // Use when specifying a scope that is different than the deployment scope
  name: guid(subscription().id, resourceGroup().id, principalId, openAiUserRole)
  properties: {
    roleDefinitionId: openAiUserRole
    principalType: 'ServicePrincipal'
    principalId: principalId
  }
}

// Cognitive Services OpenAI User
var cognitiveServiceContributorRole = subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '25fbc0a9-bd7c-42a3-aa1a-3b75d497ee68')

resource cognitiveServiceContributorAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: openai // Use when specifying a scope that is different than the deployment scope
  name: guid(subscription().id, resourceGroup().id, principalId, cognitiveServiceContributorRole)
  properties: {
    roleDefinitionId: cognitiveServiceContributorRole
    principalType: 'ServicePrincipal'
    principalId: principalId
  }
}

resource openai 'Microsoft.CognitiveServices/accounts@2022-10-01' existing = {
  name: openAiName
}
