import base64
import sys
import time

import cv2


def write(data: bytes) -> None:
    sys.stdout.buffer.write(data)
    sys.stdout.flush()


def write_png_image(data: bytes) -> None:
    data = base64.standard_b64encode(data)

    write(b"\033_Ga=T,f=100,m=1,C=1,q=2;\033\\")

    while data:
        payload, data = data[:4096], data[4096:]

        write(b"\033_Gm=1;" + payload + b"\033\\")

    write(b"\033_Gm=0;\033\\")


def delete_image() -> None:
    write(b"\033_Ga=d;\033\\")


def write_video(path: str, max_width: int):
    video_capture = cv2.VideoCapture(path)

    width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    video_capture.set(cv2.CAP_PROP_POS_FRAMES, 2210)

    fps = int(video_capture.get(cv2.CAP_PROP_FPS))

    width = max_width
    height = height // (width // max_width)

    is_success, frame = video_capture.read()

    last_frame = time.perf_counter()

    while is_success:
        frame = cv2.resize(frame, (width, height))

        _, buffer = cv2.imencode(".png", frame)

        time.sleep((1 / fps) - (time.perf_counter() - last_frame))

        write_png_image(buffer)

        last_frame = time.perf_counter()

        is_success, frame = video_capture.read()

    delete_image()


if __name__ == "__main__":
    write_video(sys.argv[1], 960)
