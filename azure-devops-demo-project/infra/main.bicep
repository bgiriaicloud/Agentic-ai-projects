@description('Name of the web application. Must be globally unique.')
param webAppName string = 'devops-demo-web-${uniqueString(resourceGroup().id)}'

@description('The location where all resources will be deployed.')
param location string = resourceGroup().location

@description('The SKU of the App Service Plan.')
param skuName string = 'F1' // Free tier (Linux)

@description('The runtime stack of the web application.')
param linuxFxVersion string = 'NODE|20-lts'

@description('Custom welcome message environment variable.')
param customWelcomeMessage string = 'Hello from Azure App Service (Deployed via Bicep & CI/CD)!'

// 1. Log Analytics Workspace for monitoring logs
resource logAnalyticsWorkspace 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: '${webAppName}-workspace'
  location: location
  properties: {
    sku: {
      name: 'PerGB2018'
    }
    retentionInDays: 30
  }
}

// 2. Application Insights for app performance monitoring
resource appInsights 'Microsoft.Insights/components@2020-02-02' = {
  name: '${webAppName}-insights'
  location: location
  kind: 'web'
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: logAnalyticsWorkspace.id
  }
}

// 3. Linux App Service Plan (Server Farm)
resource appServicePlan 'Microsoft.Web/serverfarms@2023-01-01' = {
  name: '${webAppName}-plan'
  location: location
  sku: {
    name: skuName
  }
  kind: 'linux'
  properties: {
    reserved: true // Required for Linux plans
  }
}

// 4. Web Application (App Service)
resource webApp 'Microsoft.Web/sites@2023-01-01' = {
  name: webAppName
  location: location
  kind: 'app'
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      linuxFxVersion: linuxFxVersion
      appSettings: [
        {
          name: 'PORT'
          value: '8080'
        }
        {
          name: 'NODE_ENV'
          value: 'production'
        }
        {
          name: 'APPINSIGHTS_INSTRUMENTATIONKEY'
          value: appInsights.properties.InstrumentationKey
        }
        {
          name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
          value: appInsights.properties.ConnectionString
        }
        {
          name: 'CUSTOM_WELCOME_MESSAGE'
          value: customWelcomeMessage
        }
      ]
      alwaysOn: false // Must be false for Free (F1) tier plans
      ftpsState: 'FtpsOnly'
    }
    httpsOnly: true
  }
}

// Outputs to display post-deployment information
output webAppUrl string = 'https://${webApp.properties.defaultHostName}'
output resourceGroupName string = resourceGroup().name
output planName string = appServicePlan.name
