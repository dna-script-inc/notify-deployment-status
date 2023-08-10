import requests
import json
import os
from datetime import datetime

message = '''
{
  "type": "message",
  "attachments": [
    {
      "contentType": "application/vnd.microsoft.card.adaptive",
      "content": {
        "type": "AdaptiveCard",
        "msteams": {
          "width": "Full",
          "entities": [
            $mention
          ]
        },
        "body": [
          {
            "type": "Container",
            "items": [
              {
                "type": "TextBlock",
                "text": "$title",
                "weight": "bolder",
                "size": "medium"
              },
              {
                "type": "ColumnSet",
                "columns": [
                  {
                    "type": "Column",
                    "width": "auto",
                    "items": [
                      {
                        "type": "Image",
                        "url": "$image",
                        "size": "Small",
                        "style": "Person"
                      }
                    ]
                  },
                  {
                    "type": "Column",
                    "width": "stretch",
                    "items": [
                      {
                        "type": "TextBlock",
                        "text": "Via Github Action",
                        "weight": "Bolder",
                        "wrap": true
                      },
                      {
                        "type": "TextBlock",
                        "spacing": "None",
                        "text": "$date",
                        "isSubtle": true,
                        "wrap": true
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "type": "Container",
            "items": [
              {
                "type": "TextBlock",
                "text": "$description",
                "wrap": true
              },
              {
                "type": "FactSet",
                "facts": [
                  {
                    "title": "Sha:",
                    "value": "$sha"
                  },
                  {
                    "title": "Actor:",
                    "value": "$actor"
                  }
                ]
              }
            ]
          }
        ],
        "actions": [
          {
            "type": "Action.OpenUrl",
            "title": "View Workflow Run",
            "url": "$url"
          }
        ]
      }
    }
  ]
}
'''


statuses = [
    {
        "id": "failure",
        "title": "Failed to deploy redbox service",
        "image": "https://dnas-public.s3.us-west-1.amazonaws.com/failed.png",
        "description": "The redbox service has not been deployed to QA enviroment. Please have a look <at>Truong PHAM</at>, <at>My NGUYEN</at>"
    },
    {
        "id": "success",
        "title": "Succeed to deploy redbox service",
        "image": "https://dnas-public.s3.us-west-1.amazonaws.com/passed.png",
        "description": "The redbox service has been deployed to QA enviroment successfully."
    }
]

unknown_status = {
    "id": "unknown",
    "title": "Deploy redbox service with unknown status",
    "image": "https://dnas-public.s3.us-west-1.amazonaws.com/warning.png",
    "description": "The redbox service has not been deployed to QA enviroment. Please have a look <at>Truong PHAM</at>, <at>My NGUYEN</at>"
}

sha = os.getenv("SHA", "")
status = os.getenv("STATUS", "success")
github_run_url = os.getenv('GITHUB_RUN_URL', "")
webhook_url = os.getenv('WEBHOOK_URL')
actor = os.getenv('GITHUB_ACTOR', "")
mention = os.getenv('MENTION', "")


st = next(filter(lambda d: d["id"] == status, statuses), unknown_status)

if st["id"] == 'success':
    mention = ""

message = message.replace('$mention', mention)
message = message.replace("$title", st["title"])
message = message.replace("$image", st["image"])
message = message.replace("$date", datetime.utcnow().strftime("%d-%b-%Y %H:%M:%S UTC"))
message = message.replace("$description", st["description"])
message = message.replace("$url", github_run_url)
message = message.replace("$sha", sha)
message = message.replace("$actor", actor)
print(message)
#resp = requests.post(webhook_url, json=json.loads(message))
#print(resp.text)
