import cv2 
import random
import time
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision




MODEL_PATH = "hand_landmarker.task"


base_options = python.BaseOptions(model_asset_path = MODEL_PATH) # Model dosyasının yolu
options = vision.HandLandmarkerOptions(base_options = base_options, num_hands=1 )  # Maksimum 1 el tespiti
detector = vision.HandLandmarker.create_from_options(options) # Modeli oluştur

cap = cv2.VideoCapture(0)

ates_edildi = False
skor = 0
sure = 30
oyun_basladi = False
oyun_bitti = False
baslangic_zamani= None
kalan_sure = sure

hedef_x = None
hedef_y = None
hedef_R = 60


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

    if hedef_x is None:
        hedef_x = width // 2 
        hedef_y = height // 2 

    if oyun_basladi:
        simdiki_zaman = time.monotonic()

        gecen_sure = simdiki_zaman - baslangic_zamani

        kalan_sure = int(max(0, sure - gecen_sure))

    if kalan_sure == 0 and oyun_basladi:
        oyun_basladi =False
        oyun_bitti = True
        print("OYUN BİTTİ")
              
        

    cv2.circle(frame,(hedef_x,hedef_y),hedef_R,(0,0,255),-1)
    cv2.putText(frame,f"SKOR: {skor}",(60,70),cv2.FONT_HERSHEY_SIMPLEX,3,(1,19,123),3)
    cv2.putText(frame,f"KALAN SÜRE:{kalan_sure}",(1100,100),cv2.FONT_HERSHEY_SIMPLEX,3,(1,19,123),3)

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

        if parmak_mesafe < 50 and not ates_edildi and oyun_basladi:
            print("Ateş Edildi")
            ates_edildi = True
            if hedef_mesafe <= hedef_R:
                skor +=10
                hedef_x = random.randint(hedef_R,width - hedef_R)
                hedef_y = random.randint(hedef_R, height - hedef_R)

                print("TAM İSABET!!!")
            else:
                print("IKSALADIN!!!")    

        elif parmak_mesafe > 100 and ates_edildi and oyun_basladi:
            print("Tekrar ateşe hazır")
            ates_edildi = False
        
  
       # print(f"hedef ile parmak arası mesafe: {hedef_mesafe:.2f} piksel")

    else:  # el gösterilmeszse belirt
        print("xxxxx")


    cv2.imshow("frame",frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('s') and not oyun_basladi:
        oyun_basladi = True
        baslangic_zamani = time.monotonic()
        skor = 0
        ates_edildi =False
        oyun_bitti = False
        print("OYUN BASLADI!")

    elif key == ord("q"):
        break

cap.release()
detector.close()
cv2.destroyAllWindows()