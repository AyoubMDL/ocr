import os
import cv2

# Replace 'input_folder' with the path to the folder containing your images
input_folder = 'ocr_img'
output_folder = 'cropped_images'

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Loop through each file in the input folder
for filename in os.listdir(input_folder):
    # Construct the full path to the image file
    image_path = os.path.join(input_folder, filename)

    # Read the image
    image = cv2.imread(image_path)

    # Check if the image is loaded successfully
    if image is None:
        print(f"Error: Unable to load the image from {image_path}")
        continue

    # Crop the image (adjust the cropping region as needed)
    cropped_image = image[350:, 280:1223]

    # Construct the output path for the cropped image
    output_path = os.path.join(output_folder, f"cropped_{filename}")

    # Save the cropped image
    cv2.imwrite(output_path, cropped_image)

    print(f"Cropped and saved: {output_path}")

print("Cropping and saving complete.")
