import * as pulumi from '@pulumi/pulumi'
import * as gcp from '@pulumi/gcp'

const gcpConfig = new pulumi.Config('gcp')
const projectId = gcpConfig.require('project')
const region = gcpConfig.require('region')

const app = new pulumi.Config('app')

const aiPredictionTopicName = 'ai-prediction'

// Create a service account
const cloudRunServiceAccountName = 'host-a-model-cloud-run-sa'
const apiServiceAccount = new gcp.serviceaccount.Account(
  cloudRunServiceAccountName,
  {
    accountId: cloudRunServiceAccountName,
    displayName: 'Service account for input cloud run',
    project: projectId,
  }
)

const apiServiceAccountMember = apiServiceAccount.email.apply(
  (email) => `serviceAccount:${email}`
)
const topicIamBinding = new gcp.projects.IAMBinding("ai-request-topic-binding", {
  project: projectId,
  role: 'roles/pubsub.publisher',
  members: [apiServiceAccountMember],
})

const cloudRunPubSubSubscriberIamBinding = new gcp.projects.IAMBinding(
  'api-cloud-run-pubsub-subscriber',
  {
    project: projectId,
    role: 'roles/pubsub.subscriber',
    members: [apiServiceAccountMember],
  }
)

const cloudRunInvokerIamBinding = new gcp.projects.IAMBinding(
  'api-cloud-run-invoker',
  {
    project: projectId,
    role: 'roles/run.invoker',
    members: [apiServiceAccountMember],
  }
)

const fireStoreIamBinding = new gcp.projects.IAMBinding(
  'firestore-binding',
  {
    project: projectId,
    role: 'roles/datastore.user',
    members: [apiServiceAccountMember],
  }
)

const imageSha = app.require('imageSha')
const imageUrl = app.require('imageUrl')
const imageName = `${imageUrl}@${imageSha}`

const commonEnvironmentVariables = [
  {
    name: 'PROJECT_ID',
    value: projectId,
  },
  {
    name: 'AI_PREDICTION_TOPIC',
    value: aiPredictionTopicName,
  },
]

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
        args: ['main_api:app', '--host', '0.0.0.0', '--port', '8080'],
        image: imageName,
        envs: [
          ...commonEnvironmentVariables
        ],
        volumeMounts: [],
      },
    ],
    serviceAccount: apiServiceAccount.email,
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
          ...commonEnvironmentVariables
        ],
        volumeMounts: [],
      },
    ],
    serviceAccount: apiServiceAccount.email,
  },
})

const aiRequestTopic = new gcp.pubsub.Topic(aiPredictionTopicName, {
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


const pubsubInvokerServiceAccountMember = pubsubInvokerServiceAccount.email.apply(
  (email) => `serviceAccount:${email}`
)
const pubsubInvokerServiceAccountBinding = new gcp.projects.IAMBinding(
  'pubsub-to-cloud-run-invoker',
  {
    project: projectId,
    role: 'roles/run.invoker',
    members: [
      pubsubInvokerServiceAccountMember,
    ],
  }
)

const aiWorkerBaseUrl = aiWorkerService.uri.apply((x) => `${x}/`)
const aiWorkerPredictionUrl = aiWorkerService.uri.apply((x) => `${x}/queued_prediction`)
const aiWorkerDeleteExpiredRequestsUrl = aiWorkerService.uri.apply((x) => `${x}/delete_expired_requests`)


const aiPredictionSub = new gcp.pubsub.Subscription('ai-prediction-cloud-run', {
  topic: aiRequestTopic.name,
  messageRetentionDuration: '1200s',
  pushConfig: {
    pushEndpoint: aiWorkerPredictionUrl,
    noWrapper: {
      writeMetadata: true
    },
    oidcToken: {
      serviceAccountEmail: pubsubInvokerServiceAccount.email,
      audience: aiWorkerBaseUrl,
    },
  },
  ackDeadlineSeconds: 30,
})


const aiWorkerSchedulerJob = new gcp.cloudscheduler.Job("ai-worker-scheduler-cleanup-job", {
  name: "ai-worker-daily-cleanup",
  description: "Daily trigger for ai-worker-service to clean up old requests",
  schedule: "0 0 * * *",  // Every day at midnight
  timeZone: "Etc/UTC",     // Specify the time zone
  httpTarget: {
    uri: aiWorkerDeleteExpiredRequestsUrl,
    httpMethod: "POST",
    oidcToken: {
      serviceAccountEmail: pubsubInvokerServiceAccount.email,
      audience: aiWorkerBaseUrl,
    },
  },
  project: projectId,
  region: region,
});

export const aiWorkerOutputUrl = aiWorkerBaseUrl
