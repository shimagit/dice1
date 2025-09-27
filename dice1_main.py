import cv2
from picamera2 import Picamera2
from libcamera import controls

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()
#カメラを連続オートフォーカスモードにする
picam2.set_controls({"AfMode": controls.AfModeEnum.Continuous})
 
#import cv2

# 背景画像の取得
#cap = cv2.VideoCapture(0)  # カメラを起動する
#_, background = cap.read()  # 最初のフレームを背景画像として取得
while True:
  #background = picam2.capture_file('test_x.jpg')
  #cv2.imshow("Camera", background)
  background = picam2.capture_array()
  cv2.imshow("Camera", background)
  key = cv2.waitKey(1)
  #Escキーを入力されたら画面を閉じる
  if key == 27:
    picam2.capture_file('test_x.jpg')
    break


# 背景画像をグレースケールに変換
background_gray = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)

# メインの処理
while True:
    # カメラからフレームを取得
    #_, frame = cap.read()
    frame = picam2.capture_array()


    # グレースケールに変換
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 背景差分を計算
    diff = cv2.absdiff(frame_gray, background_gray)

    # 二値化処理
    _, thresh = cv2.threshold(diff, 60, 255, cv2.THRESH_BINARY)

    # モルフォロジー処理（オープニング）
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

    # 物体を検出した領域を描画
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnt = 0

    for contour in contours:
        det = cv2.contourArea(contour) 
        print(det)
        if det > 200 and det < 2000:  # 面積が一定以上のもののみ対象
            x, y, w, h = cv2.boundingRect(contour)
            if w >= h :
               rate = w / h
            else:
               rate = h / w
            if rate < 1.25:
              cnt = cnt + 1
              cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # テキストを追加する
    text = f"Count={cnt}"
    font = cv2.FONT_HERSHEY_SIMPLEX
    org = (30, 50)  # テキストの開始位置
    fontScale = 1
    color = (255, 0, 0)  # テキストの色 (BGR形式)
    thickness = 2  # テキストの太さ

    # テキストを画像に追加する
    frame = cv2.putText(frame, text, org, font, fontScale, color, thickness, cv2.LINE_AA)

    # 結果を表示
    cv2.imshow("Frame", frame)
    cv2.imshow("Difference", thresh)

    # 'q'を押すと終了
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 後処理
#cap.release()
#cv2.destroyAllWindows()

"""
while True:
  im = picam2.capture_array()
  cv2.imshow("Camera", im)
 
  key = cv2.waitKey(1)
  # Escキーを入力されたら画面を閉じる
  if key == 27:
    picam2.capture_file("test_x"+ '.jpg')
    break
"""
picam2.stop()
cv2.destroyAllWindows()
