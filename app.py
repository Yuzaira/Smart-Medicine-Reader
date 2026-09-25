import cv2
import easyocr
import pyttsx3
import requests

# SETUP TOOLS & ENGINE NODES
speaker = pyttsx3.init()
rate = speaker.getProperty('rate')
speaker.setProperty('rate',145)
reader = easyocr.Reader(['en'])
camera = cv2.VideoCapture(0)

# Structural keywords to isolate print instructions
INSTRUCTION_KEYWORDS = ["take", "dosage", "tablet", "capsule", "mg", "avoid", "daily", "every", "warning"]

print("=== Smart Medicine Cabinet Reader Ready ===")
print("1. Hold your medicine bottle steady in front of the camera.")
print("2. Press 'SPACEBAR' on your keyboard to scan the label and fetch descriptions.")
print("3. Press 'ESC' on the webcam screen to close the app safely.")

# THE CLOUD DATABASE LAYER (openFDA API)

def fetch_medicine_description(drug_name):
    """Queries the openFDA API endpoints for drug descriptions."""
    query_name = drug_name.strip().lower()
    url = f"https://fda.gov:{query_name}&limit=1"
    
    try:
        response = requests.get(url, timeout=3).json()
        if "results" in response:
            label_data = response["results"][0]  
            
            description = ""
            if "indications_and_usage" in label_data:
                description = label_data["indications_and_usage"]
            elif "purpose" in label_data:
                description = label_data["purpose"]
                
            if description:
                sentences = str(description).split('.')
                return ". ".join(sentences[:2]) + "."
    except Exception:
        pass
    return None

try:
    while True:  
        ret, frame = camera.read() 
        if not ret:
            print("[Camera Error] Failed to stream frames.")
            break


        cv2.imshow("Smart Medicine Reader (Press SPACEBAR to Scan)", frame)
        key = cv2.waitKey(10)
        

        if key == 27:
            break
            

        elif key == 32:
            print("\n[Action] Snapshot captured! Processing with AI Engine...")
            
       
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            

            raw_text_list = reader.readtext(gray, detail=0)
            print(f"\n[OCR Result]: {raw_text_list}")

          
            local_instructions = [word for word in raw_text_list if any(k in word.lower() for k in INSTRUCTION_KEYWORDS)]
            

            fda_description = None
            detected_name = ""
            for word in raw_text_list:
                if len(word) > 4 and word.isalpha():
                    print(f"Searching database for matched phrase: '{word}'...")
                    description = fetch_medicine_description(word)
                    if description:
                        fda_description = description
                        detected_name = word
                        break


            master_voice_message = "Scanning complete. "
            
            if fda_description:
                master_voice_message += f"Identified {detected_name}. Used for: {fda_description} "
                print(f"[FDA Database Match]: {fda_description}")
            
            if local_instructions:
                clean_instructions = ' '.join(local_instructions)
                master_voice_message += f"Label instructions say: {clean_instructions}"
                print(f"[Extracted Instructions]: {clean_instructions}")

            if not fda_description and not local_instructions:
                master_voice_message = "Could not read text fields clearly. Please adjust lighting and try again."
                print("[System Alert] No matching medical terms or instructions text seen.")

            master_voice_message = master_voice_message.replace("[", "").replace("]", "").replace("_", " ")
            master_voice_message = str(master_voice_message).encode('ascii', 'ignore').decode('ascii')
            
            print(f"[Audio Status] Speaking complete phrase...")
            speaker.say(master_voice_message)
            speaker.runAndWait()
finally:
    camera.release()
    cv2.destroyAllWindows()
    speaker.stop()
