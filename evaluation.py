import argparse
import os
import glob
import cv2
import numpy as np

def restore_semiconductor_image(img_path):
    # 1. Load image as grayscale (Single channel as requested by problem statement)
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None

    # 2. Speckle/Gaussian Noise Removal using Bilateral Filtering
    # This preserves structural edges of the wafer while smoothing out grain/noise
    denoised = cv2.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)

    # 3. Spatial Resolution Reduction Fix (Super-Resolution Upscaling)
    # If the image is downsampled (256x256 or 128x128), upscale it back to 512x512
    h, w = denoised.shape[:2]
    if h != 512 or w != 512:
        restored = cv2.resize(denoised, (512, 512), interpolation=cv2.INTER_CUBIC)
    else:
        restored = denoised

    return restored

def main():
    parser = argparse.ArgumentParser(description="KLA Benchmarking Evaluation Script")
    parser.add_argument('--input_dir', type=str, required=True, help='Path to test images')
    parser.add_argument('--output_dir', type=str, required=True, help='Path to output directory')
    args = parser.parse_args()

    print(f"Loading input verification data from: {args.input_dir}")
    os.makedirs(args.output_dir, exist_ok=True)

    # Grab all target images
    extensions = ('*.png', '*.jpg', '*.jpeg', '*.bmp')
    image_files = []
    for ext in extensions:
        image_files.extend(glob.glob(os.path.join(args.input_dir, ext)))

    print(f"Total validation frames found: {len(image_files)}")

    # Execute actual processing loop over the benchmark set
    for idx, img_path in enumerate(image_files):
        filename = os.path.basename(img_path)
        restored_img = restore_semiconductor_image(img_path)

        if restored_img is not None:
            out_path = os.path.join(args.output_dir, filename)
            cv2.imwrite(out_path, restored_img)

    print("Evaluation run completed. All verification output channels fully mapped.")

if __name__ == '__main__':
    main()
