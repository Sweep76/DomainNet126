"""
Convert DomainNet (https://ai.bu.edu/M3SDA/) to DomainNet126
See paper: Semi-supervised Domain Adaptation via Minimax Entropy
"""


def parse_txt(s):
    """
    parse string like clipart/rabbit/clipart_236_000037.jpg 91
    """
    s = s.strip()
    prefix,class_index = s.split(" ")
    class_index = int(class_index)
    domain,class_name,img_name = prefix.split("/")
    return domain,class_name,img_name,class_index


def read_txt(txt_file:str):
    with open(txt_file,"r") as f:
        lines = f.readlines()
    return lines


if __name__ == "__main__":
    import os
    import shutil
    import argparse
    from tqdm import tqdm

    parser = argparse.ArgumentParser(description="convert")
    parser.add_argument("--raw_data_path", type=str,default="./image_list")
    parser.add_argument("--output_path",type=str,default="./")
    args = parser.parse_args()
    
    output_domain_list = ["clipart","painting","real","sketch"]

    for domain in output_domain_list:
        txt_file_path = f"./{domain}_list.txt"
        image_list = read_txt(txt_file_path)
        image_list = [parse_txt(s) for s in image_list]
        
        # copy file to output path
        output_path = f"{args.output_path}/{domain}"
        for image in tqdm(image_list):
            _class,_img = image[1],image[2]
            raw_path = f"{args.raw_data_path}/{domain}/{_class}/{_img}"
            target_path = f"{output_path}/{_class}"
            os.makedirs(target_path,exist_ok=True)
            shutil.copy2(raw_path,f"{target_path}/{_img}")
