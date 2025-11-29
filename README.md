# Horse Breed Detection & Classification System (YOLOv9)

This project implements a **Two-Stage Object Detection and Classification System**. It utilizes **YOLOv9** to detect horses within images and a custom-trained **YOLOv5-cls** classifier to identify their specific breeds.

## 📁 Directory Structure

```text
.
├── data/
│   └── raw_images/          # [Source] Contains the original Kaggle images for 7 breeds
├── horsebreed/              # [Dataset] Generated Train/Val/Test splits (via horsebreed_prepare)
├── tools/
│   └── horsebreed_prepare.py # Script to split raw_images into the horsebreed dataset
├── yolov9-c-converted.pt    # Pre-trained YOLOv9 detection weights (COCO)
├── runs/
│   ├── train-cls/           # Classification training results (contains best.pt)
│   └── detect/              # Detection inference results (cropped images)
├── detect.py                # YOLOv9 detection script
├── classify/
│   ├── train.py             # Classification training script
│   └── predict.py           # Classification inference script
└── requirements.txt         # Project dependencies
```

## 🛠️ Installation & Environment

**Recommended Python Version:** 3.9

Due to compatibility issues between the latest NumPy 2.x and PyTorch/OpenCV, please follow these specific installation steps:

1.  **Install Base Requirements:**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Fix Version Conflicts (Crucial Step):**
    You must downgrade NumPy and OpenCV to compatible versions:

    ```bash
    pip install "numpy<2" "opencv-python<4.10" "opencv-python-headless<4.10"
    ```

3.  **Fix `tarfile` Error (If encountered):**
    If you see an `ImportError: cannot import name 'tarfile' from 'backports'`, run:

    ```bash
    pip install backports.tarfile
    ```

## 🚀 Usage Workflow

### Step 1: Data Preparation

If you haven't already generated the `horsebreed` folder from your `raw_images`, run the preparation tool:

```bash
python tools/horsebreed_prepare.py
```

  * **Input:** `data/raw_images/` (Contains subfolders for each breed)
  * **Output:** `horsebreed/` (Organized into `train`, `test`, `val`)

### Step 2: Train the Breed Classifier

Train the classifier using transfer learning (starting from `yolov5s-cls.pt`).

```bash
python classify/train.py --model yolov5s-cls.pt --data horsebreed --epochs 100 --img 224
```

  * **Result:** The best model weights will be saved to `runs/train-cls/exp/weights/best.pt`.

### Step 3: Inference (Detection + Classification)

You have two methods to run inference.

#### Method A: Integrated Pipeline (Recommended)

Use the custom script to detect, classify, and draw results directly on the image in one go.

```bash
python detect_and_classify.py
```

  * **Note:** Ensure you edit the `source` path in the script to point to your target image (e.g., `combined_7_horses.png`).

#### Method B: Two-Stage Manual Process

Run detection and classification separately.

1.  **Detect & Crop:**
    Extract horses from the image using YOLOv9.

    ```bash
    python detect.py \
      --weights yolov9-c-converted.pt \
      --source data/images/test_horse1.png \
      --classes 17 \
      --save-crop \
      --project runs/detect \
      --name horse_result
    ```

      * `--classes 17`: Restricts detection to "Horse" only (COCO index 17).
      * `--save-crop`: Saves the detected regions for the next step.

2.  **Classify Breeds:**
    Identify the breed of the cropped images.

    ```bash
    python classify/predict.py \
      --weights runs/train-cls/exp/weights/best.pt \
      --source runs/detect/horse_result/crops/horse \
      --save-txt
    ```

## 📊 Supported Breeds

The model is trained on the Kaggle Horse Breed Dataset and supports the following 7 classes:

1.  Akhal-Teke
2.  Appaloosa
3.  Arabian
4.  Friesian
5.  Orlov-Trotter
6.  Percheron
7.  Vladimir-Heavy-Draft

## 🔧 Troubleshooting

  * **RuntimeError: Numpy is not available** / **AttributeError: \_ARRAY\_API not found**:
    This confirms you have NumPy 2.x installed. Run the downgrade command in the Installation section.
  * **Memory Errors / Silent Exit on Mac**:
    If processing large composite images, the script might crash due to memory limits. Try resizing the input image to a smaller resolution (e.g., width 2000px).
