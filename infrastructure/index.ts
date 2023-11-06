import * as pulumi from '@pulumi/pulumi'
import * as gcp from '@pulumi/gcp'

const gcpConfig = new pulumi.Config('gcp')
const projectId = gcpConfig.require('project')
const region = gcpConfig.require('region')

const app = new pulumi.Config('app')

const cloudRunServiceAccount = app.require('cloudRunServiceAccount')

// Create a service account
const serviceAccount = new gcp.serviceaccount.Account(cloudRunServiceAccount, {
  accountId: `${cloudRunServiceAccount}`,
  displayName: 'Service account for input cloud run',
  project: projectId,
})

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
