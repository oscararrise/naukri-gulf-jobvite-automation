import json 
import copy
import hashlib
import requests 
import json
import os
from dotenv import load_dotenv

load_dotenv()

headers = {
    "x-jvi-api": os.environ.get("X_JVI_API"),
    "x-jvi-sc": os.environ.get("X_JVI_SC"),
    "X-Company-Id": os.environ.get("X_COMPANY_ID"),
    "Accept": "application/json",
    "Content-Type": "application/json",
}
params = {
    "jobStatus": os.environ.get("JOB_STATUS"),
    "locCountry": os.environ.get("LOC_COUNTRY"),
    "start": int(os.environ.get("START", 1)),
    "count": int(os.environ.get("COUNT", 500)),
}

def create_keys(job_title, job_id):
    secret_key = os.environ.get("SECRET_KEY")
    access_key = os.environ.get("ACCESS_KEY")
    signature = hashlib.md5(f"{secret_key}{access_key}".encode()).hexdigest()
    en_access_key = hashlib.md5(f"{secret_key}{job_title}{job_id}{access_key}".encode()).hexdigest()
    return signature, en_access_key

def send_post_API(payload, signature, en_access_key):
    url = "https://www.naukrigulf.com/jpapi/job/offline/post"
    headers = {
        "Content-Type": "application/json",
        "accessKey": os.environ.get("ACCESS_KEY"),
        "enAccessKey": en_access_key,
        "signature": signature,
        "appId": os.environ.get("APP_ID"),
        "systemId": os.environ.get("SYSTEM_ID")
    }
    try:
        response = requests.post(url, headers=headers, json=payload)
        return response.json() if response.text else {"status": "success", "code": response.status_code}
    except requests.exceptions.RequestException as e:
        if hasattr(e, 'response') and e.response is not None:
            print(f"Respuesta del servidor: {e.response.text}")
        return None

PAYLOAD_TEMPLATE =  {
    "JobPositionPosting": {
        "JobAction": "ADD",
        "JobType": False,
        "JobPositionPostingID": "0000",
        "CompanyId": 337479,
        "HiringOrg": {
            "HideHiringOrgDetails": False,
            "Contact": {
                "VoiceNumber": {
                    "Mobile": "N/A",
                    "FaxNumber": "N/A",
                    "TelNumber": "N/A"
                },
                "FaxNumber": "",
                "CurrentLocation": 0
            }
        },
        "JobPositionInformation": {
            "JobPositionTitle": "N/A",
            "JobClassifications": {
                "PrimaryJobCategory": {
                        "JobIndustryCode": 1000,
                        "JobIndustryOther": "ARRISE",
                    "JobFunctionCode": 1000,
                    "JobFunctionOther": "Operations",
                }
            },
            "JobPositionDescription": {
                "JobKeywords": "N/A",
                "JobPositionLocation": {
                    "LocationType": "N/A",
                    "JobCountry": 17,
                    "JobCityLoc": "17.1",
                },
                "CompensationDescription": {
                    "Vacancies": 1,
                    "Pay": {
                        "CurrencyId": 1,
                        "MinimumSalary": 1,
                        "MaximumSalary": 1000
                    },
                    "BenifitsDescription": "N/A",
                    "SalaryDisplayOption": "N"
                },
                "SummaryText": "N/A"
            },
            "JobPositionRequirements": {
                "SummaryText": "N/A",
                "Nationality": "80,170",
                "Gender": "Any",
                "JobExperience": {
                    "MinimumExperience": 0,
                    "MaximumExperience": 0
                },
                "JobQualifications": {
                    "BasicQualifications": 1,
                    "BasicSpecializations": "1.2000",
                }
            }
        },
        "HowToApply": {
            "ApplicationMethods": {
                "ByWeb": {
                    "URL": "https://google.com"
                }
            }
        }
    }
}


