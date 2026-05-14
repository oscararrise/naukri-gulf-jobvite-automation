import os
import traceback
import json
import requests
from statics import *
from openpyxl import Workbook, load_workbook
from datetime import datetime


def log_job_result(payload, result, filename='naukri_log.xlsx'):
    exists = os.path.exists(filename)
    if exists:
        wb = load_workbook(filename)
    else:
        wb = Workbook()
    if 'Success' not in wb.sheetnames:
        ws_s = wb.active
        ws_s.title = 'Success'
        ws_e = wb.create_sheet('Error')
    else:
        ws_s = wb['Success']
        ws_e = wb['Error'] if 'Error' in wb.sheetnames else wb.create_sheet('Error')
    status = 'success' if isinstance(result, dict) and result.get('status') == 'success' else 'error'
    sheet = ws_s if status == 'success' else ws_e
    timestamp = datetime.utcnow().isoformat()
    job_title = payload.get('JobPositionPosting', {}).get('JobPositionInformation', {}).get('JobPositionTitle', '')
    job_id = payload.get('JobPositionPosting', {}).get('JobPositionPostingID', '')
    sheet.append([timestamp, job_title, job_id, status, json.dumps(result)])
    wb.save(filename)


def publish_job_naukrigulf():
    resp = requests.get("https://api.jobvite.com/api/v2/job", headers=headers, params=params, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    try:
        for i in range(0,len(data['requisitions'])):
            print(f"Processing job {i+1}/{len(data['requisitions'])} - {data['requisitions'][i]['title']}")
            for customfield in data['requisitions'][i]["customField"]:
                if customfield['fieldCode'] == 'post_to_job_boards':
                    if data['requisitions'][i]['postingType'] == 'External':
                        var_job_title = data['requisitions'][i]['title']
                        var_job_id = data['requisitions'][i]['requisitionId']
                    signature, en_access_key = create_keys(var_job_title, var_job_id)
                    payload = copy.deepcopy(PAYLOAD_TEMPLATE)
                    payload["JobPositionPosting"]["JobPositionInformation"]["JobPositionTitle"] = var_job_title or ''
                    payload["JobPositionPosting"]["JobPositionPostingID"] = var_job_id or ''
                    location_value = ''
                    cf_list = data.get('requisitions', [])[i].get('customField', [])
                    if cf_list:
                        location_value = cf_list[0].get('value', '')
                    location_value = location_value.replace("On site", "ONSITE").replace("Remote", "REMOTE").replace("Hybrid", "HYBRID")
                    payload["JobPositionPosting"]["JobPositionInformation"]["JobPositionDescription"]["JobPositionLocation"]["LocationType"] = location_value
                    summary = data.get('requisitions', [])[i].get('description', '')
                    payload["JobPositionPosting"]["JobPositionInformation"]["JobPositionDescription"]["SummaryText"] = summary
                    payload["JobPositionPosting"]["JobPositionInformation"]["JobPositionRequirements"]["SummaryText"] = summary
                    payload["JobPositionPosting"]["HowToApply"]["ApplicationMethods"]["ByWeb"]["URL"] = data.get("requisitions", [])[i].get("applyLink", '')
                    if len(var_job_title) <= 70:
                        result = send_post_API(payload, signature, en_access_key)
                        log_job_result(payload, result)
                        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")                     
                        print(result)
                        print(f"Job {var_job_title} publish success on Naukri Gulf.")
                        print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    except Exception as e:
        print("Error naukri post job : ", str(e), traceback.format_exc())
publish_job_naukrigulf()



