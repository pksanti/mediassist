import streamlit as st

__import__('pysqlite3')
#import sys
#sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import json
import os
from crewai import Agent, Task, Crew, Process, LLM
#from crewai_tools import (
#    FileReadTool
#)
#from crewai.tools import tool
#from textwrap import dedent
#from ibm_watson_machine_learning.foundation_models import Model
import requests
#from bs4 import BeautifulSoup
import pandas as pd
import re

model_id = "ibm/granite-3-2-8b-instruct"
project_id = 'a214617b-97d6-4aef-b555-876bf9385684'

parameters = {
    "decoding_method": "greedy",
    "max_new_tokens": 8000,
    "stop_sequences": ["Input:"],
    "repetition_penalty": 1
}

st.set_page_config(
    page_title = 'Chat'
)
st.html("""
    <style>
        .stMainBlockContainer {
            max-width:70rem;
        }
    </style>
    """
)
st.title('Autonomous Multi Agent Framwork')

def get_credentials():
    return {
        "url" : "https://us-south.ml.cloud.ibm.com",
        "apikey" : "gO-c7N7a44R81zutKkX4cR059Kb3ObI_xA4jKUs_BRfA"
    }


custom_headers = {
    "Accept": (
        "text/html,application/xhtml+xml,application/xml;"
        "q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "Gecko/20100101 Firefox/135.0"
    )

@st.dialog("Select")
def automultiagentselect():
    selection_options = {
    1: "Automated Smart Test Assistant",
    2: "Product Review System",
    3: "New Run",
    }
    userSelection = st.pills(
        "Please select to load an existing example or go for a new run",
        options=selection_options.keys(),
        format_func=lambda option: selection_options[option],
        selection_mode="single",
    )
    if userSelection is not None:
        if userSelection == 3:
            st.session_state.automultiagentselect = {"selected": "New Run"}
            st.rerun()
        else :
            st.session_state.automultiagentselect = {"selected": "Example" + str(userSelection)}
            st.rerun()

if "automultiagentselect" not in st.session_state:
    automultiagentselect()
else :
    selectedOption = st.session_state.automultiagentselect['selected']
    if selectedOption == 'New Run':
        usecaseName = st.text_input("Usecase Name", placeholder="Enter the name of the use case")
        businessProfile = st.text_area("Business Profile", placeholder="Enter the detailed business profile", height =68)

        bisRulesCol, inputDataCol = st.columns(2)
        with bisRulesCol:
            businessRules = st.text_area("Business Rules", placeholder="Enter the detailed business rules")
        with inputDataCol:
            inputData = st.text_area("Input Data", placeholder="Enter the input data")
    else :
        ucName, ebusinessProfile, ebusinessRules, einputData = getExampleSet(selectedOption)
        
        usecaseName = st.text_input("Usecase Name",value = ucName, placeholder="Enter the name of the use case")
        businessProfile = st.text_area("Business Profile",value = ebusinessProfile, placeholder="Enter the detailed business profile", height =68)

        bisRulesCol, inputDataCol = st.columns(2)
        with bisRulesCol:
            businessRules = st.text_area("Business Rules",value = ebusinessRules, placeholder="Enter the detailed business rules", height =160)
        with inputDataCol:
            inputData = st.text_area("Input Data",value = einputData, placeholder="Enter the input data", height =160)

    if(st.button('Initiate', type="secondary")):
        #masterAgentResp = master_agent_prompt_output(businessProfile, businessRules)
        #agentResp = worker_agents_prompt_output(businessProfile, businessRules, masterAgentResp['maResult'])
        #taskResp = task_prompt_output(businessProfile, masterAgentResp['maResult'], agentResp['agentResult'])          
        #finalOutput = multi_agent_crew(5, masterAgentResp['maResult'], agentResp['agentResult'], taskResp['taskResult'], inputData)         
        st.divider()
        st.header("Execution", divider="gray")

