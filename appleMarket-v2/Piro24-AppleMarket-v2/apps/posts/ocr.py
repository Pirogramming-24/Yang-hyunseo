from paddleocr import PaddleOCR
import cv2
import re

ocr = PaddleOCR(lang='korean', use_angle_cls=True)

def extract_nutrients(texts):
    result = {
        "calorie": None,
        "carb": None,
        "protein": None,
        "fat": None,
    }

    for t in texts:
        s = t.replace(" ", "").lower()

        # --- 칼로리 ---
        # 2,000 kcal (기준치) 제외
        if "kcal" in s and "2,000" not in s and "2000" not in s:
            m = re.search(r"(\d{2,4})kcal", s)
            if m:
                val = m.group(1)
                # 100~999 kcal만 허용 (실제 식품 범위)
                if 50 <= int(val) <= 1500:
                    result["calorie"] = val

        # --- 탄수화물 ---
        if "탄수화물" in s:
            m = re.search(r"탄수화물([\d\.]+)g", s)
            if m:
                result["carb"] = m.group(1)

        # --- 단백질 ---
        if "단백질" in s:
            m = re.search(r"단백질([\d\.]+)g", s)
            if m:
                result["protein"] = m.group(1)

        # --- 지방 ---
        if "지방" in s and "트랜스" not in s and "포화" not in s:
            m = re.search(r"지방([\d\.]+)g", s)
            if m:
                result["fat"] = m.group(1)

    return result



def analyze_nutrition(image_path):
    img = cv2.imread(image_path)
    result = ocr.predict(img)
    texts = result[0]["rec_texts"]

    return extract_nutrients(texts)
