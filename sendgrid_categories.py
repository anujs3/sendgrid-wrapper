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
      "subject": "Sending with SendGrid Is Fun"
    }
  ],
  "from": {
    "email": os.environ.get('DEFAULT_EMAIL')
  },
  "content": [
    {
      "type": "text/plain",
      "value": "This email should have a category attached to it."
    }
  ],
  "categories": ["EI Data", "Pipeline 2020"]
}
response = sg.client.mail.send.post(request_body=data)
print(response.status_code)
print(response.body)
print(response.headers)