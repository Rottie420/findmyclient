import uuid
from concurrent.futures import ThreadPoolExecutor
from flask import Blueprint, jsonify, render_template, request
from modules.scraper.engine import run_scraper


main_bp = Blueprint("main", __name__)
executor = ThreadPoolExecutor(max_workers=20)
jobs = {}


# ---------- Index ----------
@main_bp.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@main_bp.route("/search", methods=["POST"])
def search():

    query = request.form.get("query")

    if not query:
        return jsonify({
            "error": "Missing query"
        }), 400

    job_id = str(uuid.uuid4())

    jobs[job_id] = {
        "status": "processing",
        "result": None,
    }

    future = executor.submit(run_scraper, query)

    def callback(f):
        try:
            jobs[job_id]["result"] = f.result()
            jobs[job_id]["status"] = "completed"
        except Exception as e:
            jobs[job_id]["status"] = "failed"
            jobs[job_id]["result"] = str(e)

    future.add_done_callback(callback)

    return jsonify({
        "job_id": job_id
    })


# ---------- Get Result ----------
@main_bp.route("/result/<job_id>", methods=["GET"])
def result(job_id):

    job = jobs.get(job_id)

    if not job:
        return jsonify({
            "error": "Job not found"
        }), 404

    return jsonify(job)