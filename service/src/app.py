###############################
# Imports
###############################
import sys, json, subprocess, os, time, signal
from flask import Flask, request, make_response
from flask_cors import CORS, cross_origin
from srparser import WavParser
from DrillSetHandler import DrillSetHandler
from NWAlignment import print_dp_table, print_align_table, print_str_align, make_dp_table, determine_alignment


###############################
# Env Setup
###############################
os.chdir("../..")
base_path = os.getcwd()
drill_pathname = os.path.join(os.getcwd(), "service/drills")
log_pathname = os.path.join(os.getcwd(), "service/logs")
model_pathname = os.path.join(os.getcwd(), "service/model")
ssl_pathname = os.path.join(os.getenv("HOME"), "ssl_certs")

env = {
    "DRILL_DIR": drill_pathname,
    "AUDIO_DIR": os.path.join(drill_pathname, "audio"),
    "RECORDING_DIR": os.path.join(drill_pathname, "audio/recordings"),
    "LOG_DIR": log_pathname,
    "MODEL_DIR": model_pathname,
    "SSL_DIR": ssl_pathname,
    "DEBUG": False
}

print(env)


################################
# Flask, Vosk, Drill Data Init
################################

app = Flask(__name__)
cors = CORS(app, resources=r'/.*',
    origins="*", methods="*", allow_headers="*", headers='Content-Type')
wav_parser = WavParser(env["MODEL_DIR"])

file_name_padding = 0
drill_data_handler = DrillSetHandler(env["DRILL_DIR"] + "/drills.json")
sent_list = drill_data_handler.get_drill_set("dev_test")["sentences"]
print(sent_list)
current_sentence = 0

###############################
#  Helper Functions
###############################

def recording_cleanup_handler(sig, frame):
    print("Cleaning Recordings directory...")
    for file in os.scandir(env["RECORDING_DIR"]):
        os.remove(file)
    sys.exit(0)

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
                 os.path.join(env["RECORDING_DIR"], file_name+".wav")],
                 stdout=subprocess.PIPE, stderr=fd)

        result = wav_parser.analyze(os.path.join(env["RECORDING_DIR"], file_name+".wav"))
        result = json.loads(result)
        str_alignment = compare_results(result["text"])

        if result:
            return { "status": "success", "result": str_alignment}
        return {"status": "failure", "result": ""}

@app.route("/getDrillSets", methods=["GET", "POST"])
@cross_origin
def get_drill_sets():
    pass


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

        with open(os.path.join(env["AUDIO_DIR"]+"/dev_test", f"sent{ind}.mp3"), 'rb') as fd:
            audio_data = fd.read()

        return make_response((audio_data, {"Content-Type": "audio/mpeg"}))


##############################
# Start App
##############################
signal.signal(signal.SIGINT, recording_cleanup_handler)
app.run("0.0.0.0", port=8000, ssl_context=(env["SSL_DIR"]+"/server.crt", env["SSL_DIR"]+"/server.key"))
