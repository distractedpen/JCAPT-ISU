###############################
# Imports
###############################
import json, subprocess, os
from flask import Flask, request, url_for, make_response
from flask_cors import CORS, cross_origin
from srparser import WavParser


###############################
# Env Setup
###############################
os.chdir("../..")
base_path = os.getcwd()
list_pathname = os.path.join(os.getcwd(), "service/text")
audio_pathname = os.path.join(os.getcwd(), "service/audio")
log_pathname = os.path.join(os.getcwd(), "service/logs")
model_pathname = os.path.join(os.getcwd(), "service/model")

env = {
    "LIST_DIR": list_pathname,
    "AUDIO_DIR": audio_pathname,
    "LOG_DIR": log_pathname,
    "MODEL_DIR": model_pathname,
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

MISMATCH_SCORE = -1
INDEL_SCORE = -1
MATCH_SCORE = 1


def print_dp_table(table, result, correct, R, C):

    for i in range(C+1):
        if i == 0:
            print('　'*7, end=' ')
        else:
            print(f"{correct[i-1]:3s}", end='　')
    print()

    for j in range(R+1):
        for i in range(C+1):
            if j == 0:
                if i == 0:
                    print(' '*4, end='　')
                print(f"{table[j][i]:4d}", end='　')
            elif i == 0 and j <= len(result):
                print(f"{result[j-1]:3s}", end='　')
                print(f"{table[j][i]:4d}", end='　')
            else:
                print(f"{table[j][i]:4d}", end='　')
        print()


def print_align_table(table, result, correct, R, C):

    for i in range(C+1):
        if i == 0:
            print('　'*5, end=' ')
        else:
            print(f"{correct[i-1]:3s}", end='　')
    print()

    for j in range(R+1):
        for i in range(C+1):
            if j == 0:
                if i == 0:
                    print(' '*4, end='　')
                print(f"{table[j][i]:4s}", end='　')
            elif i == 0 and j <= len(result):
                print(f"{result[j-1]:3s}", end='　')
                print(f"{table[j][i]:4s}", end='　')
            else:
                print(f"{table[j][i]:4s}", end='　')
        print()

def print_str_align(str_alignments):
    print(str_alignments['correct'])
    for i in range(len(str_alignments['correct'])):
        if str_alignments['correct'] == str_alignments['result']:
            print("｜", end='')
        else:
            print("　", end='')
    print()
    print(str_alignments['result'])


def make_dp_table(result, correct, R, C):

    value_table = [[0]*(C+1) for _ in range(R+1)]
    align_table = [[' ']*(C+1) for _ in range(R+1)]
    
    for j in range(C+1):
        value_table[0][j] = -j
    for i in range(R+1):
        value_table[i][0] = -i

    for i in range(1, R+1):  # rows
        for j in range(1, C+1): # columns
            if correct[j-1] == result[i-1]: # correct
                value_table[i][j] = value_table[i-1][j-1] + MATCH_SCORE
                align_table[i][j] = '\\'
            elif value_table[i][j-1] > value_table[i][j]: # indel from top
                value_table[i][j] = value_table[i][j-1] + INDEL_SCORE
                align_table[i][j] = '|'
            else: # table[i-1][j-1] > table[i][j-1]: # mismatch
                value_table[i][j] = value_table[i-1][j-1] + MISMATCH_SCORE
                align_table[i][j] = '\\'
    return {'value': value_table, 'alignment': align_table}


def determine_alignment(table, result, correct, i, j):

    res_align = ''
    cor_align = ''
    align_str = ''

    while i > 0 and j > 0:
        if i > 0 and j > 0 and result[i-1] == correct[j-1]:
            res_align = result[i-1] + res_align
            cor_align = correct[j-1] + cor_align
            align_str = "+" + align_str
            i -= 1
            j -= 1
        elif i > 0 and j > 0 and table[i][j] == table[i-1][j-1] + MISMATCH_SCORE:
            res_align = result[i-1] + res_align
            cor_align = correct[j-1] + cor_align
            align_str = "-" + align_str
            i -= 1
            j -= 1
        else:
            res_align = '＿' + res_align
            cor_align = correct[j-1] + cor_align
            align_str = "-" + align_str
            j -= 1

    return {"result": list(res_align), "correct": list(cor_align), "align_str": list(align_str)}

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

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Headers", "*")
    response.headers.add("Access-Control-Allow-Methods", "*")
    return response



##############################
# App Routes (End Points)
##############################


@app.route("/")
def index():
    return url_for("/status")

@app.route("/status", methods=["GET", "POST"])
def status():
    if request.method == "POST":
        return {"status": "online", "method": "POST"}
    return {"status": "online", "method": "GET"}


@app.route("/results", methods=["POST", "GET", "OPTIONS"])
def test():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
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

@app.route("/getText", methods=["POST", "OPTIONS"])
def get_sentence_list():
    global current_sentence
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    if request.method == "POST":
        data = json.loads(request.data)
        print(data)
        ind = data["sent_index"]
        current_sentence = ind
        if ind == len(sent_list)-1:
            return {"page": "list", "sentence": sent_list[ind], "endOfList": True}
        return {"page": "list", "sentence": sent_list[ind], "endOfList": False}
    return {"page": "list", "status": "error"}


@app.route("/getAudio", methods=["POST", "GET", "OPTIONS"])
def get_sentence_audio():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()

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
app.run("0.0.0.0", port=8000)
