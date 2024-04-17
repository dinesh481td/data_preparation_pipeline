
import json
import os
import subprocess


class MergingJsons:
    def __init__(self, final_json_dir: str, merge_dir: str) -> None:
        self.final_json_dir = final_json_dir
        self.merge_dir = merge_dir

    def merge_json_files(self, input_files: str, output_file: str) -> None:
        command = ["python", "-m", "COCO_merger.merge", "--src"]
        
        command.extend(input_files)
        command.extend(["--out", output_file])
        
        return_subprocess = subprocess.run(['pip', 'show', 'COCO_merger'])
        
        if return_subprocess.returncode == 0:
            print("COCO_merger is installed.")
            subprocess.run(command, check=True)
        else:
            print("COCO_merger is not installed.")
            subprocess.run(['pip', 'install', 'COCO-merger'])  

    def json_reformat(self, merge_dir: str) -> str:
        
        json_files = os.listdir(merge_dir)
        last_json = sorted(json_files, key=lambda x: int(x.split(".")[0]))[-1]
        print("Last Json: ", last_json)
        json_file = json.load(open(os.path.join(merge_dir, last_json), "r"))

        json_object = json.dumps(json_file, indent=1)
        path_json = f'{last_json.split(".")[0]}_json_reformat.json'
        with open(f'{last_json.split(".")[0]}_json_reformat.json', "w") as outfile:
            outfile.write(json_object)
        return path_json

    def merger(self) -> str:
        json_files = [
            i for i in sorted(os.listdir(self.final_json_dir)) if i.endswith(".json")
        ]

        print(f"Found {len(json_files)} jsons")
        print(json_files)

        for index, i in enumerate(json_files):
            print(index, i)
            json_full_dir = os.path.join(self.final_json_dir, i)
            temp_merge_file = os.path.join(self.merge_dir, f"{index}.json")
            temp_merge_file_next = os.path.join(
                self.merge_dir, f"{index+1}.json"
            )
            print(temp_merge_file)
            print(json_full_dir)

            # Load JSON data from files
            with open(json_full_dir, "r") as json_file:
                json1_data = json.load(json_file)

            with open(temp_merge_file, "r") as json_file:
                json2_data = json.load(json_file)

            # Extract the set of file names from both JSONs
            file_names_json1 = {image["file_name"] for image in json1_data["images"]}
            file_names_json2 = {image["file_name"] for image in json2_data["images"]}

            # Find common file names (duplicates)
            common_file_names = file_names_json1.intersection(file_names_json2)

            # Remove images with common file names from the second JSON
            cleaned_images = [
                image
                for image in json2_data["images"]
                if image["file_name"] not in common_file_names
            ]
            cleaned_annotations = [
                ann
                for ann in json2_data["annotations"]
                if json2_data["images"][ann["image_id"]]["file_name"]
                not in common_file_names
            ]

            # Update the images and annotations in the second JSON
            json2_data["images"] = cleaned_images
            json2_data["annotations"] = cleaned_annotations

            # Save the cleaned JSON data
            with open("json_without_duplicates.json", "w") as json_file:
                json.dump(json2_data, json_file, indent=4)

            json2_data1 = os.path.join(os.getcwd(), "json_without_duplicates.json")
            self.merge_json_files([json_full_dir, json2_data1], temp_merge_file_next)

        Json_merged_path = self.json_reformat(self.merge_dir)
        return Json_merged_path
