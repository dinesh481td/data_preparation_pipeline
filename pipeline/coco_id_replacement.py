
import json
import os
from typing import Dict, List, Union
import pandas as pd


class ReplaceIds:
    def __init__(self,reference_categories_id_json_path: str) -> None:
        
        with open(reference_categories_id_json_path,'r') as f:
            self.categories_id: List[Dict[str, Union[int, str]]] = json.load(f)
         
        

    def id_change_categories(
        self, json_data: Dict[str, List[Dict[str, Union[int, str]]]]
    ) -> Dict[str, List[Dict[str, Union[int, str]]]]:
        self.json_data = json_data

        for key in self.json_data.keys():
            # Replacing IDS in Annotations :-
            if key == "annotations":
                annotations = self.json_data[key]
                for annotation in annotations:
                    class_id = annotation.get("category_id")
                    class_names = [
                        i["name"]
                        for i in self.json_data["categories"]
                        if i["id"] == class_id
                    ]
                    if class_names:
                        replace_id, replace_name = [
                            (c["id"], c["name"])
                            for c in self.categories_id["categories"]
                            if c["name"] == class_names[0]
                        ][0]
                        if class_names[0] == replace_name:
                            annotation["category_id"] = replace_id

            # Replacing IDS in Categories :-
            if key == "categories":
                instances = self.json_data[key]
                for instance in instances:
                    class_names = instance.get("name")
                    if class_names:
                        class_id = instance.get("id")
                        replace_id, replace_name = [
                            (c["id"], c["name"])
                            for c in self.categories_id["categories"]
                            if c["name"] == class_names
                        ][0]
                        if class_names == replace_name:
                            instance["id"] = replace_id

        return self.json_data

    def write_replaced_json(self, folder_path: str) -> None:
        self.folder_path = folder_path

        with open(self.folder_path, "r") as f:
            json_data = json.load(f)

        replaced_json = self.id_change_categories(json_data)
        os.makedirs(os.path.join(os.getcwd(),'coco_final_jsons'), exist_ok=True)
        re_folder_path = os.path.basename(folder_path)
        output_path = os.path.join(os.getcwd(),'coco_final_jsons',f'Replaced_{re_folder_path}.json')

        with open(output_path, "w") as f:
            json.dump(replaced_json, f, indent=2)
