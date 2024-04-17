
import os
import shutil
from typing import List
import superannotate as sa
from superannotate import SAClient
import logging

class Download_json_superannotate:
    def __init__(self, sa_client: SAClient) -> None:
        self.sa_client: SAClient = sa_client
        
    def checking_status(
        self, project_list: List[str], sa_client: SAClient
    ) -> List[str]:
        
        self.sa_client = sa_client

        checked_project_list = []
        for lst in project_list:
            meta_status = self.sa_client.get_project_metadata(str(lst))
            project_status = meta_status["status"]
            if project_status == "Completed":
                checked_project_list.append(lst)

        return checked_project_list

    def move_files_to_root(self, directory: str) -> None:
        self.directory = directory
        for root, dirs, _ in os.walk(self.directory):
            for folder in dirs:
                if folder != "classes":
                    logging.info(os.path.join(self.directory , folder))
                    for file in os.listdir(os.path.join(self.directory , folder)):
                        file_path = os.path.join(self.directory, folder, file)
                        shutil.move(file_path, os.path.join(self.directory, file))
                    folder_path = os.path.join(root, folder)
                    # Check if the directory is empty
                    if not os.listdir(folder_path):  
                        os.rmdir(folder_path)


    def coco_conversion(self, final_project_list: List[str], directory: str) -> str:
        final_project_list = final_project_list
        self.directory = directory
        export_loc_list = []


        for lst in final_project_list:
            print(lst)

            prepare = self.sa_client.prepare_export(
                lst,
                folder_names=None,
                annotation_statuses=["Completed"],
                include_fuse=False,
                only_pinned=False,
            )
            export = prepare["name"]
            export_location = os.path.join(self.directory,lst)
            os.makedirs(export_location, exist_ok=True)

            data = self.sa_client.download_export(
                lst,
                export,
                export_location,
                extract_zip_contents=True,
                to_s3_bucket=None,
            )
            export_loc_list.append(export_location)
        for ex_loc in export_loc_list:

            self.move_files_to_root(ex_loc)

            os.makedirs(os.path.join(os.getcwd(),'coco_output_superann'), exist_ok=True)
            output_path =os.path.join(os.getcwd(), "coco_output_superann", f"{ex_loc.split(os.path.sep)[-1]}")

            sa.export_annotation(
                input_dir=ex_loc,
                output_dir = output_path,
                dataset_format="COCO",
                dataset_name=f"{ex_loc.split(os.path.sep)[-1]}",
                project_type="Vector",
                task="object_detection",
            )
            logging.info(f"Completed :----------------- {ex_loc.split(os.path.sep)[-1]}")
        return output_path
