from typing import List
from src.intent_handling.tool_strategy import Tool
import os
import requests
from dotenv import load_dotenv
load_dotenv('src/.env')

# this is a concrete strategy that implements the abstract one, so that we can have multiple
class CsDetectorTool(Tool):    
    last_repo = ""
    def execute_tool(self, data:List):
        print("\n\n\nSono in execute tool",data)
        print("\n\n\n")
        #if we have 2 entities (repo and date), we execute the tool with date parameter
        if data.__len__() > 2:
            req = requests.get(os.environ.get('CSDETECTOR_URL_GETSMELLS')+'?repo='+data[0]+'&pat='+os.environ.get('PAT',"")+"&date="+data[1])
        else:
            req = requests.get(os.environ.get('CSDETECTOR_URL_GETSMELLS')+'?repo='+data[0]+'&pat='+os.environ.get('PAT',"")) #+'&user='+data[data.__len__()-1]+"&graphs=True"
        
        #req.raise_for_status()
        response_json = req.json()

        if req.status_code == 890:
            error_text = response_json.get('error')
            code = response_json.get('code')
            results = [error_text, code]
            print("\n\nRESULTATO\n\n", results)
            return results

        print("\n\n\nStampa risposta",req.json())
        print("\n\n\n")
        # we retrieve the file names created by csdetector
        results = req.json().get("result")[1:]
        return results
