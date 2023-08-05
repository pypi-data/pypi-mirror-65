#Heimdall Mail Notifier (HMN)
Heimdall mail notifier is executing an sql request on Heimdall violations database and sending the result by mail in attachment. 

##Pre-requisites
### Mailjet account
For sending mail a mailjet service account is needed.
### Service account (sa)
The CF SA should have those roles:
- roles/bigquery.dataViewer 
- role: roles/bigquery.jobUser
- roles/pubsub.editor
- role: roles/storage.objectViewer and permission on bucket

### bucket 
a bucket to store sql request is needed. 

### Secret in Secret Manager
HMN is looking for 2 secrets in secret manager (in the same project :
- mailjet_api_key
- mailjet_api_secret

## Principle
![](mail notifier.png)
HMN is listening in a pub-sub topic for message like: 

```
{   
    'requete': 'sql_file.sql', 
    'email': 'xxxx@adeo.com'
} 
```
For each message, CF is executing the sql request in violations database and send the result in attachment to email present in pub-sub


## Usefull Links
- secret Manager: https://cloud.google.com/secret-manager/docs/creating-and-accessing-secrets#secretmanager-create-secret-cli
- API Activation: https://cloud.google.com/endpoints/docs/openapi/enable-api