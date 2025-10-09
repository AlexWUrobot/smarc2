import os
import glob
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
import numpy as np


import cv2


import matplotlib.pyplot as plt
import datetime


# ===== 1. CNN Model Definition =====
class AnchorPointCNN(nn.Module):
    def __init__(self):
        super(AnchorPointCNN, self).__init__()
        self.conv1 = nn.Conv2d(3, 16, 3, padding=1)
        self.conv2 = nn.Conv2d(16, 32, 3, padding=1)
        self.conv3 = nn.Conv2d(32, 64, 3, padding=1)
        self.pool = nn.MaxPool2d(2, 2)
        self.fc1 = nn.Linear(64 * 28 * 28, 256)  # for 224x224
        self.fc2 = nn.Linear(256, 128)
        self.fc3 = nn.Linear(128, 4)  # x1, y1, x2, y2

    def forward(self, x):
        x = self.pool(F.relu(self.conv1(x)))  # -> 112x112
        x = self.pool(F.relu(self.conv2(x)))  # -> 56x56
        x = self.pool(F.relu(self.conv3(x)))  # -> 28x28
        x = x.view(x.size(0), -1)
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        return self.fc3(x)
    

class AnchorPointDataset(Dataset):
    def __init__(self, image_folder, annotations, output_size=(224, 224), debug=False, augment=True):
        self.image_folder = image_folder
        self.annotations = annotations
        self.output_size = output_size
        self.debug = debug  # Enable/disable imshow debug mode
        self.transform = transforms.Compose([
            transforms.Resize(output_size),
            transforms.ToTensor()
        ])

        # Define possible rotation angles
        self.angles = [0, 90, 180, 270] if augment else [0]
        #self.angles = [0, 180]

    def __len__(self):
        # Each image produces 4 rotated versions
        return len(self.annotations) * len(self.angles)


    def __getitem__(self, idx):
        # Determine original image and rotation
        angle_idx = idx % len(self.angles)
        img_idx = idx // len(self.angles)
        angle = self.angles[angle_idx]

        filename, coords = self.annotations[img_idx]
        img_path = os.path.join(self.image_folder, filename)
        image = Image.open(img_path).convert("RGB")

        # --- Convert to numpy for ROI detection ---
        np_img = np.array(image)
        gray = np_img.mean(axis=2)  # average intensity

        # --- Threshold to find non-black pixels ---
        mask = gray > 30  # brightness threshold
        if not mask.any():
            # fallback to full image if object not found
            left, top, right, bottom = 0, 0, np_img.shape[1], np_img.shape[0]
        else:
            ys, xs = np.where(mask)
            top, bottom = ys.min(), ys.max()
            left, right = xs.min(), xs.max()

            # Optional: add padding to ROI
            pad = 10
            left = max(0, left - pad)
            top = max(0, top - pad)
            right = min(np_img.shape[1], right + pad)
            bottom = min(np_img.shape[0], bottom + pad)

        # --- Crop the image ---
        cropped_img = np_img[top:bottom, left:right, :]

        # --- Adjust label coordinates ---
        x1, y1, x2, y2 = coords
        x1_adj, y1_adj = x1 - left, y1 - top
        x2_adj, y2_adj = x2 - left, y2 - top

        # --- Clamp values inside ROI ---
        roi_width, roi_height = right - left, bottom - top
        x1_adj = np.clip(x1_adj, 0, roi_width)
        y1_adj = np.clip(y1_adj, 0, roi_height)
        x2_adj = np.clip(x2_adj, 0, roi_width)
        y2_adj = np.clip(y2_adj, 0, roi_height)



        # --- Rotate image and adjust coordinates ---
        image_pil = Image.fromarray(cropped_img)
        if angle != 0:
            image_pil = image_pil.rotate(angle, expand=True)  # rotate image

            # Update coordinates according to rotation
            if angle == 90:
                x1_adj, y1_adj = y1_adj, roi_width - x1_adj
                x2_adj, y2_adj = y2_adj, roi_width - x2_adj
                roi_width, roi_height = roi_height, roi_width
            elif angle == 180:
                x1_adj, y1_adj = roi_width - x1_adj, roi_height - y1_adj
                x2_adj, y2_adj = roi_width - x2_adj, roi_height - y2_adj
            elif angle == 270:
                x1_adj, y1_adj = roi_height - y1_adj, x1_adj
                x2_adj, y2_adj = roi_height - y2_adj, x2_adj
            # No change needed for 0°

        # --- DEBUG: Show rotated image with adjusted points ---   
        #  please turn off data shuffle "dataloader = DataLoader(dataset, batch_size=4, shuffle=True)"
        if self.debug:
            debug_img = np.array(image_pil)  # convert PIL to numpy for cv2
            cv2.circle(debug_img, (int(x1_adj), int(y1_adj)), 6, (0, 255, 0), -1)  # P1
            cv2.circle(debug_img, (int(x2_adj), int(y2_adj)), 6, (0, 0, 255), -1)  # P2
            cv2.putText(debug_img, "P1", (int(x1_adj) + 8, int(y1_adj) - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            cv2.putText(debug_img, "P2", (int(x2_adj) + 8, int(y2_adj) - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

            cv2.imshow(f"({angle} deg) Rotated ROI Debug ", debug_img)
            key = cv2.waitKey(0)
            cv2.destroyAllWindows()


        # --- Apply transforms ---
        image = self.transform(image_pil)

        # --- Scale coordinates to resized output ---
        x_scale = self.output_size[0] / roi_width
        y_scale = self.output_size[1] / roi_height
        target = torch.tensor([
            x1_adj * x_scale, y1_adj * y_scale,
            x2_adj * x_scale, y2_adj * y_scale
        ], dtype=torch.float32)

        return image, target
    
# ===== 3. Load Annotations =====
def load_annotations(image_folder, annotation_folder):
    image_files = glob.glob(os.path.join(image_folder, "combined_*.jpg"))
    annotations = []
    for img_path in image_files:
        img_filename = os.path.basename(img_path)
        base_id = img_filename.replace("combined_", "").replace(".jpg", "")
        p1_file = os.path.join(annotation_folder, f"P1_{base_id}.txt")
        p2_file = os.path.join(annotation_folder, f"P2_{base_id}.txt")

        if not os.path.isfile(p1_file) or not os.path.isfile(p2_file):
            print(f"Warning: Missing annotation for {img_filename}, skipping.")
            continue

        with open(p1_file, 'r') as f1:
            x1, y1 = map(float, f1.read().strip().split())
        with open(p2_file, 'r') as f2:
            x2, y2 = map(float, f2.read().strip().split())

        annotations.append((img_filename, [x1, y1, x2, y2]))

    print(f"Total loaded samples: {len(annotations)}")
    return annotations


# ===== 4. Training Script =====
def main():


    # --- Device setup ---
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f" Using device: {device}")
    if torch.cuda.is_available():
        print(f"   GPU name: {torch.cuda.get_device_name(0)}")


    # --- Folders ---
    train_img = "train_and_validate/90_10/train"
    train_ann = "train_and_validate/90_10/train_annotation"
    val_img = "train_and_validate/90_10/validate"
    val_ann = "train_and_validate/90_10/validate_annotation"

    # --- Load datasets ---
    train_annotations = load_annotations(train_img, train_ann)
    val_annotations = load_annotations(val_img, val_ann)

    train_dataset = AnchorPointDataset(train_img, train_annotations, augment=True)
    val_dataset = AnchorPointDataset(val_img, val_annotations, augment=False)

    train_loader = DataLoader(train_dataset, batch_size=4, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=4, shuffle=False)   # validation, does not need the data augmentation (rotation)

    # --- Model ---
    model = AnchorPointCNN().to(device)
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    # --- Logging setup ---
    date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    model_filename = f"anchor_point_cnn_dynamic_roi_validate_{date_str}.pth"
    log_filename = f"cnn_train_validate_{date_str}.txt"
    plot_filename = f"cnn_train_validate_{date_str}.png"

    # === Logging containers ===
    #epoch_losses = []
    train_losses, val_losses = [], []


    # --- Training Loop ---
    with open(log_filename, "w") as f:
        for epoch in range(100):
            model.train()
            running_loss = 0.0
            for images, targets in train_loader:
                images, targets = images.to(device), targets.to(device)
                optimizer.zero_grad()
                outputs = model(images)
                loss = criterion(outputs, targets)
                loss.backward()
                optimizer.step()
                running_loss += loss.item()

            avg_train_loss = running_loss / len(train_loader)
            train_losses.append(avg_train_loss)

            # --- Validation phase ---
            model.eval()
            val_loss_total = 0.0
            with torch.no_grad():
                for val_images, val_targets in val_loader:
                    val_images, val_targets = val_images.to(device), val_targets.to(device)
                    val_outputs = model(val_images)
                    vloss = criterion(val_outputs, val_targets)
                    val_loss_total += vloss.item()

            avg_val_loss = val_loss_total / len(val_loader)
            val_losses.append(avg_val_loss)

            # --- Log ---
            log_line = f"Epoch {epoch+1:03d} | Train Loss: {avg_train_loss:.4f} | Val Loss: {avg_val_loss:.4f}\n"
            print(log_line.strip())
            f.write(log_line)

    # --- Save Model ---
    torch.save(model.state_dict(), model_filename)
    print(f"Model saved to {model_filename}")


    plt.figure(figsize=(8, 5))
    plt.plot(range(1, len(train_losses)+1), train_losses, marker='o', label='Train Loss')
    plt.plot(range(1, len(val_losses)+1), val_losses, marker='s', label='Validation Loss')
    plt.title("Training & Validation Loss per Epoch")
    plt.xlabel("Epoch")
    plt.ylabel("Loss (MSE)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(plot_filename)
    plt.close()
    print(f"Loss curves saved to {plot_filename}")


if __name__ == "__main__":
    main()