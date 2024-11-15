import os
import shutil
from sklearn.model_selection import train_test_split

# Set paths (update these paths as per your directory structure)
dataset_dir = "C:\\Users\\pavan\\Desktop\\crop-soil-management\\ReducedPlantVillage"
train_dir = "C:\\Users\\pavan\\Desktop\\crop-soil-management\\train"
val_dir = "C:\\Users\\pavan\\Desktop\\crop-soil-management\\val"

# Create directories for training and validation sets
os.makedirs(train_dir, exist_ok=True)
os.makedirs(val_dir, exist_ok=True)

# Split images for each class (folder)
for class_folder in os.listdir(dataset_dir):
    class_folder_path = os.path.join(dataset_dir, class_folder)
    if os.path.isdir(class_folder_path):
        # List all images in the folder
        images = os.listdir(class_folder_path)

        # Split images into training and validation (80% training, 20% validation)
        train_images, val_images = train_test_split(images, test_size=0.2, random_state=42)

        # Create class folders for train and validation sets
        os.makedirs(os.path.join(train_dir, class_folder), exist_ok=True)
        os.makedirs(os.path.join(val_dir, class_folder), exist_ok=True)

        # Move images to their respective directories
        for image in train_images:
            shutil.move(os.path.join(class_folder_path, image), os.path.join(train_dir, class_folder, image))

        for image in val_images:
            shutil.move(os.path.join(class_folder_path, image), os.path.join(val_dir, class_folder, image))

print("Dataset successfully split into training and validation sets.")
