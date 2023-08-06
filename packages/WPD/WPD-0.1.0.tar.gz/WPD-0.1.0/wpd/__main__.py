import json
import os
import sys
from io import BytesIO

import weasyprint as wp

version = (
    open(os.path.join(os.path.dirname(__file__), "VERSION")).read().strip()
)


def run(input, output):
    jobid = None
    output.write(
        json.dumps({"wpd": "wpd", "version": version, "protocol": "1"}).encode(
            "utf-8"
        )
    )
    output.write(b"\n")
    output.flush()
    try:
        while True:
            line = input.readline()
            if not line:
                return
            meta = json.loads(line.rstrip(b"\n").decode("utf-8"))
            jobid = meta["id"]
            if "action" in meta:
                continue
            css_str = meta.get("css")
            size = meta["size"]
            content = input.read(size)
            assert input.read(1) == b"\n"
            css = []
            if css_str:
                css.append(wp.CSS(string=css_str))
            html = wp.HTML(string=content.decode("utf-8"))
            pdf = BytesIO()
            html.write_pdf(pdf, stylesheets=css)
            pdf = pdf.getvalue()
            output.write(
                json.dumps({"id": jobid, "size": len(pdf)}).encode("utf-8")
            )
            output.write(b"\n")
            output.write(pdf)
            output.write(b"\n")
            output.flush()
    except Exception as e:
        import traceback

        sys.stderr.write(traceback.format_exc())
        output.write(
            json.dumps({"id": jobid, "error": str(e)}).encode("utf-8")
        )
        output.write(b"\n")


def main():
    run(sys.stdin.buffer, sys.stdout.buffer)
