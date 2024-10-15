import json
import os

import requests as req
from flask import Blueprint, jsonify, request

from .constants import webhook_urls
from .reports import Report
from .tasks import on_board_hco

main = Blueprint("main", __name__)


@main.route("/summarize", methods=["POST"])
def reports():

    # check for data
    if not request.data:
        resp = jsonify({"error": "No payload provided."})
        resp.status_code = 400
        return resp

    # load the request data
    data = json.loads(request.data)

    # make sure the data has array structure
    # to maintain data integrity.
    if not isinstance(data, list):
        resp = jsonify({"error": "Request payload must be an array."})
        resp.status_code = 400
        return resp

    # get the model to use for the summary, default to `llama`
    model = request.args.get("model", "llama")

    report = Report(data)

    # summary
    summary = {
        "medRepId": data[0].get("medRepId"),
        "hcpId": data[0].get("hcpId"),
        "practitionerDetail": data[0].get("practitionerDetail"),
        "summary": report.summarize(model),
    }
    return jsonify(summary)


# @main.route("/reports", methods=["POST"])
# def index():
#     if "file" in request.files:
#         xlsx_file = request.files["file"]
#         file_path = f"./{xlsx_file.filename}"
#         # save for reading
#         xlsx_file.save(file_path)
#         data = read_file(file_path)
#         # clean up
#         os.remove(file_path)

#         return jsonify(data)

#     return jsonify({"error": "No file to read"})


@main.route("/onboard", methods=["POST"])
def on_board():
    data = request.get_json()
    templateUrl = data.get("templateUrl")
    companyId = data.get("companyId")
    managerId = data.get("managerId")
    envWebhooks = data.get("envWebhooks")

    print("-------------------------------------------")
    print(templateUrl, companyId, managerId)

    result = on_board_hco(templateUrl, companyId, managerId)

    # try:
    #     res = req.post(webhook_urls.get(envWebhooks), json=result)
    # except Exception:
    #     print("An error occur")

    print("Result------", result)
    # try:
    return jsonify({"result": "Good"})
    # except Exception:
    #     return jsonify({"error": "No file to read"})
