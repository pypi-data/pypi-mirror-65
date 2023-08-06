import json
import time
import os.path as osp
import os
# import numpy as np
import SimpleITK as sitk

DEFAULT_DICOM_TAG = {
    "patientID": "0010|0020",
    "studyUID": "0020|000d",
    "seriesUID": "0020|000e",
    "customUID": "0008|103e",
    "instance_number": "0020|0013",
    "sop_instance_uid": "0008|0018"
}


def sitk_read_image(img_path, as_np=False):
    try:
        img = sitk.ReadImage(img_path)
        if as_np:
            img = sitk.GetArrayFromImage(img)
    except Exception:
        print("[Error] unable to load img_path")
        return None
    return img


def get_image_info(img_path, info=None):
    """
    read dicom tags and return their values as dict
    args:
        img_path (str): the image path
        info (dict{tag_name->tag_position})
    return:
        info_dict:  the dicom tag values, default is 'None'
    """
    parsing_tags = DEFAULT_DICOM_TAG.copy()
    if info is not None:
        parsing_tags.update(info)
    info_dict = {tag: None for tag in parsing_tags}
    if isinstance(img_path, sitk.Image):
        img_itk = img_path
    elif isinstance(img_path, str):
        if not osp.exists(img_path):
            print("[Error]image_path does not exist")
            return info_dict
        img_itk = sitk_read_image(img_path)
        if img_itk is None:
            return info_dict
    for tag, meta_key in parsing_tags.items():
        try:
            info_dict[tag] = img_itk.GetMetaData(meta_key).strip(" \n")
        except Exception:
            info_dict[tag] = None
    return info_dict


def make_dir(*args):
    """
    the one-liner directory creator
    """
    path = osp.join(*[arg.strip(" ") for arg in args])
    if not osp.isdir(path):
        from random import random

        time.sleep(random() * 0.001)
        if not osp.isdir(path):
            os.makedirs(path)
    return path


def copy_files(root_2d, output_dir, is_2d=True, do_copy=True, valid_patient_list=[]):
    info_name = "info2d.json" if is_2d else "info3d.json"
    patient_list = []
    for root, dirs, files in os.walk(root_2d):
        for filename in files:
            if not filename.endswith("dcm"):
                continue
            img_path = osp.join(root, filename)
            info = get_image_info(img_path)
            # token = (info["patientID"], info["studyUID"], info["seriesUID"])
            token = (info["patientID"], info["studyUID"])
            if len(valid_patient_list) > 0 and token not in valid_patient_list:
                continue
            # print(info["seriesUID"], valid_patient_list[token])
            patient_list.append(token)
            out_dir = osp.join(output_dir, info["patientID"])
            if do_copy:
                print(root)
                if not osp.exists(out_dir):
                    os.makedirs(out_dir)
                if is_2d:
                    out_path = osp.join(out_dir, info["customUID"])
                else:
                    out_path = osp.join(
                        out_dir, info["studyUID"])
                if not osp.exists(out_path):
                    os.symlink(root, out_path)

                info["src"] = root
                info["dst"] = out_path
                with open(info_name, "a") as f:
                    f.writelines([json.dumps(info), "\n"])
            break
    return patient_list


if __name__ == "__main__":
    #     root_2d = "/breast_data/cta/dicom/train00/"
    root_2d = "/data/disk3/xueguan_bankuai/coronary/train00/"
    root_3d = "/data/disk4/cor_cta/bt_587/dicom/"
    root_anno = "/data/disk3/xueguan_bankuai/coronary/zqy/anno_to_label"
    output_dir = "/data/disk3/xueguan_bankuai/coronary/zqy/axial_valid"
    # output_dir = "/data/disk3/xueguan_bankuai/coronary/zqy/test_label_full"
    # patient2d = copy_files(root_2d, output_dir, is_2d=True, do_copy=False)
    # patient3d = copy_files(root_3d, output_dir, is_2d=False, do_copy=False)
    # valid_patient_list = [p for p in patient3d if p in patient2d]

    valid_patient_list = {}
    for root, dirs, files in os.walk(root_anno):
        for filename in files:
            if filename.endswith(".json"):
                token = root.split("/")[-3:-1]
                valid_patient_list[tuple(token)] = root.split("/")[-1]
                break
    # print(valid_patient_list)

    copy_files(root_2d, output_dir, is_2d=True, do_copy = True,
               valid_patient_list=valid_patient_list)
    # copy_files(root_3d, output_dir, is_2d=False,
    #            valid_patient_list=valid_patient_list)
