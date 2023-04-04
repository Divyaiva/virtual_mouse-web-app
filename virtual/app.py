from flask import Flask,render_template,Response
import cv2
import mediapipe as mp
import pyautogui

app = Flask(__name__)
cap = cv2.VideoCapture(0)
#hand_detector = mp.solutions.hands.Hands()
#drawing_utils = mp.solutions.drawing_utils
#screen_width, screen_height = pyautogui.size()
#index_y = 0
@app.route('/')
def index():
    return render_template('index1.html')


def virtual_mouse():
    hand_detector = mp.solutions.hands.Hands()
    drawing_utils = mp.solutions.drawing_utils
    screen_width, screen_height = pyautogui.size()
    index_y = 0
    while True:
        _, frame = cap.read()
        frame = cv2.flip(frame, 1)
        frame_height, frame_width, _ = frame.shape
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        output = hand_detector.process(rgb_frame)
        hands = output.multi_hand_landmarks
        if hands:
            for hand in hands:
                drawing_utils.draw_landmarks(frame, hand)
                landmarks = hand.landmark
                for id, landmark in enumerate(landmarks):
                    x = int(landmark.x*frame_width)
                    y = int(landmark.y*frame_height)
                    if id == 8:
                        cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 0, 255))
                        index_x = screen_width/frame_width*x
                        index_y = screen_height/frame_height*y

                    if id == 4:
                        cv2.circle(img=frame, center=(x,y), radius=10, color=(0, 0, 255))
                        thumb_x = screen_width/frame_width*x
                        thumb_y = screen_height/frame_height*y
                        print('outside', abs(index_y - thumb_y))
                        if abs(index_y - thumb_y) < 20:
                            pyautogui.click()
                            pyautogui.sleep(1)
                        elif abs(index_y - thumb_y) < 100:
                            pyautogui.moveTo(index_x, index_y)
        cv2.imshow('Virtual Mouse', frame)
        cv2.waitKey(1)

     
        
        


        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
    #return render_template("index1.html")
#@app.route('/')
#def index():
    #return render_template('index1.html')

@app.route('/video')
def video():
    return Response(virtual_mouse(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__=="__main__":
    app.run(debug=True)




