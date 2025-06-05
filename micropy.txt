import machine
import esp
import time
import os

# Constants for Deep Sleep
SLEEP_TIME = 30 * 60 * 1000000  # 30 minutes in microseconds

# Simulating a camera function (since OV7670 requires low-level access)
def capture_image():
    # Dummy function: Normally, you'd interface with OV7670 via SPI/I2C
    return [(100, 200, 100), (180, 180, 60), (150, 80, 30)]  # Simulated pixel data

# Function to assess plant health based on pixel colors
def assess_plant_health(image_data):
    green_count, yellow_count, brown_count = 0, 0, 0
    total_pixels = len(image_data)

    for pixel in image_data:
        red, green, blue = pixel

        if green > red and green > blue:
            green_count += 1
        elif red > green and red > blue:
            yellow_count += 1
        elif red > green and blue < 50:
            brown_count += 1 

    green_ratio = green_count / total_pixels
    yellow_ratio = yellow_count / total_pixels
    brown_ratio = brown_count / total_pixels

    if green_ratio > 0.5:
        return "Healthy"
    elif yellow_ratio > 0.3:
        return "Possible Nutrient Deficiency"
    elif brown_ratio > 0.3:
        return "Unhealthy (Wilting or Disease)"
    else:
        return "Undetermined"

# Function to save results to a text file
def log_result(health_status):
    try:
        with open("/plant_health_log.txt", "a") as file:
            file.write(f"Plant Health: {health_status}\n")
        print("Logged to file successfully!")
    except Exception as e:
        print(f"Error logging file: {e}")

# Main execution
print("Capturing image...")
image_data = capture_image()  # Simulated image capture
health_status = assess_plant_health(image_data)
print(f"Plant Health: {health_status}")

log_result(health_status)  # Save to file

# Deep sleep for 30 minutes
print("Sleeping for 30 minutes...")
machine.deepsleep(SLEEP_TIME)