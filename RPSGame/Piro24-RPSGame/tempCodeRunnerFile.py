import mediapipe as mp
import math, time
from mediapipe.tasks.python import vision
from webcam import cv2_stream
import cv2 as cv
from visualization import draw_manual, print_RSP_result



## 필요한 함수 작성
def distance(p1, p2):
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


FINGER_TIPS = [8, 12, 16, 20]
FINGER_PIPS = [6, 10, 14, 18]

def count_extended_fingers(hand_landmarks):
    wrist = hand_landmarks[0]
    count = 0

    for tip, pip in zip(FINGER_TIPS, FINGER_PIPS):
        d_tip = distance(hand_landmarks[tip], wrist)
        d_pip = distance(hand_landmarks[pip], wrist)

        if d_tip > d_pip:   # 펴져 있음
            count += 1

    return count



def classify_rps(hand_landmarks):
    finger_count = count_extended_fingers(hand_landmarks)

    if finger_count == 0:
        return 0   # Rock
    elif finger_count == 4:
        return 1   # Paper
    elif finger_count == 2:
        return 2   # Scissors
    else:
        return None


def run_rps_camera():
    cap = cv.VideoCapture(0)  # Mac이면 1 or 2

    base_options = vision.BaseOptions(model_asset_path="hand_landmarker.task")
    options = vision.HandLandmarkerOptions(
        base_options=base_options,
        num_hands=1
    )
    detector = vision.HandLandmarker.create_from_options(options)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        image_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=image_rgb)

        result = detector.detect(mp_image)

        # 1. 랜드마크 그리기
        frame = draw_manual(frame, result)

        # 2. RPS 판단
        rps = None
        if result.hand_landmarks:
            rps = classify_rps(result.hand_landmarks[0])

        # 3. 결과를 카메라 화면 위에 출력
        frame = print_RSP_result(frame, rps)

        cv.imshow("RPS Game", frame)

        if cv.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv.destroyAllWindows()



if __name__ == "__main__":
    run_rps_camera()