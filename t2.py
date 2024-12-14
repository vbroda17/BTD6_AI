import pyautogui
import cv2
import numpy as np

def capture_and_process_screen(scale=0.5):
    print("Press 'q' in the display window to quit.")

    # Create a resizable window
    cv2.namedWindow("Processed Screen", cv2.WINDOW_NORMAL)

    while True:
        # Capture the screen
        screenshot = pyautogui.screenshot()
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # Resize for better performance
        frame_resized = cv2.resize(
            frame,
            (int(frame.shape[1] * scale), int(frame.shape[0] * scale))
        )

        # Apply computer vision processing (e.g., edge detection)
        edges = cv2.Canny(frame_resized, 100, 200)

        # Display the processed screen
        cv2.imshow("Processed Screen", edges)

        # Quit if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Quitting...")
            break

    # Cleanup
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_and_process_screen(scale=0.5)
