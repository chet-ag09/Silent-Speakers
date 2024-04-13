import tkinter as tk
from tkinter import ttk, PhotoImage, filedialog
import cv2
import mediapipe as mp
from PIL import Image, ImageTk
import customtkinter
import webbrowser
import ttkbootstrap as tb
from ttkbootstrap import Style

# Initializin Mediapipe hands module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)

class SignLanguageApp:
    def __init__(self, root): 
        #(THE UI)
        self.root = root
        self.root.title("Silent Speakers")
        self.photo = PhotoImage(file = "Asset imgs/Logo.png")
        self.root.iconphoto(False, self.photo)
        self.root.configure(bg="#262626")
        self.root.geometry('1000x750')
        self.bg = PhotoImage(file = "Asset imgs/bg_silent.png") 
        self.root.resizable(False, False)

        self.tabControl = tb.Notebook(root, bootstyle="dark")  # Move tab initialization here
        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)
        self.tabControl.pack(expand = 1, fill ="both") 

        style=ttk.Style()
        style.layout("TNotebook", [])
        style.configure("TNotebook", highlightbackground="#848a98",tabmargins=0)


        self.bg_image = Image.open("Asset imgs/dk.png") 
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)

        #TABS
        self.tabControl.add(self.tab1, text='Sign-to-Text Translation')
        self.tabControl.add(self.tab2, text='Text-to-Sign Translation')

    #TAB 1--------------------------------------

        # Create a Label widget and display the background image
        self.bg_label = tk.Label(self.tab1, image=self.bg_photo)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
      
        self.ph1 = Image.open("Asset imgs/space_not.png") 
        self.ph1_photo = ImageTk.PhotoImage(self.ph1)

        self.video_frame = tb.Label(self.tab1, background='#117f52')
        self.video_frame.pack(padx=10, pady=10)

        self.label = tk.Label(self.tab1, image=self.ph1_photo, bg='#383838')
        self.label.pack(pady=2, padx=2)
      
        
        self.sign_value = tk.StringVar()
        self.sign_value.set("Awaiting Sign")
        self.sign_entry = tb.Entry(self.tab1, textvariable=self.sign_value, width=33, font='Arial 20', state="disabled", bootstyle="dark")
        
        self.sign_entry.pack(pady=5)
        
        style = Style()
        style_btn = "MyButton.TButton" 
        style.configure(style_btn, font=("Arial"), background="#00bc8c", borderwidth=0, foreground="#383838")
        style_map = {
    "background": [("hover", "#018f6b")],
    "foreground": [("hover", "white")],
}

        style.map(style_btn, **style_map)

        #Camera Start
        self.start_button = tb.Button(self.tab1, text='Live Camera Feed', command=self.start_detection, width=20, style=style_btn) 
        self.start_button.pack(padx=1, pady=5)

        #Camera Stop
        self.stop_live = tb.Button(self.tab1, text='Stop Camera Feed', command=self.stop_detection, width=20, style=style_btn) 
        self.stop_live.pack(padx=1, pady=5)

        #Open Videos
        self.pre_recorded_video = tb.Button(self.tab1, text='Pre-Recorded Video', command=self.open_video, width=20, style=style_btn) 
        self.pre_recorded_video.pack(padx=1, pady=5)

        self.is_detecting = False

    #TAB2-------------------------------------------------
        # Create a Label widget and display the background image for 2nd tab
        
        self.bg_label2 = tk.Label(self.tab2, image=self.bg_photo)
        self.bg_label2.place(x=0, y=0, relwidth=1, relheight=1)

        self.ph2 = Image.open("Asset imgs/space.jpg") 
        self.ph2_photo = ImageTk.PhotoImage(self.ph2)

        #Show the sign
        self.sign_image_label = tk.Label(self.tab2, text='Translated Image..', bg='#383838', image=self.ph2_photo)
        self.sign_image_label.pack(pady=40, padx=2)
        self.load_asl_images()

        self.text_img_says = tk.Label(self.tab2, text='Please Enter Text to translate.', bg='#282828', font='Arial 20', fg='#f1f1f1')
        self.text_img_says.pack(pady=10)

        #Input area for the text to sign
        self.phrase_entry = tk.Entry(self.tab2, width=33, font='Arial 20')
        self.phrase_entry.pack(pady=5)
        self.phrase_entry.bind("<KeyRelease>", self.show_sign_image)

        
