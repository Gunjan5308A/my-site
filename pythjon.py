import cv2
import numpy as np

# Function to assess plant health based on leaf color
def assess_plant_health(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define color ranges
    green_mask = cv2.inRange(hsv, (35, 40, 40), (90, 255, 255))
    yellow_mask = cv2.inRange(hsv, (20, 100, 100), (30, 255, 255))
    brown_mask = cv2.inRange(hsv, (10, 50, 50), (20, 255, 255))

    green_ratio = np.sum(green_mask) / np.prod(green_mask.shape)
    yellow_ratio = np.sum(yellow_mask) / np.prod(yellow_mask.shape)
    brown_ratio = np.sum(brown_mask) / np.prod(brown_mask.shape)

    if green_ratio > 0.5:
        return "Healthy"
    elif yellow_ratio > 0.3:
        return "Possible Nutrient Deficiency"
    elif brown_ratio > 0.3:
        return "Unhealthy (Wilting or Disease)"
    else:
        return "Undetermined"

# Open camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Cannot access the camera.")
    exit()

print("Press 'q' to exit.")

while True:
    ret, frame = cap.read()
    if not ret:
        print("No frame captured!")
        break

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Detect green areas (likely plants)
    mask = cv2.inRange(hsv, (35, 40, 40), (90, 255, 255))
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    detected = False  # Flag to ensure only plants are analyzed

    for contour in contours:
        if cv2.contourArea(contour) > 500:  # Filter small objects
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
            
            plant_crop = frame[y:y+h, x:x+w]
            health_status = assess_plant_health(plant_crop)
            
            cv2.putText(frame, f"Health: {health_status}", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            detected = True  
    
    if not detected:
        cv2.putText(frame, "No Plant Detected", (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    # Display frame
    cv2.imshow("Plant Health Detector", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()