from vosk import Model, KaldiRecognizer, SetLogLevel
import sys, os, wave


class WavParser():

    def __init__(self, model):
        self.model = Model(model)


    def analyze(self, wavefile):
        wf = wave.open(wavefile, 'rb')
        if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
            return "Audio file must be WAV format mono PCM."

        rec = KaldiRecognizer(self.model, wf.getframerate())
        rec.SetWords(True)


        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if rec.AcceptWaveform(data):
                print(rec.Result())
                pass
            else:
                #print(rec.PartialResult())
                pass

        return rec.FinalResult()
