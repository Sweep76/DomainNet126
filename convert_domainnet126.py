"""
Convert DomainNet (https://ai.bu.edu/M3SDA/) to DomainNet126
See paper: Semi-supervised Domain Adaptation via Minimax Entropy
"""

from pathlib import Path
from typing import List, Tuple


def parse_txt(line: str) -> Tuple[str, str, str, int]:
    """
    Parses a line like: clipart/rabbit/clipart_236_000037.jpg 91
    Returns: domain, class_name, image_name, class_index
    """
    prefix, class_index = line.strip().split(" ")
    class_index = int(class_index)
    domain, class_name, image_name = prefix.split("/")
    return domain, class_name, image_name, class_index


def read_txt(txt_file: str) -> List[str]:
    with open(txt_file, "r") as f:
        return [line.strip() for line in f if line.strip()]


if __name__ == "__main__":
    import argparse
    from tqdm import tqdm
    import shutil

    parser = argparse.ArgumentParser(description="Convert DomainNet to DomainNet126.")
    parser.add_argument("--raw_data_path", type=str, default="./image_list", help="Path to raw image folders.")
    parser.add_argument("--output_path", type=str, default="./", help="Output root directory.")
    args = parser.parse_args()

    output_domains = ["clipart", "painting", "real", "sketch"]

    for domain in output_domains:
        txt_path = Path(f"./{domain}_list.txt")
        if not txt_path.exists():
            print(f"[WARNING] File not found: {txt_path}")
            continue

        output_base = Path(args.output_path) / domain
        raw_base = Path(args.raw_data_path) / domain

        lines = read_txt(str(txt_path))
        parsed = [parse_txt(line) for line in lines]

        for domain_name, class_name, image_name, _ in tqdm(parsed, desc=f"Copying {domain}"):
            src = raw_base / class_name / image_name
            dest_dir = output_base / class_name
            dest = dest_dir / image_name

            try:
                dest_dir.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dest)
            except FileNotFoundError:
                print(f"[ERROR] File not found: {src}")
            except Exception as e:
                print(f"[ERROR] Failed to copy {src} to {dest}: {e}")
