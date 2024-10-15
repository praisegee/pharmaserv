# call-report-summary-Project

## Description

A Flask app that give a summary of requests payload.

## Endpoints and the sample payload

### BaseURL: _https://api.ai.pharmaserv.co_

#### 1. _/summerize_

**Sample Request**

```json
[
  {
    "medRepId": "64cbb8f1af9faf444f0cc5d4",
    "hcpId": "66258f552c03a4262d152e71",
    "practitionerDetail": {
      "name": "Dr. John Doe 1",
      "deparment": "Cardiology",
      "category": "Specialist"
    },
    "detailedProducts": [
      {
        "name": "Emzor paracetamol ",
        "rxAmount": 72,
        "clinicalOverviewReaction": "Positive",
        "efficacyReaction": "Effective",
        "safetyReaction": "Safe"
      },
      {
        "name": "Emzor paracetamol ",
        "rxAmount": 36,
        "clinicalOverviewReaction": "Neutral",
        "efficacyReaction": "Moderate",
        "safetyReaction": "Safe"
      }
    ],
    "notes": {
      "objectionNotes": "None",
      "nextStepActionNotes": "Follow-up in 1 month"
    }
  }
  ...
]
```

**Sample Response**

```json
{
  "hcpId": "66258f552c03a4262d152e71",
  "medRepId": "64cbb8f1af9faf444f0cc5d4",
  "practitionerDetail": {
    "category": "Specialist",
    "deparment": "Cardiology",
    "name": "Dr. John Doe 1"
  },
  "summary": "**Summary and Recommendations of the Products' Reviews from the Practitioners' Perspectives:**\n\nHere are summaries"
}
```

#### 2. _/reports_

**Sample Request**

```bash
curl -X POST -F 'file=@sample_file.txt' https://api.ai.pharmaserv.co/reports
```

**Sample Response**

```json
[
    {
        "address": "42251 Salas Curve Suite 325, North Richardview, PA 95097",
        "company": "Henderson, Lozano and Andrews",
        "country": "Reunion",
        "dateOfBirth": "Mon, 19 Sep 1988 00:00:00 GMT",
        "department": "Neurology",
        "email": "rcastillo@moore.com",
        "firstName": "Monica",
        "lastName": "Wilson",
        "licenseNumber": "Piud-5858198",
        "npiNumber": 6924867223,
        "phoneNumber": "(042)382-2092",
        "specialty": "Pediatrician",
        "state": "Oklahoma",
        "title": "Engineer, electrical",
        "yearsOfExperience": 32
    },
    {
        "address": "237 Bradley Extensions Apt. 350, Michaelside, CA 46531",
        "company": "Reilly, Smith and Salazar",
        "country": "British Virgin Islands",
        "dateOfBirth": "Thu, 04 Apr 1985 00:00:00 GMT",
        "department": "Cardiology",
        "email": "ymorgan@quinn-roberson.net",
        "firstName": "Michael",
        "lastName": "Lopez",
        "licenseNumber": "VGCF-5917740",
        "npiNumber": 2462823438,
        "phoneNumber": "257-916-5093",
        "specialty": "Dermatologist",
        "state": "Hawaii",
        "title": "Programmer, systems",
        "yearsOfExperience": 11
    },
    ...
]
```
