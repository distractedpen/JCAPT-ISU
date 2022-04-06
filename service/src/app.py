###############################
# Imports
###############################
import json, subprocess, os
from flask import Flask, request, make_response, render_template
from flask_cors import CORS, cross_origin
from srparser import WavParser
from NWAlignment import print_dp_table, print_align_table, print_str_align, make_dp_table, determine_alignment


###############################
# Env Setup
###############################
os.chdir("../..")
base_path = os.getcwd()
list_pathname = os.path.join(os.getcwd(), "service/text")
audio_pathname = os.path.join(os.getcwd(), "service/audio")
log_pathname = os.path.join(os.getcwd(), "service/logs")
model_pathname = os.path.join(os.getcwd(), "service/model")
ssl_pathname = os.path.join(os.getenv("HOME"), "ssl_certs")

env = {
    "LIST_DIR": list_pathname,
    "AUDIO_DIR": audio_pathname,
    "LOG_DIR": log_pathname,
    "MODEL_DIR": model_pathname,
    "SSL_DIR": ssl_pathname,
    "DEBUG": False
}

print(env)


################################
# Flask & Vosk Init
################################

app = Flask(__name__)
cors = CORS(app, resources=r'/.*',
    origins="*", methods="*", allow_headers="*", headers='Content-Type')
wav_parser = WavParser(env["MODEL_DIR"])

# set up sentence list
current_sentence = 0
sent_list = []
with open(os.path.join(env["LIST_DIR"], "list.txt"), "r") as fd:
    for line in fd:
        line = line.strip("\n")
        line = line.replace("。", "")
        sent_list.append(line)


###############################
#  Helper Functions
###############################

def compare_results(result_text):
    #
    # Dynamic Programming:
    #   Align Correct Text to Vosk Output
    # Correct:    私は大_学生です
    # Ex Output:  私は＿医学＿です
    # Alignment:  ＋＋ーーーー＋＋


    # remove spaces from resultText
    result = result_text.replace(" ", "")
    correct = sent_list[current_sentence]

    R = len(result)
    C = len(correct)

    tables = make_dp_table(result, correct, R, C)

    str_alignments = determine_alignment(tables['value'], result, correct, R, C)

    if env["DEBUG"]:
        print("*"*36)
        print_dp_table(tables['value'], result, correct, R, C)
        print("*"*36)
        print_align_table(tables['alignment'], result, correct, R, C)
        print("*"*36)
        print_str_align(str_alignments)
        print("*"*36)

    return str_alignments

##############################
# App Routes (End Points)
##############################

@app.route("/")
@cross_origin()
def index():
    global current_sentence

    return render_template("index.html")

@app.route("/status", methods=["GET", "POST"])
@cross_origin()
def status():
    if request.method == "POST":
        return {"status": "online", "method": "POST"}
    return {"status": "online", "method": "GET"}


@app.route("/results", methods=["POST", "GET"])
@cross_origin()
def test():

    if request.method == "POST":

        audio_data = request.data

        with open(os.path.join(env["AUDIO_DIR"], "audio_file.ogg"), "wb") as fd:
            fd.write(audio_data)

        # convert data from ogg to wav using a subprocess
        with open(os.path.join(log_pathname, "convert.log"), "w") as fd:
            subprocess.run(
                ["ffmpeg",
                 "-i", os.path.join(env["AUDIO_DIR"], "audio_file.ogg"),
                 "-ar", "48000", "-ac", "1",
                 os.path.join(audio_pathname, "audio_file.wav")],
                 stdout=subprocess.PIPE, stderr=fd)

        result = wav_parser.analyze(os.path.join(env["AUDIO_DIR"], "audio_file.wav"))
        result = json.loads(result)
        print(result)
        str_alignment = compare_results(result["text"])

        if result:
            print(audio_pathname)
            os.remove(os.path.join(audio_pathname, "audio_file.ogg"))
            os.remove(os.path.join(audio_pathname, "audio_file.wav"))
            return {
                "page": "test",
                "status": "POST success",
                "result": str_alignment
                }

    return {"page": "test", "status": "online", "result": "Error"}

@app.route("/getText", methods=["POST"])
@cross_origin()
def get_sentence_list():
    global current_sentence

    if request.method == "POST":
        data = json.loads(request.data)
        print(data)
        ind = data["sent_index"]
        current_sentence = ind
        if ind == len(sent_list)-1:
            return {"page": "list", "sentence": sent_list[ind], "endOfList": True}
        return {"page": "list", "sentence": sent_list[ind], "endOfList": False}
    return {"page": "list", "status": "error"}


@app.route("/getAudio", methods=["POST"])
@cross_origin()
def get_sentence_audio():

    if request.method == "POST":
        data = json.loads(request.data)
        ind = data["audiofileIndex"]

        with open(os.path.join(audio_pathname, "test", f"sent{ind}.mp3"), 'rb') as fd:
            audio_data = fd.read()

        return make_response((audio_data, {"Content-Type": "audio/mpeg"}))

    return {"status": "getAudio is working."}


##############################
# Start App
##############################
app.run("0.0.0.0", port=8000, ssl_context=(env["SSL_DIR"]+"/server.crt", env["SSL_DIR"]+"/server.key"))
