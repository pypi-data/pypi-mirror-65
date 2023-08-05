from deeptext.utils import filter_boxes_by_centroid_ratios, filter_by_box_intersection

default_craft_params = {"cuda": False,
                        "mag_ratio": 0.8,
                        "refiner": True,
                        "crop_type": "box",
                        "rectify": True,
                        "export_extra": True}

default_filter_params = {"type": "none"}


def detect_text(image_path,
                output_dir=None,
                detector="craft",
                craft_params=default_craft_params,
                filter_params=default_filter_params):
    """
    Arguments:
        image_path: path to the image to be processed
        output_dir: path to the results to be exported
        detector: model to be used as detector ["craft"]
        craft_params: parameters of the craft detector
        filter_params: parameters of the positional filter
    """
    # load image
    if detector == "craft":
        import craft_text_detector as craft
        image = craft.read_image(image_path)

    if detector == "craft":
        # load refiner if required
        if craft_params["refiner"]:
            refine_net = craft.load_refinenet_model()
        else:
            refine_net = None

    # perform prediction
    if detector == "craft":
        prediction_result = craft.get_prediction(image=image,
                                                 craft_net=craft.craft_net,
                                                 refine_net=refine_net,
                                                 text_threshold=0.7,
                                                 link_threshold=0.4,
                                                 low_text=0.4,
                                                 cuda=craft_params["cuda"],
                                                 canvas_size=1280,
                                                 mag_ratio=craft_params["mag_ratio"],
                                                 show_time=False)
        # arange regions
        if craft_params["crop_type"] == "box":
            crop_regions = prediction_result["boxes"]
            filter_regions = prediction_result["boxes_as_ratios"]
        elif craft_params["crop_type"] == "poly":
            crop_regions = prediction_result["polys"]
            filter_regions = prediction_result["polys_as_ratios"]
        else:
            raise TypeError("crop_type can be only 'polys' or 'boxes'")

    # filter boxes if filter params are given
    if filter_params["type"] != "none":
        if filter_params["type"] == "centroid":
            result = filter_boxes_by_centroid_ratios(filter_regions, filter_params)
        elif filter_params["type"] == "box":
            result = filter_by_box_intersection(filter_regions, filter_params)

        crop_regions = crop_regions[result["selected_box_indexes"]]
        prediction_result["filtered_box_indexes"] = result["selected_box_indexes"]

    # export if output_dir is given
    prediction_result["text_crop_paths"] = []
    if output_dir is not None:
        # export detected text regions
        exported_file_paths = craft.export_detected_regions(image_path=image_path,
                                                            image=image,
                                                            regions=crop_regions,
                                                            output_dir=output_dir,
                                                            rectify=craft_params["rectify"])
        prediction_result["text_crop_paths"] = exported_file_paths

        if detector == "craft":
            # export heatmap, detection points, box visualization
            if craft_params["export_extra"]:
                craft.export_extra_results(image_path=image_path,
                                           image=image,
                                           regions=crop_regions,
                                           heatmap=prediction_result["heatmap"],
                                           output_dir=output_dir)

    # return prediction results
    return prediction_result
