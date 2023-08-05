from __future__ import absolute_import

__version__ = "0.1.3"

from deeptext.detect import detect_text as dt
from deeptext.recognize import recognize_text as rt

default_craft_params = {"cuda": False,
                        "mag_ratio": 0.8,
                        "refiner": True,
                        "crop_type": "box",
                        "rectify": True,
                        "export_extra": True}

default_filter_params = {"type": "none"}


# detect texts
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
    prediction_result = dt(image_path,
                           output_dir=output_dir,
                           detector=detector,
                           craft_params=craft_params,
                           filter_params=filter_params)

    # return prediction results
    return prediction_result


# recognize texts
def recognize_text(image_paths,
                   recognizer="tesseract-eng"):
    """
    Arguments:
        image_paths: list of paths to the images to be processed
        recognizer: model to be used as recognizer ["tesseract-eng, tesseract-tur"]
    """
    prediction_result = rt(image_paths=image_paths,
                           recognizer=recognizer)

    # return prediction results
    return prediction_result
