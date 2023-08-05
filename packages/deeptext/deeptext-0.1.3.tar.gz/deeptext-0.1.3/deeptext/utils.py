import numpy as np
from shapely.geometry import Point, Polygon


def order_points(pts):
    pts = np.array(pts, dtype="float32")
    # initialzie a list of coordinates that will be ordered
    # such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the
    # bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype="float32")
    # the top-left point will have the smallest sum, whereas
    # the bottom-right point will have the largest sum
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    # now, compute the difference between the points, the
    # top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    # return the ordered coordinates
    return rect


def get_box_centroids(regions):
    """
    Calculates centroid coords of the given polys/boxes.

    boxes: np.array([[[3,2],[5,4],[3,5],[2,1]],
                     [[3,2],[5,4],[3,5],[2,1]],
                     [[3,2],[5,4],[3,5],[2,1]]])

    centroids_as_ratios: [(0.13,0.3),(0.13,0.3),(0.13,0.3)]
    """
    centroids_as_ratios = []
    for region in regions:
        centroid_coord_tuple = Polygon(region).centroid.coords[:][0]
        centroids_as_ratios.append(centroid_coord_tuple)

    return {"centroids_as_ratios": centroids_as_ratios}


def filter_by_centroid_ratios(boxes, centroids_as_ratios, filter_params):
    """
    Filters the given centroid ratios based using filter params, and returns
    a list of indexes of selected boxes.

    boxes: np.array([[[3,2],[5,4],[3,5],[2,1]],
                     [[3,2],[5,4],[3,5],[2,1]],
                     [[3,2],[5,4],[3,5],[2,1]]])

    centroids_as_ratios = [(0.13,0.3),(0.13,0.3),(0.13,0.3)]

    filter_params = {"centers": [[0.1,0.3], [0.2,0.4]], "marigin_x": 0.1, "marigin_y": 0.05}
    """
    filter_ctrs = filter_params["centers"]
    filter_mrg_x = filter_params["marigin_x"]
    filter_mrg_y = filter_params["marigin_y"]
    selected_box_indexes = []
    for ind, centroid_as_ratios in enumerate(centroids_as_ratios):
        for filter_ctr in filter_ctrs:
            filter_box = Polygon([[filter_ctr[0] - filter_mrg_x, filter_ctr[1] - filter_mrg_y],
                                 [filter_ctr[0] + filter_mrg_x, filter_ctr[1] - filter_mrg_y],
                                 [filter_ctr[0] + filter_mrg_x, filter_ctr[1] + filter_mrg_y],
                                 [filter_ctr[0] - filter_mrg_x, filter_ctr[1] + filter_mrg_y]])
            if filter_box.contains(Point(centroid_as_ratios)):
                selected_box_indexes.append(ind)

    return selected_box_indexes


def filter_by_box_intersection(boxes, filter_params):
    """
    Filters the given centroid ratios using filter params, and returns a list
    of indexes of selected boxes.

    min_intersection_ratio: btw 0 and 1

    boxes: np.array([[[3,2],[5,4],[3,5],[2,1]],
                     [[3,2],[5,4],[3,5],[2,1]],
                     [[3,2],[5,4],[3,5],[2,1]]])

    filter_params = {"boxes": [[[3,2],[5,4],[3,5],[2,1]],
                               [[3,2],[5,4],[3,5],[2,1]]],
                     "marigin_x": 0.1,
                     "marigin_y": 0.05,
                     "min_intersection_ratio": 0.9}
    """
    filter_boxes = filter_params["boxes"]
    filter_mrg_x = filter_params["marigin_x"]
    filter_mrg_y = filter_params["marigin_y"]
    min_intersection_ratio = filter_params["min_intersection_ratio"]
    selected_box_indexes = []
    for ind, box in enumerate(boxes):
        #box = order_points(box)
        for filter_box in filter_boxes:
            #filter_box = order_points(filter_box)
            box = Polygon(box)
            filter_box = Polygon([[filter_box[0][0] - filter_mrg_x, filter_box[0][1] - filter_mrg_y],
                                 [filter_box[1][0] + filter_mrg_x, filter_box[1][1] - filter_mrg_y],
                                 [filter_box[2][0] + filter_mrg_x, filter_box[2][1] + filter_mrg_y],
                                 [filter_box[3][0] - filter_mrg_x, filter_box[3][1] + filter_mrg_y]])
            # calculate intersection ratio
            intersection_ratio = round(filter_box.intersection(box).area/box.area, 2)
            # filter out if smaller than min ratio
            if intersection_ratio >= min_intersection_ratio:
                selected_box_indexes.append(ind)

    return {"selected_box_indexes": selected_box_indexes}


def filter_boxes_by_centroid_ratios(boxes, filter_params):
    """
    Filters the given centroid ratios using filter params, and returns a list
    of indexes of selected boxes.

    boxes: np.array([[[3,2],[5,4],[3,5],[2,1]],
                     [[3,2],[5,4],[3,5],[2,1]],
                     [[3,2],[5,4],[3,5],[2,1]]])

    centroid_ratios = [(0.13,0.3),(0.13,0.3),(0.13,0.3)]

    filter_params = {"centers": [(0.1,0.3), (0.2,0.4)], "marigin_x": 0.1, "marigin_y": 0.05}
    """
    result = get_box_centroids(boxes)
    selected_box_indexes = filter_by_centroid_ratios(boxes, result["centroids_as_ratios"], filter_params)

    return {"selected_box_indexes": selected_box_indexes, "centroids_as_ratios": result["centroids_as_ratios"]}


if __name__ == "__main__":
    import craft_text_detector as craft
    # image path
    image_path = "data/idcard.png"
    # detect texts
    prediction_result = craft.detect_text(image_path=image_path, mag_ratio=0.8)
    # get boxes
    boxes = prediction_result["boxes_as_ratio"]
    # test filter_boxes_by_centroid_ratios
    filter_params = {"centers": [[0.49, 0.08]], "marigin_x": 0.1, "marigin_y": 0.05}
    filter_params = {"centers": [[0.44, 0.49]], "marigin_x": 0.08, "marigin_y": 0.05}
    selected_boxes = filter_boxes_by_centroid_ratios(boxes, filter_params)
    # test filter_by_box_coverage
    filter_params = {"boxes": [[[0.1460197 , 0.0395937 ],
                               [0.84171425, 0.05356989],
                               [0.84125618, 0.10991851],
                               [0.14556163, 0.09594232]]],
                     "marigin_x": 0.05,
                     "marigin_y": 0.05}
    selected_box_indexes = filter_by_box_intersection(boxes, filter_params, min_intersection_ratio=0.99)
