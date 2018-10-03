import sendgrid
import os

sg = sendgrid.SendGridAPIClient(apikey=os.environ.get('SENDGRID_API_KEY'))
data = {
  "personalizations": [
    {
      "to": [
        {
          "email": os.environ.get('DEFAULT_EMAIL')
        }
      ],
      "subject": "Sending IS Fun!",
      "custom_args": {
        "team": "EI",
        "name": "Anuj Shah"
      }
    }
  ],
  "from": {
    "email": os.environ.get('DEFAULT_EMAIL')
  },
  "content": [
    {
      "type": "text/plain",
      "value": "This email should have custom arguments and a category."
    }
  ],
  "categories": ["EI Data"]
}
response = sg.client.mail.send.post(request_body=data)
print(response.status_code)
print(response.body)
print(response.headers)