import streamlit as st
from gpt import GPTStructuredReporting
import os
import json
from utils import read_docx, text_from_pdf_file, text_from_pdf_file_path, json_to_table
import pandas as pd

improvement_suggestions = """
1. Use company API key instead of the developer's.
2. Declutter UI.
3.. When downloading csv, make it such that the findings are not displayed in 
one long line; instead broken up into multiple lines (but still the same cells).
4. Make the app HIPAA-compliant and GDPR-compliant, including the call to openai api.
5. Beautify the app.
"""

decluttering_ui_steps = """
1. Formatting errors
2. Button layout
3. Section layout
"""
def upload_file():
    uploaded_file = st.file_uploader("Choose a file", type=['txt', 'pdf', 'docx'])
    if uploaded_file is not None:
        if uploaded_file.type == 'application/pdf':
            report = text_from_pdf_file(uploaded_file)
        elif uploaded_file.type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            report = read_docx(uploaded_file)
        elif uploaded_file.type == 'text/plain':
            # Decode the byte content to string
            report = str(uploaded_file.read(), 'utf-8')
        print(report)
        return report
    else:
        return None
@st.cache_data
def process_report_helper(report, api_key, test=False):
    # Initialize the GPTStructuredReporting class with the API key and template path.
    if not test:
        gpt = GPTStructuredReporting(api_key, "static/report_templates.json")
    else: # For developers developing the app, use the turbo model to speed up development and reduce costs.
        gpt = GPTStructuredReporting(api_key, "static/report_templates.json", model="gpt-3.5-turbo")
    # Process the report and capture the structured result.
    structured_report = gpt(report)
    return structured_report

def process_report(report, api_key, test=False):
    with st.spinner('Processing and structuring report...'):
        try: 
            st.session_state["structured_report"] = process_report_helper(report, api_key, test)
        except Exception as e:
            if "Incorrect API key" in str(e):
                st.error("Incorrect API key used in the program. Please leave a comment in the comments section about this so I can know.")
            else:
                st.error("An error occurred while processing the report. Please leave a comment in the comments section about this so I can know.")
                st.error("Error: " + str(e))
def initialize_session_state():
    if "structured_report" not in st.session_state:
        st.session_state["structured_report"] = None
    if "OPENAI_API_KEY" not in st.session_state:
        try:
            from secret_keys import OPENAI_API_KEY
            st.session_state["OPENAI_API_KEY"] = OPENAI_API_KEY
        except:
            st.session_state["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")
def instructions():
    st.write("This tool is designed to help radiologists structure their reports. \
             It uses the OpenAI API (GPT-4) to generate the structured report.")
    st.write("**Instructions**")
    st.write("""
              1. Upload a radiology report as a .txt, .pdf, or .docx file. Or, enter/paste a radiology report into the text box and press Ctrl+Enter.
              2. Click the 'Submit' button.  
              3. After ~20-25 seconds, the report will be structured and displayed below in a table or JSON format.  
             
            To try an example, click the 'Try example' button. After ~20-25 seconds, the \
            example report will be structured and displayed below in JSON format.
             """)
def credits():
    st.write("**Credits**")
    st.write("This app is a Streamlit adaptation of the [gpt4-structured-reporting](https://github.com/kbressem/gpt4-structured-reporting) GitHub repository, \
             created by Keno Bressem, a board-certified radiologist. For more information about him, please \
             see https://aim.hms.harvard.edu/team/keno-bressem.")
def disclaimer():
     st.warning("This app is for educational and resource use only. Don't upload patient information or any other sensitive information to a third party API.")
    

