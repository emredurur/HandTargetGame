import cv2 
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision



MODEL_PATH = "hand_landmarker.task"


base_options = python.BaseOptions(model_asset_path = MODEL_PATH) # Model dosyasının yolu
options = vision.HandLandmarkerOptions(base_options = base_options, num_hands=1 )  # Maksimum 1 el tespiti
detector = vision.HandLandmarker.create_from_options(options) # Modeli oluştur

cap = cv2.VideoCapture(0)

ates_edildi = False

while True:

    ret,frame = cap.read()

    if not ret:
        break

    frame=cv2.flip(frame,1)
    
    rgb_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)  # MediaPipe görüntü formatı
    
    # El tespiti yap
    detection_result = detector.detect(mp_image)
    # Görüntünün boyutlarını al
    height, width = frame.shape[:2]

    hedef_x = width // 2
    hedef_y = height // 2
    hedef_R = 60


    cv2.circle(frame,(hedef_x,hedef_y),hedef_R,(0,0,255),-1)


    if detection_result.hand_landmarks:   
        hand = detection_result.hand_landmarks[0]
        index_finger = hand[8]
        bas_parmak = hand[4]

        # Normalize koordinatları piksele dönüştür
        x_degeri = int(index_finger.x * width)
        y_degeri = int(index_finger.y * height)

        bas_x = int(bas_parmak.x * width)
        bas_y = int(bas_parmak.y * height)

        parmak_mesafe = ((bas_x - x_degeri)**2 + (bas_y - y_degeri)**2)**0.5
        hedef_mesafe = ((hedef_x-x_degeri)**2 + (hedef_y - y_degeri)**2)**0.5

        cv2.circle(frame,(x_degeri,y_degeri),25,(0,255,0),-1)
        cv2.line(frame,(x_degeri-25,y_degeri),(x_degeri+25,y_degeri),(0,0,255),3)
        cv2.line(frame,(x_degeri,y_degeri-25),(x_degeri,y_degeri+25),(0,0,255),3)

        if parmak_mesafe < 100 and not ates_edildi:
            print("Ateş Edildi")
            ates_edildi = True

        elif parmak_mesafe > 160 and ates_edildi:
            print("Tekrar ateşe hazır")
            ates_edildi = False
        
        
       # print(f"Parmaklar arasi mesafe: {parmak_mesafe:.2f} piksel")
        print(f"hedef ile parmak arası mesafe: {hedef_mesafe:.2f} piksel")

    else:  # el gösterilmeszse belirt
        print("xxxxx")


    cv2.imshow("frame",frame)

    if cv2.waitKey(1) & 0xFF == ord("q") :
        break

cap.release()
detector.close()
cv2.destroyAllWindows()