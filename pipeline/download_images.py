import json
import os
import random
from typing import List
from google.cloud import storage
from superannotate import SAClient


def download_images_all(
    final_json_path: str, project_list: List[str], sample_size: int,bucket_name:str,sa_client: SAClient,storage_client_creds:str,download_all_images_folder_path:str
) -> None:
    with open(final_json_path, "r") as f:
        json_data = json.load(f)

    json_image_names = json_data["images"]
    json_image_names = random.sample(json_image_names, sample_size)

    for file in json_image_names:
        print(file["file_name"])
        file_name = file["file_name"]


        completed_project_list = sa_client.search_projects(status="Completed")

        final_list = [i for i in project_list if i in completed_project_list]


        storage_client = storage.Client.from_service_account_json(storage_client_creds)
        gcp_bucket = storage_client.bucket(bucket_name)

        for item in final_list:
            print(item)
            search_result = sa_client.search_items(
                project=item, name_contains=file_name, recursive=True
            )
        image_name = search_result[0]["name"]
        image_project_name = search_result[0]["path"]
        destination_file_name = os.path.join(download_all_images_folder_path, file_name)
        img_gcp_url = search_result[0]["url"]

        blob = gcp_bucket.blob(img_gcp_url)

        with open(destination_file_name, "wb") as f:
            blob.download_to_file(f)
