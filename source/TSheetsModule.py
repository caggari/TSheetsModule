import json
import pandas as pd
from datetime import datetime


class TSheets:

    token

    def __init__(inpToken):
        token=inpToken

    def search(base_url, inpList, inpCode, inpToken):
        if inpList is None:
            inpList = []
        jobcodes_base_url = '{base_url}/jobcodes?'.format(base_url=base_url)
        if (inpCode == None):
            url = jobcodes_base_url
        else:
            url = "{base_url}parent_ids={inpCode}".format(base_url=jobcodes_base_url, inpCode=inpCode)
        headers = {
                'Authorization': "Bearer %s" % (inpToken),
        }
        response = requests.request("GET", url, headers=headers)
        jobData= json.loads(response.text)
        jobCodes= jobData['results']['jobcodes']
            
        for key in jobCodes:
            value = jobCodes[key]
            inpList.append(value)
            if value['has_children'] == True:
                search(base_url, inpList, value['id'], inpToken)
        return inpList

    def formatList(data_df)
        data_df.columns
        print(data_df.head())
        data_df['scale_id'] = data_df.index + 1
        data_df['last_modified'] = pd.to_datetime(data_df['last_modified'])#, unit='s').dt.tz_convert(None)
        data_df['created'] = pd.to_datetime(data_df['created'])#, unit='s').dt.tz_convert(None)

        data_df['last_modified'] = data_df['last_modified'].dt.tz_convert(None)
        data_df['created'] = data_df['created'].dt.tz_convert(None)
        print(data_df.head())



    
