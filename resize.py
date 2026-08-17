from PIL import Image

# Change these paths
SOURCE = "Method/FLAIR/10.png"
REFERENCE = "Method/Ours/10.png"
OUTPUT = "Method/FLAIR/10.png"


# Get target dimensions from reference image
with Image.open(REFERENCE) as ref:
    target_size = ref.size

# Resize source image
with Image.open(SOURCE) as img:
    resized = img.resize(target_size, Image.Resampling.LANCZOS)
    resized.save(OUTPUT)

print(f"Resized {SOURCE}")
print(f"Target size: {target_size}")
print(f"Saved to: {OUTPUT}")