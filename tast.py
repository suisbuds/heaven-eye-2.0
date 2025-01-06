import cv2

# RTSP 流地址
rtsp_url = "rtsp://admin:admin888@192.168.1.2:555"

# 创建视频捕获对象
cap = cv2.VideoCapture(rtsp_url)

if not cap.isOpened():
    print("无法打开 RTSP 流")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("无法获取帧")
        break

    # 显示帧
    cv2.imshow('RTSP Stream', frame)

    # 按 'q' 键退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放资源
cap.release()
cv2.destroyAllWindows()