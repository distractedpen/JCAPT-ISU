###############################
# Imports
###############################
import sys, json, subprocess, os, time, signal
import uuid
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

###############################
#  Helper Functions
###############################

def recording_cleanup_handler(sig, frame):
    print("Cleaning Recordings directory...")
    for file in os.scandir(env["RECORDING_DIR"]):
        os.remove(file)
    sys.exit(0)

def compare_results(result, correct):
    #
    # Dynamic Programming:
    #   Align Correct Text to Vosk Output
    # Correct:    私は大_学生です
    # Ex Output:  私は＿医学＿です
    # Alignment:  ＋＋ーーーー＋＋


    # remove spaces from resultText
    result = result.replace(" ", "")
    
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

        id = request.form["id"]
        index = int(request.form["index"])

        audio_data = request.files['audio']
        file_name = str(int(time.time())) + str(file_name_padding).zfill(4)
        file_name_padding = ( file_name_padding + 1 ) % 9999 # 0000
        audio_data.save(os.path.join(env["RECORDING_DIR"], file_name+".ogg"))


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

        correct = drill_data_handler.get_sentence(id, index)

        str_alignment = compare_results(result["text"], correct)

        

        if result:
            return { "status": "success", "result": str_alignment}
        return {"status": "failure", "result": ""}

@app.route("/getDrillSets", methods=["GET", "POST"])
@cross_origin()
def get_drill_sets():
    drill_sets = drill_data_handler.get_drill_sets()
    return {"drill_sets": drill_sets}

@app.route("/getDrillSet", methods=["POST"])
@cross_origin()
def get_drill_set():
    req_data = json.loads(request.data)
    drill_set_id = req_data["drill_set_id"]
    drill_set_data = drill_data_handler.get_drill_set(drill_set_id) 
    return {"drillSet": drill_set_data}


@app.route("/getAudio", methods=["POST"])
@cross_origin()
def get_sentence_audio():

    if request.method == "POST":
        data = json.loads(request.data)
        drill_set_id = data["drillSetId"]
        file_name = data["fileName"]

        with open(os.path.join(env["AUDIO_DIR"], drill_set_id, file_name), 'rb') as fd:
            audio_data = fd.read()

        return make_response((audio_data, {"Content-Type": "audio/mpeg"}))

@app.route("/newDrillSet", methods=["POST"])
@cross_origin()
def new_drill_set():
    
    id = str(uuid.uuid4())
    new_audio_dir = os.path.join(env["AUDIO_DIR"], id)
    num_sentences = int(request.form["num_sentences"])
    name = request.form["name"]
    sentences = [ request.form["sentence"+str(i)] for i in range(num_sentences)]
    audio = [ key + ".wav" for key in request.files.keys()]
    
    # Create new Drill Set
    new_drill_set = {"name": name, "sentences": sentences, "audio": audio}
    drill_data_handler.add_drill_set(id, new_drill_set)
    
    # Save Audio to Correct directory
    os.mkdir(new_audio_dir)
    
    for filename in audio:
        audio_data = request.files[filename[:-4]]
        audio_data.save(os.path.join(new_audio_dir, filename))
    
    return {"status": "success"}


@app.route("/deleteDrillSet", methods=["POST"])
@cross_origin()
def delete_drill_set():
    
    data = json.loads(request.data)
    id = data["drillSetId"]

    drill_data_handler.remove_drill_set(id)

    return {"status": "success"}

@app.route("/updateDrillSet", methods=["POST"])
@cross_origin()
def update_drill_set():
    
    id = request.form["drillSetId"]
    audio_dir = os.path.join(env["AUDIO_DIR"], id)
    num_sentences = int(request.form["num_sentences"])
    name = request.form["name"]
    sentences = [ request.form["sentence"+str(i)] for i in range(num_sentences)]
    audio = [ key + ".wav" for key in request.files.keys()]
    print(audio)
    # Create new Drill Set
    new_drill_set = {"name": name, "sentences": sentences, "audio": audio}
    drill_data_handler.update_drill_set(id, new_drill_set)
    
    # Save Audio to Correct directory
    for filename in audio:
        pathname = os.path.join(audio_dir, filename)
        os.remove(pathname)
        audio_data = request.files[filename[:-4]]
        audio_data.save(pathname)
    
    return {"status": "success"}


##############################
# Start App
##############################
signal.signal(signal.SIGINT, recording_cleanup_handler)
# app.run("0.0.0.0", port=8000, ssl_context=(env["SSL_DIR"]+"/server.crt", env["SSL_DIR"]+"/server.key"))
