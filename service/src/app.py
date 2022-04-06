###############################
# Imports
###############################
import json, subprocess, os, time, signal
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
recording_pathname = os.path.join(os.getcwd(), "service/audio/recordings")
example_audio_pathname = os.path.join(os.getcwd(), "service/audio/examples")
log_pathname = os.path.join(os.getcwd(), "service/logs")
model_pathname = os.path.join(os.getcwd(), "service/model")
ssl_pathname = os.path.join(os.getenv("HOME"), "ssl_certs")

env = {
    "LIST_DIR": list_pathname,
    "RECORDING_DIR": recording_pathname,
    "EXAMPLE_AUDIO_DIR": example_audio_pathname,
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
file_name_padding = 0
with open(os.path.join(env["LIST_DIR"], "list.txt"), "r") as fd:
    for line in fd:
        line = line.strip("\n")
        line = line.replace("。", "")
        sent_list.append(line)



###############################
#  Helper Functions
###############################

def recording_cleanup_handler(sig, frame):
    for file in os.scandir(env["RECORDING_DIR"]):
        os.remove(file)

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
    return render_template("index.html")

@app.route("/status", methods=["GET", "POST"])
@cross_origin()
def status():
    if request.method == "POST":
        return {"status": "online", "method": "POST"}
    return {"status": "online", "method": "GET"}


@app.route("/results", methods=["POST"])
@cross_origin()
def test():
    global file_name_padding

    if request.method == "POST":

        audio_data = request.data
        file_name = str(int(time.time())) + str(file_name_padding).zfill(4)
        file_name_padding = ( file_name_padding + 1 ) % 9999 # 0000

        with open(os.path.join(env["RECORDING_DIR"], file_name+".ogg"), "wb") as fd:
            fd.write(audio_data)

        # convert data from ogg to wav using a subprocess
        with open(os.path.join(log_pathname, "convert.log"), "w") as fd:
            subprocess.run(
                ["ffmpeg",
                 "-i", os.path.join(env["RECORDING_DIR"], file_name+".ogg"),
                 "-ar", "48000", "-ac", "1",
                 os.path.join(recording_pathname, file_name+".wav")],
                 stdout=subprocess.PIPE, stderr=fd)

        result = wav_parser.analyze(os.path.join(env["RECORDING_DIR"], file_name+".wav"))
        result = json.loads(result)
        str_alignment = compare_results(result["text"])

        if result:
            return { "status": "success", "result": str_alignment}
        return {"status": "failure", "result": ""}


@app.route("/getText", methods=["POST"])
@cross_origin()
def get_sentence_list():
    global current_sentence

    if request.method == "POST":
        data = json.loads(request.data)
        ind = data["sent_index"]
        current_sentence = ind
        if ind == len(sent_list)-1:
            return {"page": "list", "sentence": sent_list[ind], "endOfList": True}
        return {"page": "list", "sentence": sent_list[ind], "endOfList": False}


@app.route("/getAudio", methods=["POST"])
@cross_origin()
def get_sentence_audio():

    if request.method == "POST":
        data = json.loads(request.data)
        ind = data["audiofileIndex"]

        with open(os.path.join(env["EXAMPLE_AUDIO_DIR"], f"sent{ind}.mp3"), 'rb') as fd:
            audio_data = fd.read()

        return make_response((audio_data, {"Content-Type": "audio/mpeg"}))


##############################
# Start App
##############################
signal.signal(signal.SIGINT, recording_cleanup_handler)
app.run("0.0.0.0", port=8000, ssl_context=(env["SSL_DIR"]+"/server.crt", env["SSL_DIR"]+"/server.key"))
