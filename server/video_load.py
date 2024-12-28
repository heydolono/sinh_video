import cv2


def initialize_video_streams(video_paths):
    """Инициализация потоков видео для каждого пути в video_paths."""
    return [cv2.VideoCapture(path) for path in video_paths]


def load_annotations(annotation_paths):
    """Загрузка аннотаций из файлов."""
    annotations = []
    for path in annotation_paths:
        with open(path, 'r') as file:
            timestamps = [float(line.strip()) for line in file.readlines()]
            annotations.append(timestamps)
    return annotations
