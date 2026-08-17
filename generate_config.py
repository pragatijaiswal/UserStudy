import os
import json

IMAGES_DIR = "Method"
OUTPUT_JSON = "config.json"

IMAGE_EXTS = (".png", ".jpg", ".jpeg", ".webp")

INPUT_MASK_NAME = "Input+Mask"


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

    print(f"\nProcessing {method}")

    for filename in images:

        subject = os.path.splitext(filename)[0]

        if not subject.isdigit():
            continue

        if subject not in subjects_data:
            subjects_data[subject] = {
                "input_mask": None,
                "methods": []
            }

        relative_path = os.path.join(
            IMAGES_DIR,
            method,
            filename
        ).replace("\\", "/")


        # ============================
        # INPUT + MASK
        # ============================

        if method.lower() == INPUT_MASK_NAME.lower():

            subjects_data[subject]["input_mask"] = relative_path

            print(
                f"  Input+Mask: {relative_path}"
            )

        else:

            subjects_data[subject]["methods"].append({
                "name": method,
                "file": relative_path
            })

            print(
                f"  Method: {method} -> {relative_path}"
            )


subjects = []


for subject in sorted(
    subjects_data.keys(),
    key=lambda x: int(x)
):

    data = subjects_data[subject]

    if data["input_mask"] is None:
        print(
            f"WARNING: No Input+Mask for Subject {subject}"
        )

    if not data["methods"]:
        print(
            f"WARNING: No methods for Subject {subject}"
        )
        continue

    subjects.append({
        "name": subject,
        "input_mask": data["input_mask"],
        "methods": data["methods"]
    })


with open(OUTPUT_JSON, "w") as f:

    json.dump(
        {"subjects": subjects},
        f,
        indent=2
    )


print("\n================================")
print("config.json generated")
print("================================")
print(f"Subjects: {len(subjects)}")