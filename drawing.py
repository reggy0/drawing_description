import re
import docx
from flask import Flask, jsonify, request,render_template
from happytransformer import HappyGeneration, GENSettings

app = Flask(__name__,template_folder='Tamplate')

happy_gen = HappyGeneration("GPT-NEO", "EleutherAI/gpt-neo-1.3B")

training_cases = """Keywords:Upload Commands & Algorithms task diagram304,Figure 10,Select Algorithm Command304b,Stored detection algorithms304e,Download Algorithm Command304c,Customized detection algorithms304f,Downloaded algorithm memory unspecified,Hardware Status Command 304d,Activating a New Algorithm 304e,Recently Recorded Buffer Size304f,Reporting Battery Status and Available Buffer Size304g
Output:As illustrated in the Upload Commands & Algorithms task diagram 304, which is illustrated in FIG. 10, there is shown the software task that manages uploading of new algorithms and commands 304a sent from outside wireless devices into the ECG monitor device via wireless transceivers  . The system includes several commands that allow for efficient and effective management of wireless devices and the algorithms they use. Select Algorithm Command 304b selects one of the stored detection algorithms 304e in the ECG device  . Download Algorithm Command 304c can download and store customized detection algorithms 304f from outside computing devices  into the downloaded algorithm memory  in the ECG device . The system also includes a command for checking the hardware status (304d) and activating a new algorithm (304e). Additionally, there is a command for downloading a new algorithm and setting the "recently recorded" (SRW) buffer size (304f). Finally, there is a command for reporting battery status and available buffer size (304g). These commands provide an efficient and effective way to manage wireless devices and the algorithms they use.
### 
Keywords:Process Detected Abnormalities task diagram303,FIG. 9,Abnormalities-detected software flag303a,Recently recorded ECG data,Sent to outside mobile device303c,Wireless transceivers,Programmable size of SRW buffers,User interface device module,Length of time recorded,Larger memory space
Output:As illustrated in the Process Detected Abnormalities task diagram 303, which is illustrated in FIG. 9, there is shown the software task that checks the status of the above mentioned "abnormalities-detected" software flag 303a, and in the event this flag is set, then the size of the recently recorded ECG data leading to the abnormal event 303b which is stored in the SRW buffer  is sent 303c to an outside mobile device via wireless transceivers . The size as determined by 303b, of the SRW buffers, which represents the amount of data prior to the abnormal event being transferred, is programmable via the outside wireless device as well as via the user interface device module of the ECG device.  In other words, the size is both the length of time that is recorded and also the size of the memory space required to store this data.  The larger memory space available, the longer the period of time that can be recorded.
###
Keywords:Smart Personal Emergency Response System (SPERS)100,FIG. 1,Monitoring, analyzing, and communicating behavior,Emergency condision,Non-emergency conditions,Interactive communication unit,Non-transitory computer readable storage medium,Data analytics processor
Output:FIG. 1 exemplarily illustrates a top perspective view of a smart personal emergency response system (SPERS) 100 for monitoring, analyzing, and communicating behavior of a user in emergency conditions and non-emergency conditions to multiple user devices. As used herein, “user” refers to an entity, for example, a baby, an elderly patient, a paralyzed person, etc., that is monitored using the SPERS 100. Also, as used herein, “emergency conditions” refer to conditions that cause severe symptoms in the user and may put the health of the user in serious risk, for example, a heart attack, a sudden fall, fainting, etc. Also, as used herein, “non-emergency conditions” refer to conditions of the user that do not require sudden medical attention, for example, routine activities of the user. The user devices are, for example, a laptop, a smart phone, a tablet, a computer, etc. As used herein, “behavior” refers to different vital parameters and trends in the vital parameters of the user in the emergency conditions and the non-emergency conditions. The SPERS 100 mainly comprises multiple sensors, an interactive communication unit, a non-transitory computer readable storage medium, and at least one data analytics processor. The SPERS 100 is a wearable device by means of a lanyard 105, a clip, etc., and is waterproof.
###
Keywords:Thought Processing Application - Main Block Diagram,FIG. 4,Medical Monitoring Device (MMD),Plurality of electrodes,EEG signals representing brain electrical activity, received and recorded 310,Amplified 121,Digitized utilizing an A/D converter 125,High-pass filter 122 ,Low-pass filter 123,Feature Extraction 141, identifies segments of data within EEG recording that are of interest,Artificial Intelligence (AI)130, accesses historical EEG recording database 320 to optimize Feature Extraction process and decoding 142 process,Historical EEG recording database 320,Decoding 142
Output:Referring now to FIG. 4, there is shown a Thought Processing Application - Main Block Diagram of the present invention, Medical Monitoring Device (MMD), wherein a plurality of electrodes  is placed on the patient's scalp and is connected to the present invention via a series of wires. The EEG signals representing the brain electrical activity thru the electrodes are received and recorded 310. Next, the recorded EEG signals are amplified 121 and digitized utilizing an A/D converter 125. Next, a series of filters are applied to eliminate noise and unrelated frequencies. A high-pass filter 122 is utilized to pass all frequencies above a defined frequency limit and reject all frequencies below that limit, while a low-pass filter 123 is used to pass all frequencies below a defined frequency and reject all frequencies above the said limit. Next, Feature Extraction 141 is performed to identify segments of data within the EEG recording that is of interest. Artificial Intelligence (AI) 130 accesses the historical EEG recording database 320 and optimizes the Feature Extraction process. Next, the decoding 142 process, in conjunction with Artificial Intelligence (AI) 130, accesses the historical EEG recording database 320 to optimize and convert the extracted features into decoded text information.
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
