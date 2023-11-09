import * as pulumi from '@pulumi/pulumi'
import * as gcp from '@pulumi/gcp'

const gcpConfig = new pulumi.Config('gcp')
const projectId = gcpConfig.require('project')
const region = gcpConfig.require('region')

const app = new pulumi.Config('app')

const aiPredictionTopicName = 'ai-prediction'

// Create a service account
const cloudRunServiceAccountName = 'host-a-model-cloud-run-sa'
const serviceAccount = new gcp.serviceaccount.Account(
  cloudRunServiceAccountName,
  {
    accountId: cloudRunServiceAccountName,
    displayName: 'Service account for input cloud run',
    project: projectId,
  }
)

const imageSha = app.require('imageSha')
const imageUrl = app.require('imageUrl')
const imageName = `${imageUrl}@${imageSha}`

const apiService = new gcp.cloudrunv2.Service('api-service', {
  name: 'api-service',
  ingress: 'INGRESS_TRAFFIC_ALL',
  location: region,
  template: {
    scaling: {
      maxInstanceCount: 2,
    },
    volumes: [],
    containers: [
      {
        args: ['api:app', '--host', '0.0.0.0', '--port', '8080'],
        image: imageName,
        envs: [
          {
            name: 'PROJECT_ID',
            value: projectId,
          },
          {
            name: 'AI_PREDICTION_TOPIC',
            value: aiPredictionTopicName,
          },
        ],
        volumeMounts: [],
      },
    ],
    serviceAccount: serviceAccount.email,
  },
})

// Allow public traffic
const apiServiceAllUsersBinding = new gcp.cloudrun.IamBinding(
  'allow-all-users',
  {
    location: region,
    service: apiService.name,
    role: 'roles/run.invoker',
    members: ['allUsers'],
  }
)

const aiWorkerService = new gcp.cloudrunv2.Service('ai-worker-service', {
  name: 'ai-worker-service',
  ingress: 'INGRESS_TRAFFIC_ALL',
  location: region,
  template: {
    scaling: {
      maxInstanceCount: 2,
    },
    volumes: [],
    containers: [
      {
        args: ['ai_worker_api:app', '--host', '0.0.0.0', '--port', '8080'],
        image: imageName,
        envs: [
          {
            name: 'PROJECT_ID',
            value: projectId,
          },
        ],
        volumeMounts: [],
      },
    ],
    serviceAccount: serviceAccount.email,
  },
})

const exampleTopic = new gcp.pubsub.Topic(aiPredictionTopicName, {
  name: aiPredictionTopicName,
})

const pubsubInvokerServiceAccountName = 'pubsub-invoker-service-account'
const pubsubInvokerServiceAccount = new gcp.serviceaccount.Account(
  pubsubInvokerServiceAccountName,
  {
    accountId: pubsubInvokerServiceAccountName,
    displayName: 'Service account for invoking cloud run from pubsub',
    project: projectId,
  }
)

const pubsubInvokerServiceAccountBinding = new gcp.projects.IAMBinding(
  'pubsub-to-cloud-run-invoker',
  {
    project: projectId!,
    role: 'roles/run.invoker',
    members: [
      pulumi.interpolate`serviceAccount:${pubsubInvokerServiceAccount.email}`,
    ],
  }
)

const aiWorkerUrl = aiWorkerService.uri.apply((x) => `${x}/run_prediction`)

const exampleSub = new gcp.pubsub.Subscription('ai-prediction-cloud-run', {
  topic: exampleTopic.name,
  messageRetentionDuration: '1200s',
  pushConfig: {
    pushEndpoint: aiWorkerUrl,
    oidcToken: {
      serviceAccountEmail: pubsubInvokerServiceAccount.email,
    },
  },
  ackDeadlineSeconds: 30,
})

export const aiWorkerOutputUrl = aiWorkerUrl
