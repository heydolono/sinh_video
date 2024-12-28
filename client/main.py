import pickle
import tkinter as tk

import cv2
import numpy as np
import zmq
from PIL import Image, ImageTk


class VideoClient(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Синхронное воспроизведение видео")
        self.geometry("1280x960")
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.SUB)
        self.socket.connect("tcp://localhost:5555")
        self.socket.setsockopt_string(zmq.SUBSCRIBE, "")
        self.frames = [None] * 4
        self.timestamps = [None] * 4
        self.speed = 1
        self.image_on_canvas = [None] * 4
        self.image_objects = [None] * 4

        self.update_video()

    def update_video(self):
        try:
            frame_data = self.socket.recv()
            frames = pickle.loads(frame_data)
            print(f"Получено {len(frames)} кадров.")

            for i, frame in enumerate(frames):
                if frame is not None and isinstance(frame[0], np.ndarray):
                    print(f"[Поток {i+1}] Размер кадра: {frame[0].shape}")
                    self.timestamps[i] = frame[1]
                    frame_with_marker = self.add_marker(
                        frame[0], self.timestamps[i]
                    )
                    resized_frame = self.resize_frame(frame_with_marker)
                    frame_image = self.convert_to_image(resized_frame)
                    self.display_frame(frame_image, i)

        except Exception as e:
            print(f"Ошибка при получении данных: {e}")
        self.after(int(1000 / self.speed), self.update_video)

    def add_marker(self, frame, timestamp):
        """Добавление метки на изображение."""
        if frame is None or not isinstance(frame, np.ndarray):
            return frame

        cv2.putText(frame,
                    "STARIY KADR",
                    (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255), 2)
        cv2.putText(frame,
                    f"timestamp: {timestamp:.3f}",
                    (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2)
        return frame

    def resize_frame(self, frame):
        """Уменьшение размера кадра, чтобы кадры не перекрывали друг друга."""
        if frame is None:
            return None
        window_width = self.winfo_width()
        window_height = self.winfo_height()
        resized_frame = cv2.resize(
            frame, (window_width // 2, window_height // 2)
        )
        return resized_frame

    def convert_to_image(self, frame):
        """Преобразование кадра из OpenCV в формат, пригодный для Tkinter."""
        if frame is None:
            return None
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame)
        return ImageTk.PhotoImage(image)

    def display_frame(self, frame_image, index):
        """Отображение кадра на холсте в соответствующем углу."""
        if frame_image:
            x_offset = 0
            y_offset = 0
            if index == 0:
                x_offset, y_offset = 0, 0
            elif index == 1:
                x_offset, y_offset = self.winfo_width() // 2, 0
            elif index == 2:
                x_offset, y_offset = 0, self.winfo_height() // 2
            elif index == 3:
                x_offset, y_offset = self.winfo_width() // 2, self.winfo_height() // 2
            if self.image_on_canvas[index] is None:
                self.image_on_canvas[index] = self.canvas.create_image(
                    x_offset, y_offset, image=frame_image, anchor="nw"
                )
                self.image_objects[index] = frame_image
            else:
                self.canvas.itemconfig(self.image_on_canvas[index],
                                       image=frame_image)
                self.image_objects[index] = frame_image
            self.update_idletasks()


if __name__ == "__main__":
    app = VideoClient()
    app.mainloop()
