import re
import docx
from flask import Flask, jsonify, request,render_template
from happytransformer import HappyGeneration, GENSettings

app = Flask(__name__,template_folder='Tamplate')

happy_gen = HappyGeneration("GPT-NEO", "EleutherAI/gpt-neo-1.3B")

training_cases = """Keywords:Upload commands/algorithms from wireless devices304,FIGURE 10,Received commands from outside computer via telemetry?304a,Select algorithm command?304b,Download algorithm command?304c,Check hardware status command?304d,Activate new algorithm 304e,Download new algorithm / set “recently recorded” (srw) buffer size304f,Report battery status and available buffer size304G
Output:As shown in FIG 1, the present invention Secure Storage for Dispensing of Opioids (SSDO) 100. The general shape of the SSDO is generally circular and includes a round primary medication tray 103 and similarly rounded secondary medication tray 104 both has parallel rounded cover 101 and 102 respectively. They both also have A Primary Tray Medication Compartment 128 and a Secondary tray medication compartment 129. This houses the medication until it is dispensed. The Secondary cover however may or may not have a port for microphone 126 and speaker 127 which is recessed on the top cover it also houses a Secondary tray cover locking harness 153 and a dual tray cover interconnected locking shaft which is used to lock the device, preventing unauthorized access and tampering. The Dispenser has a display unit 105 used as a graphics user interface for the various functions of the pill dispenser and can house a mobile computing device and an Avatar 106. The computing device can be embedded into the current setup and maybe a separate detachable unit. It can have a set of legs one in the back and the other in the front 107. The Pill dispenser can be charged through charging contacts 125, this is also the part that makes connection to the docking station.
### 
Keywords:Process detected abnormalities303,FIGURE 9,Is “abnormalities detected” flag set?  303a,Get buffer size for recently recorded data (SRW) as was last inputted via user interface device or via telemetry from outside computing device)303b,Transfer recently recorded ECG data prior to abnormal event to outside computing device via telemetry303c
Output:As illustrated in the Process Detected Abnormalities task diagram 303, which is illustrated in FIG. 9, there is shown the software task that checks the status of the above mentioned "abnormalities-detected" software flag 303a, and in the event this flag is set, then the size of the recently recorded ECG data leading to the abnormal event 303b which is stored in the SRW buffer 74 is sent 303c to an outside mobile device 15 via wireless transceivers 60. The size as determined by 303b, of the SRW 74 buffers, which represents the amount of data prior to the abnormal event being transferred, is programmable via the outside wireless device 15 as well as via the user interface device module 80 of the ECG device 10.  In other words, the size is both the length of time that is recorded and also the size of the memory space required to store this data.  The larger memory space available, the longer the period of time that can be recorded.
###
Keywords:Referring to FIG. 4,software flow diagram,RFID authorization process,software application 400a,mobile device,paired WSD device 10,telemetry,RFID authorization request 400b,WSD access password 400c,internal memory,second authentication processaccess password,close proximity,RFID authorization granted 400d,mobile device searches 400f,RFID authorization denied 400h,RFID authorization granted 400g
Output:Referring to FIG. 4, there is shown a detail of a software flow diagram 400 for the RFID authorization process. A software application 400a is loaded and activated on the mobile device which is capable of communicating with the paired WSD device 10 via telemetry. Once the mobile device initiates an RFID authorization request 400b, the mobile device internal memory is then searched for a WSD access password 400c. In the event that WSD access password is not discovered in the phones internal memory, indicating no WSD has been paired with the mobile device, RFID authorization is granted 400d without requiring a second authentication process through the use of the WSD. If WSD secure password is discovered in the internal memory of the mobile device, the mobile devices searches for the paired WSD via telemetry 400f. If the paired WSD is not found within close proximity of the mobile device, then RFID authorization is denied 400h.  If the paired WSD is found within close proximity of the mobile device, then RFID authorization is granted 400g
###
Keywords:Referring to FIG. 5,software flow diagram,mobile phone access,mobile device 500a,WSD access password 500b,internal memory,paired WSD device,telemetry 500c,close proximity,access to the mobile device granted 500d,access to the mobile denied 500f,mobile device access granted 500g
Output:Referring to FIG. 5, there is shown a detail of a software flow diagram 500 for the mobile phone access. In the event of access to the mobile device 500a, mobile device internal memory is searched for a WSD access password 500b. If the WSD access password is not discovered in the phones internal memory, indicating no WSD has been paired with the mobile device, access to the mobile device is granted 500d. If WSD access password is discovered in the internal memory of the mobile device, the mobile devices searches for the paired WSD via telemetry 500c. If the paired WSD is not found within close proximity of the mobile device, then access to the mobile is denied 500f.  If the paired WSD is found within close proximity of the mobile device, then mobile device access is granted 500g.
###"""

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/generate", methods=["POST"])
def generate_text():
  file = request.files['fileInput']

#extract keyword data from the file
  def extract_data(file):
    doc = docx.Document(file.name)
    keywords = []
    tag_value = ""
    description = ""
    for para in doc.paragraphs:
        text = para.text
        if "TAG:" in text:
            tag_value = text.split(":")[1].strip()
        if "Description:" in text:
            description = text.split(":")[1].strip()
            keywords.append({"tag_value": tag_value, "description": description})
    return [d['description'] + d['tag_value'] for d in keywords]
    print(keywords)

    #Creating the prompt
    def create_prompt(training_cases, keywords):
        keywords = ", ".join(keywords)
        prompt = training_cases + "\nKeywords: "+ keywords+ "\nOutput:"
        return prompt
    prompt = create_prompt(training_cases, keywords)

    # Generate text using the HappyGeneration model
    args_beam = GENSettings(num_beams=5, no_repeat_ngram_size=2, early_stopping=True, min_length=5, max_length=150)
    # Generate text using the HappyGeneration model
    output_text= happy_gen.generate_text(prompt, args=args_beam)

    # Return the generated text as a JSON response
    print("output_text:", output_text)
    return jsonify({"output_text": output_text.text})

if __name__ == '__main__':
  app.run()