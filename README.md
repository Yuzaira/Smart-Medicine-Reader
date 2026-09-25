# ==================================Smart Medicine Cabinet Reader============================================================
A lightweight Python app that helps people read medicine bottles using their webcam. When you hold a bottle up and press the Spacebar, the script uses computer vision to find the text, looks up what the medication is used for via the official openFDA web API, and reads the instructions out loud using text-to-speech.

I built this specifically as an accessibility tool to help visually impaired or elderly individuals manage their prescriptions hands-free without reading tiny print labels.

## How it Works
1.**Camera Feed:** Opens a live video window using OpenCV.
2. **Text Scanning:** When you press SPACEBAR, it takes a snapshot and handles high-contrast grayscale formatting so EasyOCR can read the letters off the curved plastic surface.
3. **FDA Database Search:** The script filters out numeric noise and automatically queries the openFDA API using the drug name it found.
4. **Voice Feedback:** It combines the local dosage instructions (like "mg", "tablets", "daily") with the official usage description from the cloud, and reads the entire sentence aloud in a clear, slowed-down voice pace.

## Setup & Installation

Make sure you have your webcam connected and your computer speakers turned on.

1. Clone or download this repository.
2. Open your terminal in the project folder and install the required libraries:

```Bash
pip install -r requirements.txt
```
3.Run the script:
```Bash
python app1.py
```

## How to Test It
* Hold a medicine bottle (like Ibuprofen or Aspirin) steady in front of the lens. Make sure the text is well-lit and facing forward.
* Press the Spacebar on your keyboard.
* The console will log the raw text array it reads, and you will hear your speakers say: "Scanning complete. Identified [Drug]. Used for: [FDA Details]..."
* Press the ESC key on the video window whenever you want to close the app safely.
**Note:** Since this app queries public open-source registries, always verify your treatment amounts against your actual physical printed script label guidelines before taking medications.

## Project Takeaways
* Handled string manipulation filters to split up long, text-heavy FDA data packets into concise 2-sentence user descriptions.
* Solved hidden OS audio buffer clipping issues by implementing a hardware thread execution delay (time.sleep) to prevent the speech engine from dropping sentences early.
* Configured custom speech rate parameters to convert fast, robotic audio streams into natural human-friendly speech paces
