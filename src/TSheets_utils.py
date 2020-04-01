import json
import pandas as pd
from datetime import datetime
import requests


class TSheets:

    token

    def __init__(self, bearer_token):
        """
        :param bearer_token: grants access to TSheets
        """
        self.token=bearer_token
    
    def _search_(self, base_url, inpList, inpCode):
        """recursively search for TSheets jobCodes

        :param base_url: the url which search is called from
        :param inpList: list of jobCodes
        :param inpCode: parent of existing jobCodes
        """
        if inpList is None:
            inpList = []
        jobcodes_base_url = '{base_url}/jobcodes?'.format(base_url=base_url)
        if (inpCode == None):
            url = jobcodes_base_url
        else:
            url = "{base_url}parent_ids={inpCode}".format(base_url=jobcodes_base_url, inpCode=inpCode)
        headers = {
                'Authorization': "Bearer %s" % (self.token),
        }
        response = requests.request("GET", url, headers=headers)
        jobData= json.loads(response.text)
        jobCodes= jobData['results']['jobcodes']
            
        for key in jobCodes:
            value = jobCodes[key]
            inpList.append(value)
            if value['has_children'] == True:
                self._search_(base_url, inpList, value['id'])
        return inpList

    def _createDF_(self):
        """generates a new dataframe from tsheets data
        """
        tsheets_base_url = 'https://rest.tsheets.com/api/v1'
        mydata = self._search_(tsheets_base_url, None, None)
        data_df = pd.DataFrame.from_records(mydata)
        return data_df

    def _formatList_(self, data_df):
        """formats the data to Scale Marketing Standards
        :param data_df: unformatted dataframe
        """
        print(data_df)
        data_df['scale_id'] = data_df.index + 1
        data_df['last_modified'] = pd.to_datetime(data_df['last_modified'])#, unit='s').dt.tz_convert(None)
        data_df['created'] = pd.to_datetime(data_df['created'])#, unit='s').dt.tz_convert(None)

        data_df['last_modified'] = data_df['last_modified'].dt.tz_convert(None)
        data_df['created'] = data_df['created'].dt.tz_convert(None)
        return data_df

    def save_csv_file(self, file_base_path, current_datetime):
        """
        :param file_base_path:the path the file will be created at
        :param inpDateTime:the date given to the file location
        """
        unformatted_df=self._createDF_
        data_df=self._formatList_(unformatted_df)
        current_date = current_datetime
        data_df.rename(columns={'type':'timesheet_type'}, inplace=True)    
        cols = ['scale_id', 'parent_id', 'id', 'assigned_to_all', 'billable', 'active', 'timesheet_type',
            'has_children', 'billable_rate', 'short_code', 'name', 
            'project_id', 'locations', 'created', 'last_modified']
        for colname in ['assigned_to_all', 'billable', 'active', 'has_children']:
            data_df[colname][data_df[colname] == 'TRUE'] = 1
            data_df[colname][data_df[colname] == 'FALSE'] = 0
            data_df[colname] = data_df[colname].astype(int)

        out_file = '{folder}/tsheets_output_{year}_{month}_{day}.csv'.format(folder=file_base_path
                                                                     , year=current_date.year
                                                                     , month=str(current_date.month).zfill(2)
                                                                     , day=str(current_date.day).zfill(2))

        data_df.sort_values(['parent_id', 'id'])[cols].to_csv(out_file,index=False,sep=',')
        
    