#(The FUNCS)-------------------------------------------------------------------------------------------------------------------
    #SELECTING THE VID WITH SIGN
    def open_video(self):
        self.label.pack_forget()
        video_file_path = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi")])
        if video_file_path:
            self.process_video(video_file_path)


    #PROCESSING THE SELECTED VIDEO
    def process_video(self, video_file_path):
        cap = cv2.VideoCapture(video_file_path)

        while True: 
            ret, frame = cap.read()
            if not ret:
                break

            frame = cv2.resize(frame, (640, 360))  # Resize the frame to 640x360
            frame = self.detect_and_translate(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
            image = ImageTk.PhotoImage(image)

            self.video_frame.config(image=image)
            self.video_frame.image = image

            self.root.update()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    #Finding and Loading the imagw based on the text
    def load_asl_images(self):
        self.asl_images = {}
        for phrase in ['Hello', 'Thank you', 'Angry', 'Love', 'Water']:
            image_path = f"asl_img/{phrase}.png"
            print(f"Loading image for phrase: {phrase}, Path: {image_path}")
            try:
                image = Image.open(image_path)
                self.asl_images[phrase] = image
            except FileNotFoundError:
                print(f"Error: Image file '{image_path}' not found.")

    def show_sign_image(self, event):
        entered_phrase = self.phrase_entry.get().capitalize()
        if entered_phrase in self.asl_images:
            image = self.asl_images[entered_phrase]
            photo = ImageTk.PhotoImage(image)
            self.sign_image_label.config(image=photo)
            self.sign_image_label.image = photo
        else:
            self.sign_image_label.config(image=None)
    
    #DETECT SIGN WHEN TRUE
    def start_detection(self):
        self.is_detecting = True
        self.label.pack_forget()
        self.start_button.configure(command=None)
        self.detect_sign()
    #STOP DETECTING SIGN
    def stop_detection(self):
        self.is_detecting = False
        self.stop_live.configure(command=None)


    
    #MAIN DETECTING SIGN
    def detect_sign(self):
        cap = cv2.VideoCapture(0)
        
        while self.is_detecting:
            ret, frame = cap.read()
            if not ret:
                break
            
            frame = self.detect_and_translate(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(frame)
            image = ImageTk.PhotoImage(image)
            
            self.video_frame.config(image=image)
            self.video_frame.image = image
            
            self.root.update()
        
        cap.release()
        cv2.destroyAllWindows()

    
    def detect_and_translate(self, frame):
        # DETECT HANDS IN THE FRAME
        results = hands.process(frame)
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # CLASSIFY THE HAND GESTURE
                sign = self.classify_hand_gesture(hand_landmarks)
                
                # UPDATE THE DETECTED SIGN
                self.sign_value.set(sign)
        
        return frame
    
    def classify_hand_gesture(self, hand_landmarks):
        # Extract landmarks for specific fingers
        landmarks = hand_landmarks.landmark
        
        
        # Get the y-coordinates of certain landmarks for classification
        index_tip_y = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
        middle_tip_y = landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
        ring_tip_y = landmarks[mp_hands.HandLandmark.RING_FINGER_TIP].y
        pinky_tip_y = landmarks[mp_hands.HandLandmark.PINKY_TIP].y
        thumb_tip_y = landmarks[mp_hands.HandLandmark.THUMB_TIP].y
        wrist_y = landmarks[mp_hands.HandLandmark.WRIST].y
        thumb_base_y = landmarks[mp_hands.HandLandmark.THUMB_MCP].y
        
        
        # Define thresholds for sIGNS
        if index_tip_y > middle_tip_y and middle_tip_y < ring_tip_y and ring_tip_y < pinky_tip_y and thumb_tip_y < wrist_y:
            return 'Hello'
        elif index_tip_y < middle_tip_y and middle_tip_y < ring_tip_y and ring_tip_y < pinky_tip_y and thumb_tip_y < wrist_y:
            return 'Thank you'
        elif index_tip_y < middle_tip_y and middle_tip_y > ring_tip_y and ring_tip_y > pinky_tip_y and thumb_tip_y < wrist_y:
            return 'I Love You'
        elif thumb_tip_y < index_tip_y:
            return 'Yes'
        elif index_tip_y > middle_tip_y and thumb_tip_y < wrist_y:
            return 'No'
        elif index_tip_y < wrist_y and middle_tip_y < wrist_y and ring_tip_y < wrist_y and pinky_tip_y < wrist_y:
         #if thumb touches the chin (thumb base lower than fingertips and thumb tip higher than base)
          if thumb_base_y > wrist_y and thumb_tip_y > thumb_base_y:
              #if thumb touches near the chin (base close to wrist and tip higher than base)
              if abs(thumb_base_y - wrist_y) < abs(index_tip_y - wrist_y):
                  return 'Wrong'

        
        return 'Unknown Sign'

if __name__ == "__main__":
    root = tb.Window(themename="darkly")
    app = SignLanguageApp(root)
    root.mainloop()