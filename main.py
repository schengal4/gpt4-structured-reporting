import streamlit as st
from gpt import GPTStructuredReporting

@st.cache_data
def process_radiology_report(report, api_key):
    # Initialize the GPTStructuredReporting class with the API key and template path.
    gpt = GPTStructuredReporting(api_key, "static/report_templates.json")
    # Process the report and capture the structured result.
    structured_report = gpt(report)
    return structured_report

# Set up the title and instructions for the Streamlit app interface.
st.title('Radiology Report Structuring Tool')
st.markdown('## Please enter the radiology report below')
api_key = "Secret"

# Create a text area in the UI for the user to input or paste the radiology report.
report = st.text_area("Report")

# The submit button for processing the report.
button = st.button("Submit")

# Stop the app if the report is empty (no input from the user).
if report.strip() == "":
    st.stop()
# When the user clicks the 'Submit' button, process the report.
if button:
     # Check if the report is not empty before processing.
    if report.strip():  # Check if the report is not empty
        with st.spinner('Processing...'):
            # Process the report and capture the structured result.
            structured_report = process_radiology_report(report, api_key)
            # Indicate successful structuring and display the structured report in JSON format.
            st.json(structured_report)

    expected = {
  "INDICATION": "Male patient presenting with abdominal pain and unexplained weight loss.",
  "COMPARISON": "No prior exam for comparison.",
  "TECHNIQUE": "Axial CT images of the abdomen and pelvis were obtained after administering oral contrast material.",
  "FINDINGS": {
    "LIVER_AND_BILIARY_SYSTEM": "The liver appears normal in size and attenuation, with no focal lesions or biliary ductal dilatation detected. The gallbladder contains multiple gallstones, but there are no signs of cholecystitis or wall thickening.",
    "SPLEEN": "The spleen is unremarkable, showing no evidence of masses, inflammation, or abnormalities.",
    "PANCREAS": "The pancreas is unremarkable, showing no evidence of masses, inflammation, or abnormalities.",
    "ADRENAL_GLANDS": "The adrenal glands are unremarkable, showing no evidence of masses, inflammation, or abnormalities.",
    "KIDNEYS,_URETERS,_AND_BLADDER": "Both kidneys are within normal limits in terms of size and configuration. No renal or ureteral stones are present, and there is no hydroureter or hydronephrosis. The bladder appears unremarkable, with no intrinsic or extrinsic masses.",
    "BOWEL": "Diverticulosis is observed in the sigmoid colon, but no signs of acute diverticulitis are present. No bowel obstruction or significant bowel wall thickening is detected.",
    "APPENDIX": "The appendix is not visualized, and there is no periappendiceal fat stranding.",
    "PERITONEAL_CAVITY": "No abdominal ascites or lymphadenopathy is identified in the peritoneal cavity.",
    "PROSTATE_AND_SEMINAL_GLANDS_(IF_PRESENT)": "The prostate gland is grossly unremarkable.",
    "VASCULATURE": "Normal.",
    "LYMPH_NODES": "No lymphadenopathy is observed."
  },
  "IMPRESSION": "Multiple gallstones without signs of acute cholecystitis. Diverticulosis in the sigmoid colon without acute diverticulitis. Moderate-sized, reducible umbilical hernia. Mild degenerative changes in the lumbar spine."
}