import PIL
import json
from PIL import Image
from typing import Dict, List


def shape_data(path: str) -> Dict[str, Dict[str, List[str]]]:
    """Shape data from 'res.json' file

    Args:
        path (str): The path to the 'res.json' file

    Returns:
        Dict[str, Dict[str, List[str]]]:
    """

    with open(path) as f:
        res = json.load(f)

    path_queries = sorted(res.keys())

    id_cows = [path_query.split("/")[-2] for path_query in path_queries]
    id_cows = sorted(set(id_cows), key=id_cows.index)

    anns = {}

    for id_cow in id_cows:
        top1, top2_5, top6_later = {}, {}, {}
        for path_query in path_queries:
            if id_cow == path_query.split("/")[-2]:
                id_dbs = [path_db.split("/")[-2] for path_db in res[path_query]]
                if id_cow == id_dbs[0]:
                    top1[path_query] = res[path_query]
                elif id_cow in id_dbs[:5]:
                    top2_5[path_query] = res[path_query]
                else:
                    top6_later[path_query] = res[path_query]

        anns[id_cow] = {"top1": top1, "top2_5": top2_5, "top6_later": top6_later}

    return anns


def pad_image(image: PIL.Image, bg_color=(0, 0, 0)):
    w, h = image.size
    if w == h:
        return image
    elif w > h:
        result = Image.new(image.mode, (w, w), bg_color)
        result.paste(image, (0, (w - h) // 2))
        return result
    else:
        result = Image.new(image.mode, (h, h), bg_color)
        result.paste(image, ((h - w) // 2, 0))
        return result