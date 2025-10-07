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
    def __init__(self, image_folder, annotations, output_size=(224, 224), debug=False):
        self.image_folder = image_folder
        self.annotations = annotations
        self.output_size = output_size
        self.debug = debug  # Enable/disable imshow debug mode
        self.transform = transforms.Compose([
            transforms.Resize(output_size),
            transforms.ToTensor()
        ])

    def __len__(self):
        return len(self.annotations)

    def __getitem__(self, idx):
        filename, coords = self.annotations[idx]
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

        # --- Debug visualization ---
        if self.debug:
            debug_img = cropped_img.copy()
            cv2.circle(debug_img, (int(x1_adj), int(y1_adj)), 6, (0, 255, 0), -1)  # Green for P1
            cv2.circle(debug_img, (int(x2_adj), int(y2_adj)), 6, (0, 0, 255), -1)  # Red for P2
            cv2.putText(debug_img, "P1", (int(x1_adj) + 8, int(y1_adj) - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            cv2.putText(debug_img, "P2", (int(x2_adj) + 8, int(y2_adj) - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

            cv2.imshow("ROI Debug", debug_img)
            key = cv2.waitKey(0)
            if key == 27:  # Press ESC to quit early
                cv2.destroyAllWindows()
                exit(0)

        # --- Convert cropped image back to PIL for transforms ---
        image = Image.fromarray(cropped_img)
        image = self.transform(image)

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
    image_folder = "for_cnn_training_combined_from_dema"
    annotation_folder = "for_cnn_training_points_from_dema"

    annotations = load_annotations(image_folder, annotation_folder)
    dataset = AnchorPointDataset(image_folder, annotations)
    dataloader = DataLoader(dataset, batch_size=4, shuffle=True)

    model = AnchorPointCNN()
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    # === Add date suffix ===
    date_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    model_filename = f"anchor_point_cnn_dynamic_roi_{date_str}.pth"
    log_filename = f"cnn_train_{date_str}.txt"
    plot_filename = f"cnn_train_{date_str}.png"

    # === Logging containers ===
    epoch_losses = []

    with open(log_filename, "w") as f:
        for epoch in range(100):
            running_loss = 0.0
            for images, targets in dataloader:
                optimizer.zero_grad()
                outputs = model(images)
                loss = criterion(outputs, targets)
                loss.backward()
                optimizer.step()
                running_loss += loss.item()

            avg_loss = running_loss / len(dataloader)
            epoch_losses.append(avg_loss)

            #print(f"Epoch {epoch+1} | Loss: {running_loss / len(dataloader):.4f}")
            # Print and log
            log_line = f"Epoch {epoch+1} | Loss: {avg_loss:.4f}\n"
            print(log_line.strip())
            f.write(log_line)
    

    # Save model
    torch.save(model.state_dict(), model_filename)
    print(f"Model saved to {model_filename}")


    # === Plot Epoch vs. Average Loss ===
    plt.figure(figsize=(8,5))
    plt.plot(range(1, len(epoch_losses)+1), epoch_losses, marker='o', linewidth=2)
    plt.title("Training Loss per Epoch")
    plt.xlabel("Epoch")
    plt.ylabel("Average Training Loss")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(plot_filename)
    plt.close()
    print(f"Loss curve saved to {plot_filename}")

if __name__ == "__main__":
    main()