import cv2


def read_frame_by_timestamp(
        video_capture, timestamps, current_time, last_frame
    ):
    """Считывание кадра по временной метке."""
    frame = None
    closest_index = None
    for i, timestamp in enumerate(timestamps):
        if timestamp >= current_time:
            closest_index = i
            break
    if closest_index is not None:
        video_capture.set(cv2.CAP_PROP_POS_FRAMES, closest_index)
        success, frame = video_capture.read()
        if success:
            return frame, timestamps[closest_index]
    return last_frame
