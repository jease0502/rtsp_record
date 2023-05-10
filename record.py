import cv2
import time
from datetime import datetime
import schedule

rtsp_url = 'rtsp://example.com/stream'
cap = cv2.VideoCapture(rtsp_url)
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

def record_video():
    while True:
        now = datetime.now()
        filename = now.strftime('%Y-%m-%d_%H-%M-%S.mp4')
        out = cv2.VideoWriter(filename, fourcc, 30, (width, height))
        next_save_time = time.time() + 60
        while True:
            ret, frame = cap.read()
            if ret:
                out.write(frame)
                current_time = time.time()
                if current_time >= next_save_time:
                    out.release()
                    break
            else:
                break
        out.release()
        if current_time >= next_save_time:
            continue
        else:
            break

    cap.release()
    cv2.destroyAllWindows()


now = datetime.now()
if (now.weekday() <= 4 and now.hour >= 18) or (now.weekday() >= 5 and now.hour >= 13):
    record_video()
else:
    schedule.every().monday.at("18:00").until("23:59").do(record_video)
    schedule.every().tuesday.at("18:00").until("23:59").do(record_video)
    schedule.every().wednesday.at("18:00").until("23:59").do(record_video)
    schedule.every().thursday.at("18:00").until("23:59").do(record_video)
    schedule.every().friday.at("18:00").until("23:59").do(record_video)
    schedule.every().saturday.at("13:00").until("23:59").do(record_video)
    schedule.every().sunday.at("13:00").until("23:59").do(record_video)

while True:
    schedule.run_pending()
    time.sleep(1)