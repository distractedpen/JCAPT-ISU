###############################
# Imports
###############################
from flask import Flask, request, url_for
from flask_cors import CORS, cross_origin
from srparser import WavParser
import json, subprocess, os


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
}

print(env)



################################
# Flask & Vosk Init
################################

app = Flask(__name__)
cors = CORS(app)
app.config['CORS-HEADERS'] = 'Content-Type'

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

def compare_results(resultText):
    global current_sentence
    # compare spoken result with the actual sentence.
    # compare character by character.
    # assuming we go through list in order, with no change.

    # remove spaces from resultText
    resultText = resultText.replace(" ", "")

    correct_answer = sent_list[current_sentence]
    starting_char = correct_answer[0]
    correct_chars = [0 for i in range(len(correct_answer))]
    print(correct_answer, starting_char, correct_chars)
    start_compare = False
    start_index = 0
    for index, char in enumerate(resultText):
        print(char, index)

        print(f"{char} == {starting_char} ? {char == starting_char}")
        if not start_compare and char == starting_char:
            start_compare = True
            start_index = index

        if not start_compare:
            continue

        if char == correct_answer[index - start_index]:
            correct_chars[index-start_index] = 1 

    if sum(correct_chars) == len(correct_answer):
        current_sentence += 1

    return list(resultText), list(correct_answer), correct_chars


##############################
# App Routes (End Points)
##############################

@app.route("/")
def index():
    return url_for("/results")


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
        
        listResultText, listCorrectAnswer, listIsCharCorrect = compare_results(result["text"])

        if result:
            print(audio_pathname)
            os.remove(os.path.join(audio_pathname, "audio_file.ogg"))
            os.remove(os.path.join(audio_pathname, "audio_file.wav"))
            return {
                "page": "test",
                "status": "POST success", 
                "result": 
                    {
                        "listResultText": listResultText,
                        "listCorrectAnswer": listCorrectAnswer,
                        "listIsCharCorrect": listIsCharCorrect
                    }
                }

    return {"page": "test", "status": "online", "result": "Error"}

@app.route("/getText", methods=["POST"])
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
