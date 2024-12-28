import pickle
import time

import numpy as np
import zmq
from config import ANNOTATION_PATHS, SYNC_FPS, VIDEO_PATHS
from frame_extr import read_frame_by_timestamp
from video_load import initialize_video_streams, load_annotations


def video_server():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5555")
    video = initialize_video_streams(VIDEO_PATHS)
    annotations = load_annotations(ANNOTATION_PATHS)
    start_time = min(
        annotations[0][0], annotations[1][0],
        annotations[2][0], annotations[3][0]
    )
    current_time = start_time
    last_frames = [None for _ in range(len(video))]
    print("Сервер запущен на tcp://*:5555")
    while True:
        frames = []
        for i, (video_stream, timestamps) in enumerate(zip(video, annotations)):
            frame_data = read_frame_by_timestamp(
                video_stream, timestamps, current_time, last_frames[i]
            )
            if frame_data is None or frame_data[0] is None:
                print(f"[Поток {i+1}] Нет кадра для времени"
                      f" {current_time}, используется предыдущий кадр.")
            else:
                print(
                    f"[Поток {i+1}] Считан кадр с временной"
                    f" меткой {frame_data[1]}")
            if frame_data is not None and frame_data[0] is not None:
                last_frames[i] = frame_data
                frames.append((last_frames[i][0], last_frames[i][1]))
            else:
                print(f"[Поток {i+1}] Кадр пустой.")
        try:
            socket.send(pickle.dumps(frames))
            print("Кадры отправлены клиенту.")
        except Exception as e:
            print(f"Ошибка при отправке данных: {e}")
        current_time += 1 / SYNC_FPS
        time.sleep(1 / SYNC_FPS)


if __name__ == "__main__":
    video_server()
