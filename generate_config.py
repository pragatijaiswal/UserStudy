import os
import json

IMAGES_DIR = "Method"
OUTPUT_JSON = "config.json"

IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".webp")


def find_images(folder):
    """Return sorted list of image files in folder."""
    files = []

    for f in os.listdir(folder):
        if f.lower().endswith(IMAGE_EXTS):
            files.append(f)

    # Numerical sorting: 1.png, 2.png, ..., 9.png, 10.png
    def sort_key(filename):
        name = os.path.splitext(filename)[0]

        if name.isdigit():
            return (0, int(name))

        return (1, name.lower())

    return sorted(files, key=sort_key)


subjects = []

if not os.path.isdir(IMAGES_DIR):
    raise FileNotFoundError(f"Folder not found: {IMAGES_DIR}")


# Find all method folders
methods_data = {}

for method in sorted(os.listdir(IMAGES_DIR)):

    method_path = os.path.join(IMAGES_DIR, method)

    if not os.path.isdir(method_path):
        continue

    images = find_images(method_path)

    if not images:
        print(f"WARNING: No images in {method}")
        continue

    print(f"\nProcessing {method}")

    for img_file in images:

        image_name = os.path.splitext(img_file)[0]

        if image_name not in methods_data:
            methods_data[image_name] = []

        rel_path = f"{method}/{img_file}"

        print(f"  {image_name}: {rel_path}")

        methods_data[image_name].append({
            "name": method,
            "file": rel_path
        })


# Sort subjects numerically
def subject_sort_key(name):
    if name.isdigit():
        return (0, int(name))

    return (1, name.lower())


for subject_name in sorted(methods_data.keys(), key=subject_sort_key):

    subjects.append({
        "name": subject_name,
        "methods": methods_data[subject_name]
    })


# Write JSON
with open(OUTPUT_JSON, "w") as f:
    json.dump(
        {"subjects": subjects},
        f,
        indent=2
    )

print(f"\nDone -> {OUTPUT_JSON} generated")
print(f"Found {len(subjects)} images/subjects")
