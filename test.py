from screeninfo import get_monitors
import pyautogui
import cv2
import numpy as np

def display_selected_monitor(monitor, monitor_index, scale=0.5):
    try:
        print(f"Displaying monitor {monitor_index}: {monitor}")
        print("Press 'q' in the display window to quit.")
        
        # Create a resizable window
        cv2.namedWindow(f"Monitor {monitor_index}", cv2.WINDOW_NORMAL)

        while True:
            # Capture the specified monitor's region
            screenshot = pyautogui.screenshot(region=(
                monitor.x,  # Starting x-coordinate
                monitor.y,  # Starting y-coordinate
                monitor.width,  # Width of the monitor
                monitor.height  # Height of the monitor
            ))
            
            # Convert the screenshot to a NumPy array
            frame = np.array(screenshot)
            
            # Convert the color from RGB (Pillow) to BGR (OpenCV)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            
            # Resize the frame (scale down by default)
            frame_resized = cv2.resize(
                frame, 
                (int(monitor.width * scale), int(monitor.height * scale))
            )
            
            # Display the screen
            cv2.imshow(f"Monitor {monitor_index}", frame_resized)
            
            # Exit if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Quitting...")
                break
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
    finally:
        # Clean up OpenCV windows
        cv2.destroyAllWindows()

if __name__ == "__main__":
    # Get all monitors
    monitors = get_monitors()
    for i, monitor in enumerate(monitors):
        print(f"Monitor {i}: {monitor}")

    # Select a monitor (0 for Monitor 0, 1 for Monitor 1)
    monitor_index = 0  # Change this to 1 for Monitor 1
    selected_monitor = monitors[monitor_index]

    # Display the monitor with scaling (e.g., 0.5 for 50% size)
    display_selected_monitor(selected_monitor, monitor_index, scale=0.5)
