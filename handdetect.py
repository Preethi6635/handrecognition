import cv2
import mediapipe as mp
from google.protobuf.json_format import MessageToDict

# Initializing the MediaPipe Hands model
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    model_complexity=1,
    min_detection_confidence=0.75,
    min_tracking_confidence=0.75,
    max_num_hands=2)

# Initialize the video capture object
cap = cv2.VideoCapture(0)

try:
    while True:
        # Read video frame by frame
        success, img = cap.read()
        if not success:
            break

        # Flip the image (frame)
        img = cv2.flip(img, 1)

        # Convert BGR image to RGB image
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Process the RGB image
        results = hands.process(imgRGB)

        # If hands are present in the image (frame)
        if results.multi_hand_landmarks:
            # Both Hands are present in the image (frame)
            if len(results.multi_handedness) == 2:
                # Display 'Both Hands' on the image
                cv2.putText(img, 'Both Hands', (250, 50),
                            cv2.FONT_HERSHEY_COMPLEX,
                            0.9, (0, 255, 0), 2)
            # If any hand is present
            else:
                for i in results.multi_handedness:
                    # Return whether it is Right or Left Hand
                    label = MessageToDict(i)['classification'][0]['label']
                    if label == 'Left':
                        # Display 'Left Hand' on the left side of the window
                        cv2.putText(img, label + ' Hand', (20, 50),
                                    cv2.FONT_HERSHEY_COMPLEX,
                                    0.9, (0, 255, 0), 2)
                    if label == 'Right':
                        # Display 'Right Hand' on the right side of the window
                        cv2.putText(img, label + ' Hand', (460, 50),
                                    cv2.FONT_HERSHEY_COMPLEX,
                                    0.9, (0, 255, 0), 2)

        # Display the video frame
        cv2.imshow('Image', img)

        # Break the loop when 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    # Release the video capture object and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()
