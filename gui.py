import cv2
import tkinter as tk
from PIL import Image, ImageTk

from recognition import recognize


def start_gui():

    root = tk.Tk()

    root.title("Face Recognition")
    root.geometry("900x700")


    title = tk.Label(
        root,
        text="FACE RECOGNITION SYSTEM",
        font=("Arial", 20, "bold")
    )

    title.pack(pady=10)


    camera_label = tk.Label(root)

    camera_label.pack()


    status = tk.Label(
        root,
        text="Camera OFF",
        font=("Arial", 14)
    )

    status.pack(pady=5)


    name_label = tk.Label(
        root,
        text="Recognized: None",
        font=("Arial", 14)
    )

    name_label.pack(pady=5)


    cap = None
    running = False


    def update():

        if not running:
            return

        success, frame = cap.read()

        if success:

            frame, names = recognize(frame)


            if len(names) > 0:

                name_label.config(
                    text="Recognized: " + ", ".join(names)
                )

            else:

                name_label.config(
                    text="Recognized: None"
                )


            frame_rgb = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2RGB
            )

            img = Image.fromarray(frame_rgb)

            img = ImageTk.PhotoImage(img)

            camera_label.config(image=img)

            camera_label.image = img


        root.after(10, update)


    def start_camera():

        nonlocal cap
        nonlocal running

        if running:
            return

        cap = cv2.VideoCapture(0)

        running = True

        status.config(
            text="Camera ON"
        )

        update()


    def stop_camera():

        nonlocal cap
        nonlocal running

        running = False

        if cap is not None:

            cap.release()
            cap = None

        camera_label.config(image="")

        name_label.config(
            text="Recognized: None"
        )

        status.config(
            text="Camera OFF"
        )


    button_frame = tk.Frame(root)

    button_frame.pack(pady=15)


    start_button = tk.Button(
        button_frame,
        text="START CAMERA",
        command=start_camera,
        width=15
    )

    start_button.grid(
        row=0,
        column=0,
        padx=5
    )


    stop_button = tk.Button(
        button_frame,
        text="STOP CAMERA",
        command=stop_camera,
        width=15
    )

    stop_button.grid(
        row=0,
        column=1,
        padx=5
    )


    exit_button = tk.Button(
        button_frame,
        text="EXIT",
        command=root.destroy,
        width=15
    )

    exit_button.grid(
        row=0,
        column=2,
        padx=5
    )


    root.mainloop()