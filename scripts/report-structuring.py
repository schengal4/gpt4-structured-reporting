import sys

sys.path.append("..")

import json
import os
from copy import deepcopy

from tqdm.autonotebook import tqdm

from gpt import GPTStructuredReporting

with open("../reports/structured_reports.json", "r") as file:
    json_string = file.read()
data = json.loads(json_string)


model = GPTStructuredReporting(
    api_key="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",
    path_to_templates="../static/report_templates.json",
    model="gpt-4",
)

for category, reports in tqdm(data.items()):
    for report_num, report in tqdm(reports.items()):
        report = data[category][report_num]
        if report["structured"] == "":
            structured = model(report["free_text"])
            data[category][report_num]["structured"] = structured
            print(structured)
        with open(f"../reports/structured_reports_test.json", "w+") as f:
            f.write(json.dumps(data))
