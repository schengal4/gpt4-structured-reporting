# AI-Powered Radiology Report Structuring Tool
The "AI-Powered Radiology Report Structuring Tool" application is designed to enhance the utility of radiological documentation by transforming unstructured, narrative-style radiology reports into a structured, standardized format. By leveraging the OpenAI GPT-4 API, the application interprets free-text reports—submitted as .pdf, .docx, .txt files or directly pasted text—and systematically organizes the information into distinct fields. This structured output facilitates easier interpretation, comparison, and integration into health records systems.
## Instructions
1. Upload a radiology report as a .txt, .pdf, or .docx file. Or, enter/paste a radiology report into the text box and press Ctrl+Enter.  
2. Click the 'Submit' button.  
3. After ~20-25 seconds, the report will be structured and displayed below in JSON format or a table.  
To try an example, click the 'Try example' button. After ~20-25 seconds, the example report will be structured and displayed below in JSON format or a table.
## Repository Structure:

```
├── main.py: Contains the Streamlit interface.  
├── gpt.py: Contains the core functionality (the prompts used in the GPT-4 calls, processing of intermediate results).  
├── utils.py: Contains the functionality for processing user-uploaded files (.pdf, word, and .txt).
├── example_files: Folder with the file used when the user clicks the "Try Example" button.
├── reports: Folder that contains sample reports (comes from the parent kbressem/gpt4-structured-reporting repository).  
│   ├── structured_reports.json: Sample radiology reports w/ GPT-4-generated outputs (comes from kbressem/gpt4-structured-reporting)  
├── static 
│   ├── report_templates.json: contains the output templates sent to GPT-4 to help it select the best one.
```
## Credits
This app is a Streamlit adaptation of the [gpt4-structured-reporting](https://github.com/kbressem/gpt4-structured-reporting) GitHub repository, created by Keno Bressem, a board-certified radiologist. For more information about him, please see https://aim.hms.harvard.edu/team/keno-bressem.

The core functionality/prompts used are based on the paper [Leveraging GPT-4 for Post Hoc Transformation of Free-text Radiology Reports into Structured Reporting: A Multilingual Feasibility Study](https://doi.org/10.1148/radiol.230725), published in April 2023 and cited by 51+ different papers so far.

## Disclaimer
This app is for educational and research use only. Don't upload patient information or any other sensitive information to a third-party API.
    