def main(): 
  initialize_session_state()
  # Set up the title and instructions for the Streamlit app interface.
  st.title('Radiology Report Structuring Tool')
  instructions()
  credits()
  disclaimer()


  # Create a text area in the UI for the user to input or paste the radiology report.
  report_upload_option = st.radio("Option for entering the report", ("Upload report as file", "Paste report"), horizontal=True)
  if report_upload_option == "Paste report":
      text_container = st.empty()
      report = text_container.text_area("Report")
  else:
      report = upload_file() #User uploads a file and it gets converted to text. Doesn't support images or bold/italics/underline/color yet.
  # Create try example button
  # The submit button for processing the report.
  
  try_example = st.button("Try example")
  button = st.button("Submit")

  if not st.session_state["structured_report"] and not try_example and (not report or not report.strip()):
      st.stop()
  # OpenAI API key from session state
  api_key = st.session_state["OPENAI_API_KEY"]

  if try_example:
      # This worked well, but "VASCULAR TUMOR INVOLVEMENT AND DEGREE" was classified as "No", different than the provided test case
      if report_upload_option == "Paste report":
          EXAMPLE = """
      CLINICAL HISTORY: Evaluation for pancreatic cancer.
      TECHNIQUE: Non-contrast, arterial phase, and venous phase contrast-enhanced CT images of the abdomen and pelvis were obtained using a multidetector CT scanner. Multiplanar reformations were also reviewed.
      FINDINGS: 
          Pancreatic tumor: There is a 3.5 x 3.2 x 2.8 cm hypodense mass in the pancreatic head, which demonstrates mild heterogeneous enhancement on arterial and venous phases. The mass causes mild upstream dilation of the pancreatic duct, measuring up to 4 mm in diameter. There is no pancreatic parenchymal atrophy.
          Metastatic disease: Multiple liver lesions are identified, the largest being in segment VIII, measuring 2.3 x 1.8 cm, with arterial enhancement and washout on the venous phase, consistent with metastatic deposits. No intrahepatic biliary dilatation is observed. There are enlarged peripancreatic, porta hepatis, and retroperitoneal lymph nodes, the largest measuring 1.8 x 1.3 cm. No pelvic or retrocrural lymphadenopathy is detected. No suspicious lung nodules or pleural effusions are noted.
          Vascular involvement: The pancreatic mass encases the superior mesenteric vein (SMV) and partially compresses it, with less than 50% narrowing of the vessel lumen. The main portal vein, splenic vein, and superior mesenteric artery (SMA) are patent and not encased by the tumor. No signs of cavernous transformation are observed.
          Thrombosis: No thrombus is identified within the portal vein, SMV, splenic vein, or inferior vena cava (IVC).
          Anatomy: The liver, spleen, adrenal glands, and kidneys demonstrate normal size, shape, and enhancement pattern. No renal or ureteral calculi are detected. The gallbladder, appendix, and bowel loops are unremarkable. No free fluid or air is observed in the abdominal or pelvic cavities.
      IMPRESSION: Hypodense mass in the pancreatic head, measuring 3.5 x 3.2 x 2.8 cm, consistent with a pancreatic neoplasm. Multiple liver lesions consistent with metastatic disease. Enlarged peripancreatic, porta hepatis, and retroperitoneal lymph nodes, suggestive of lymph node metastases. Partial encasement and compression of the superior mesenteric vein by the pancreatic mass, without thrombosis. No other vascular involvement or thrombosis identified. No additional intra-abdominal or pelvic pathologies detected.
      """
      
          report = text_container.text_area("Report", value=EXAMPLE, height=400, max_chars=10000) 
      elif report_upload_option == "Upload report as file":
          report = text_from_pdf_file_path("example_files/sample_radiology_report.pdf")
      process_report(report, api_key, test=False)  

  if button and report.strip():
      process_report(report, api_key, test=False)

  if st.session_state["structured_report"]:
      st.markdown("## Please review the structured report below")
      structured_report = st.session_state["structured_report"]
      view_option = st.radio("View structured report as", ("JSON", "Table"), horizontal=True)
      if view_option == "JSON":
          st.json(structured_report)
          pretty_json = json.dumps(structured_report, indent=2)
          # Create a download button and the download functionality
          st.download_button(
              label="Download JSON", 
              data=pretty_json, 
              file_name="structured_report.json", 
              mime="application/json"
          )
      elif view_option == "Table":
          try:
              table = json_to_table(structured_report)
              st.dataframe(table)

              # Convert the DataFrame to CSV
              csv = table.to_csv(index=True)

              # Create a download button for the CSV data
              st.download_button(
                  label="Download data as CSV",
                  data=csv,
                  file_name='structured_report.csv',
                  mime='text/csv',
              )
          except Exception as e:
              st.error("Error with converting json report to table." + str(e) + "\n Here's the report in json: ")
              st.json(structured_report)
      elif view_option == "List":
          pass

if __name__ == "__main__":
    main()