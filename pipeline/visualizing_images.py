import json
import os
import cv2
import pandas as pd


def bounding_box(ann_folder_path: str, img_folder_path: str, json_path: str) -> None:
    # Reading the images from the folder
    images_files = os.listdir(img_folder_path)
    len(images_files)

    # Reading the JSON file
    f = open(json_path)
    data = json.load(f)

    # Displaying only the keys in the JSON
    data.keys()

    image_d = data.get("images")
    annot_d = data.get("annotations")

    id_lst_img = []
    filename_lst_img = []
    for i in range(len(image_d)):
        id_lst_img.append(image_d[i]["id"])
        filename_lst_img.append(image_d[i]["file_name"])

    id_annot = []
    bbox_coord = []
    class_names = []
    for i in range(len(annot_d)):
        id_annot.append(annot_d[i]["image_id"])
        bbox_coord.append(annot_d[i]["bbox"])
        class_names.append(annot_d[i]["category_id"])

    img_df = pd.DataFrame(columns=["Image_id", "File_name"])
    img_df["Image_id"] = id_lst_img
    img_df["File_name"] = filename_lst_img
    

    annot_df = pd.DataFrame(columns=["Image_id", "bboxs", "class_names"])
    annot_df["Image_id"] = id_annot
    annot_df["bboxs"] = bbox_coord
    annot_df["class_names"] = class_names

    # Joining the two Datasets on Image ID

    new_df = annot_df.merge(img_df, on=["Image_id"], how="left")
    

    file_n = []
    for file in new_df["File_name"]:
        file_n.append(file)
    new_df["modified_filename"] = file_n
    

    annotated_img_c2 = []
    count_2 = []

    grouped_df = new_df.groupby("modified_filename")

    if not os.path.exists(ann_folder_path):
        os.mkdir(ann_folder_path)

    for img in images_files:
        if img in grouped_df.groups:
            grouped_df2 = grouped_df.get_group(img)
            grouped_df2 = grouped_df2.reset_index(drop=True)
            images = cv2.imread(os.path.join(img_folder_path, img))

            for i in range(len(grouped_df2)):
                if images is not None:
                    xmin, ymin, width, height = grouped_df2["bboxs"][i]
                    cv2.rectangle(
                        images,
                        (int(xmin), int(ymin)),
                        (int(xmin + width), int(ymin + height)),
                        (255, 0, 0),
                        1,
                    )
                    # Find the corresponding category ID for the current annotation
                    category_id = grouped_df2["class_names"][i]

                    # Extract the class name for the given category ID
                    cls_name = [
                        str(cat["name"])
                        for cat in data["categories"]
                        if cat["id"] == category_id
                    ]

                    cls_names_str = ", ".join(cls_name)
                    cv2.putText(
                        images,
                        cls_names_str,
                        (int(xmin), int(ymin) - 5),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,  # Font scale
                        (255, 0, 0),  # Text color
                        1,  # Text thickness
                        cv2.LINE_AA,
                    )
                    annotated_img_c2.append(img)
                    count_2.append(len(grouped_df2))
                    cv2.imwrite(
                        os.path.join(ann_folder_path, f"{img}_annotated.jpg"), images
                    )
            else:
                print(f"Warning: No annotations found for image {img}")
