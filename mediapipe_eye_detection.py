import cv2 
import numpy as np
import mediapipe as mp 
import socket
import time

serverAddressPort = ("192.168.77.9", 20001)
bufferSize = 1024
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)######


mp_face_mesh = mp.solutions.face_mesh


#Landmarks of eyes and irises
LEFT_EYE =[ 362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398 ]
RIGHT_EYE=[ 33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161 , 246 ] 
LEFT_IRIS = [474, 475, 476, 477]
RIGHT_IRIS = [469, 470, 471, 472]


cap = cv2.VideoCapture(0)

with mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as face_mesh:
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img_h, img_w = frame.shape[:2]
        results = face_mesh.process(rgb_frame)
        if results.multi_face_landmarks:
            mesh_points=np.array([np.multiply([p.x, p.y], [img_w, img_h]).astype(int) for p in results.multi_face_landmarks[0].landmark])

            #detected eyes and draw rectangle
            xl, yl, wl, hl = cv2.boundingRect(mesh_points[LEFT_EYE])
            xr, yr, wr, hr = cv2.boundingRect(mesh_points[RIGHT_EYE])
            cv2.rectangle(frame, (xl,yl), (xl+wl, yl+hl), (0,255,0), 1)
            cv2.rectangle(frame, (xr,yr), (xr+wr, yr+hr), (0,255,0), 1)

            left_roi = frame[yl:yl+hl, xl:xl+wl]
            right_roi = frame[yr:yr+hr, xr:xr+wr]

            #detected iris and center point
            (l_cx, l_cy), l_radius = cv2.minEnclosingCircle(mesh_points[LEFT_IRIS])
            (r_cx, r_cy), r_radius = cv2.minEnclosingCircle(mesh_points[RIGHT_IRIS])
            center_left = np.array([l_cx, l_cy], dtype=np.int32)
            center_right = np.array([r_cx, r_cy], dtype=np.int32)

            cv2.circle(frame, center_left, int(l_radius), (255,0,255), 1, cv2.LINE_AA) #iris
            cv2.circle(frame, center_right, int(r_radius), (255,0,255), 1, cv2.LINE_AA) #iris

            cv2.circle(frame, center_left, radius=0, color=(0, 0, 255), thickness=2) #göz bebeği
            cv2.circle(frame, center_right, radius=0, color=(0, 0, 255), thickness=2) #göz bebeği
            
            #eye bounding boxes divided 9 area
            #command variable should be sended to microcontroler
            komut = None
            if(center_left[1] < (yl + (2*hl/3)) and center_left[1] > (yl + (hl/3)) and center_left[0] < (xl + (2*wl/3)) and center_left[0] > (xl + (wl/3))):
                frame = cv2.putText(frame, "Merkez Bölge", (15, 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
                komut = "Merkez Bölge" #göz merkeze baktığında araç duracak
                print(komut)
            elif(center_left[1] < (yl + (hl/3)) and center_left[1] > (yl) and center_left[0] < (xl + (wl/3)) and center_left[0] > (xl)):
                frame = cv2.putText(frame, "Sol yukari", (15, 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
                komut = "Sol yukari"
                print(komut)
            elif(center_left[1] < (yl + (hl/3)) and center_left[1] > (yl) and center_left[0] < (xl + (2*wl/3)) and center_left[0] > (xl+ (wl/3))):
                frame = cv2.putText(frame, "Yukari", (15, 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
                komut = "Yukari"
                print(komut)
            elif(center_left[1] < (yl + (hl/3)) and center_left[1] > (yl) and center_left[0] < (xl + wl) and center_left[0] > (xl + (2*hl/3))):
                frame = cv2.putText(frame, "Sag yukari", (15, 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
                komut = "Sag yukari"
                print(komut)
            elif(center_left[1] < (yl + hl) and center_left[1] > (yl + (2*hl/3)) and center_left[0] < (xl + (wl/3)) and center_left[0] > (xl)):
                frame = cv2.putText(frame, "Sol asagi", (15, 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
                komut = "Sol asagi"
                print(komut)
            elif(center_left[1] < (yl + hl) and center_left[1] > (yl + (2*hl/3)) and center_left[0] < (xl + (2*wl/3)) and center_left[0] > (xl + (wl/3))):
                frame = cv2.putText(frame, "Asagi", (15, 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
                komut = "Asagi"
                print(komut)
            elif(center_left[1] < (yl + hl) and center_left[1] > (yl + (2*hl/3)) and center_left[0] < (xl + wl) and center_left[0] > (xl + (2*wl/3))):
                frame = cv2.putText(frame, "Sag asagi", (15, 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
                komut = "Sag asagi"
                print(komut)
            elif(center_left[1] < (yl + (2*hl/3)) and center_left[1] > (yl + (hl/3)) and center_left[0] < (xl + (wl/3)) and center_left[0] > (xl)):
                frame = cv2.putText(frame, "Sol", (15, 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
                komut = "Sol"
                print(komut)
            elif(center_left[1] < (yl + (2*hl/3)) and center_left[1] > (yl + (hl/3)) and center_left[0] < (xl + wl) and center_left[0] > (xl + (2*wl/3))):
                frame = cv2.putText(frame, "Sag", (15, 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)
                komut = "Sag"
                print(komut)
            else:
                komut = "Empty Package" 
                print(komut)
            
            bytesToSend = str.encode(komut)
            UDPClientSocket.sendto(bytesToSend, serverAddressPort)
            msgFromServer = UDPClientSocket.recvfrom(bufferSize)

        cv2.imshow('img', frame)

        key = cv2.waitKey(1)
        if key ==ord('q'):
            break
cap.release()
cv2.destroyAllWindows()
            