import os
import shutil
import download_images
import superannotate as sa
import visualizing_images as vm
from coco_id_replacement import ReplaceIds
from download_completed_project import Download_json_superannotate
from multi_json_merger import MergingJsons
from superannotate import SAClient

api_key = "api-key here"

sa_client = SAClient(api_key)

sample_size = 10

project_list = ["test_1","test_2"]


def __main__() -> None:
    directory = os.path.join(os.getcwd(),"jsons_superann")
    os.makedirs(directory, exist_ok=True)
    download = Download_json_superannotate(sa_client)

    final_project_list = download.checking_status(project_list, sa_client)
    coco_path = download.coco_conversion(final_project_list, directory)
    replacer = ReplaceIds(os.path.join(os.getcwd(),"merged_jsons","0.json"))
    for folders_names in os.listdir(os.path.join(os.getcwd(),"coco_output_superann")):
        for file_name in os.listdir(os.path.join(os.getcwd(),"coco_output_superann",folders_names)):    
            if file_name.endswith(".json"):
                print(file_name)
                replacer.write_replaced_json(
                    os.path.abspath(os.path.join("coco_output_superann", folders_names,file_name))
                )
                print()
                print(
                    f"--------------------------------  Replacement completed for {file_name} -------------------------------------"
                )

    final_json_dir = os.path.join(os.getcwd(),"coco_final_jsons")
    mrg_merge_dir = os.path.join(os.getcwd(),"merged_jsons")
    merger = MergingJsons(final_json_dir, mrg_merge_dir)
    json_merged_path = merger.merger()
    os.makedirs(os.path.join(os.getcwd(),"all_images"), exist_ok=True)
    os.makedirs(os.path.join(os.getcwd(),"ann_folder"), exist_ok=True)
    final_json_path = os.path.join(os.getcwd(), json_merged_path)
    download_images.download_images_all(final_json_path, final_project_list, sample_size,"super_annotate_demo",sa_client,os.path.join(os.getcwd(),"credentials","keyfile.json"),os.path.join(os.getcwd(),"all_images"))

    vm.bounding_box("ann_folder", "all_images", json_merged_path)


if __name__ == "__main__":
    __main__()