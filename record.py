import cv2
import time
from datetime import datetime
import schedule

# RTSP串流網址
rtsp_url = 'rtsp://example.com/stream'

# 設定OpenCV的RTSP串流接收器
cap = cv2.VideoCapture(rtsp_url)

# 設定編碼器和視頻大小
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

def record_video():
    # 設定視頻儲存器
    now = datetime.now()
    filename = now.strftime('%Y-%m-%d_%H-%M-%S.mp4')
    out = cv2.VideoWriter(filename, fourcc, 30, (width, height))

    # 設定每半個小時存檔一次的計時器
    start_time = time.time()
    next_save_time = start_time + 1800

    while True:
        # 讀取RTSP串流的一個影格
        ret, frame = cap.read()

        if ret:
            # 將影格寫入視頻文件
            out.write(frame)

            # 檢查是否到了下一個存檔時間
            current_time = time.time()
            if current_time >= next_save_time:
                # 關閉視頻儲存器，儲存視頻文件
                out.release()

                # 更新下一個存檔時間
                next_save_time = current_time + 1800
        else:
            break

    # 釋放資源
    cap.release()
    cv2.destroyAllWindows()

# 判斷目前時間是否符合規則
now = datetime.now()
if (now.weekday() <= 4 and now.hour >= 18) or (now.weekday() >= 5 and now.hour >= 13):
    record_video()
else:
    # 設定排程，等待下一次符合規則的時間再開始錄影
    schedule.every().monday.at("18:00").until("23:59").do(record_video)
    schedule.every().tuesday.at("18:00").until("23:59").do(record_video)
    schedule.every().wednesday.at("18:00").until("23:59").do(record_video)
    schedule.every().thursday.at("18:00").until("23:59").do(record_video)
    schedule.every().friday.at("18:00").until("23:59").do(record_video)
    schedule.every().saturday.at("13:00").until("23:59").do(record_video)
    schedule.every().sunday.at("13:00").until("23:59").do(record_video)

while True:
    # 執行所有已排程的工作
    schedule.run_pending()

    # 等待一秒
    time.sleep(1)