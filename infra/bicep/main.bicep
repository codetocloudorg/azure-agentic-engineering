// =============================================================================
// Azure AI Infrastructure - Main Deployment
// =============================================================================
// This template deploys the core infrastructure for Azure AI applications
// following the AI Landing Zone pattern.
//
// Author: Code to Cloud Team
// =============================================================================

targetScope = 'resourceGroup'

// =============================================================================
// Parameters
// =============================================================================

@description('Environment name (e.g., dev, staging, prod)')
@allowed(['dev', 'staging', 'prod'])
param environmentName string = 'dev'

@description('Azure region for resources')
param location string = resourceGroup().location

@description('Principal ID for role assignments (e.g., user or managed identity)')
param principalId string

@description('Tags to apply to all resources')
param tags object = {
  Environment: environmentName
  Project: 'azure-agentic-engineering'
  Team: 'code-to-cloud'
}

// =============================================================================
// Variables
// =============================================================================

var resourcePrefix = 'aae-${environmentName}'
var uniqueSuffix = uniqueString(resourceGroup().id)

// =============================================================================
// Modules
// =============================================================================

// Log Analytics Workspace for monitoring
module monitoring 'modules/monitoring.bicep' = {
  name: 'monitoring-${uniqueSuffix}'
  params: {
    name: '${resourcePrefix}-law'
    location: location
    tags: tags
  }
}

// Key Vault for secrets management
module keyVault 'modules/keyvault.bicep' = {
  name: 'keyvault-${uniqueSuffix}'
  params: {
    name: '${resourcePrefix}-kv-${uniqueSuffix}'
    location: location
    tags: tags
    principalId: principalId
    logAnalyticsWorkspaceId: monitoring.outputs.workspaceId
  }
}

// Azure OpenAI Service
module openAI 'modules/openai.bicep' = {
  name: 'openai-${uniqueSuffix}'
  params: {
    name: '${resourcePrefix}-oai-${uniqueSuffix}'
    location: location
    tags: tags
    principalId: principalId
    logAnalyticsWorkspaceId: monitoring.outputs.workspaceId
    deployments: [
      {
        name: 'gpt-4o'
        model: 'gpt-4o'
        version: '2024-08-06'
        capacity: 10
      }
      {
        name: 'text-embedding-3-large'
        model: 'text-embedding-3-large'
        version: '1'
        capacity: 10
      }
    ]
  }
}

// Azure AI Search for RAG
module aiSearch 'modules/ai-search.bicep' = {
  name: 'aisearch-${uniqueSuffix}'
  params: {
    name: '${resourcePrefix}-search-${uniqueSuffix}'
    location: location
    tags: tags
    principalId: principalId
    logAnalyticsWorkspaceId: monitoring.outputs.workspaceId
  }
}

// Storage Account for data
module storage 'modules/storage.bicep' = {
  name: 'storage-${uniqueSuffix}'
  params: {
    name: replace('${resourcePrefix}st${uniqueSuffix}', '-', '')
    location: location
    tags: tags
    principalId: principalId
  }
}

// =============================================================================
// Outputs
// =============================================================================

@description('OpenAI endpoint URL')
output openAIEndpoint string = openAI.outputs.endpoint

@description('AI Search endpoint URL')
output aiSearchEndpoint string = aiSearch.outputs.endpoint

@description('Key Vault URI')
output keyVaultUri string = keyVault.outputs.uri

@description('Log Analytics Workspace ID')
output logAnalyticsWorkspaceId string = monitoring.outputs.workspaceId

@description('Storage Account name')
output storageAccountName string = storage.outputs.name
