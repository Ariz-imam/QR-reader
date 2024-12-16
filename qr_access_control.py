import cv2
import pandas as pd
import time

# Load your valid user IDs from the CSV file and remove duplicates
csv_file = 'qr_data.csv'
df = pd.read_csv(csv_file)

# Use a set to store unique user IDs
valid_ids = set(df['USER_ID'].drop_duplicates())  # Remove duplicates

def main():
    cap = cv2.VideoCapture(0)  # Start the webcam
    detector = cv2.QRCodeDetector()  # Create the QRCodeDetector

    last_scanned_id = None  # To track the last scanned QR code
    scan_completed = False  # Flag to indicate if the scan is completed for the current ID

    while True:
        ret, frame = cap.read()  # Read a frame from the webcam
        if not ret:
            print("Failed to capture video")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert the frame to grayscale
        
        # Detect and decode the QR code
        data, points, _ = detector.detectAndDecode(gray)

        # Check if a QR code is detected
        if points is not None and data:  # Check if points and data are valid
            # Draw the bounding box around the detected QR code
            pts = points[0].astype(int)
            cv2.polylines(frame, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

            # Validate the QR code data against the list of valid user IDs
            if data in valid_ids:
                if last_scanned_id != data:  # New valid scan detected
                    print("Valid QR Code Data:", data)
                    last_scanned_id = data  # Update last scanned ID
                    scan_completed = True  # Mark scan as completed
                elif scan_completed:  # If the scan is completed for this ID
                    # Print duplicate message only once
                    print("Duplicate scan detected:", data)
                    scan_completed = False  # Reset scan completion status to avoid further duplicate messages
            else:
                print("Invalid QR Code Data:", data)
                last_scanned_id = None  # Reset if invalid data is read
                scan_completed = False  # Reset scan completion status

        # If scan is completed for current valid ID, skip further processing
        if scan_completed:
            continue  # Skip to the next frame

        cv2.imshow("QR Code Scanner", frame)  # Show the video feed
        
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
            break

    cap.release()  # Release the webcam
    cv2.destroyAllWindows()  # Close all OpenCV windows

if __name__ == "__main__":
    main()
