import os
import json

IMAGES_DIR = "Method"
OUTPUT_JSON = "config.json"

IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".webp")


def find_images(folder):
    files = [
        f for f in os.listdir(folder)
        if f.lower().endswith(IMAGE_EXTS)
    ]

    def sort_key(filename):
        name = os.path.splitext(filename)[0]

        if name.isdigit():
            return (0, int(name))

        return (1, name.lower())

    return sorted(files, key=sort_key)


if not os.path.isdir(IMAGES_DIR):
    raise FileNotFoundError(
        f"Folder not found: {IMAGES_DIR}"
    )


subjects_data = {}

for method in sorted(os.listdir(IMAGES_DIR)):

    method_path = os.path.join(IMAGES_DIR, method)

    if not os.path.isdir(method_path):
        continue

    images = find_images(method_path)

    if not images:
        print(f"WARNING: No images found in {method}")
        continue

    for filename in images:

        subject = os.path.splitext(filename)[0]

        if not subject.isdigit():
            continue

        if subject not in subjects_data:
            subjects_data[subject] = []

        relative_path = os.path.join(
            IMAGES_DIR,
            method,
            filename
        ).replace("\\", "/")

        subjects_data[subject].append({
            "name": method,
            "file": relative_path
        })


subjects = []

for subject in sorted(
    subjects_data.keys(),
    key=lambda x: int(x)
):

    subjects.append({
        "name": subject,
        "methods": subjects_data[subject]
    })


with open(OUTPUT_JSON, "w") as f:
    json.dump(
        {"subjects": subjects},
        f,
        indent=2
    )


print(
    f"Generated {OUTPUT_JSON} "
    f"with {len(subjects)} subjects."
)