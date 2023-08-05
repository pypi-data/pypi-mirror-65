import cv2


def recognize_text(image_paths,
                   recognizer="tesseract-eng"):
    """
    Arguments:
        image_paths: list of paths to the images to be processed
        recognizer: model to be used as recognizer ["tesseract-eng, tesseract-tur"]
    """
    recognized_texts = []
    for image_path in image_paths:
        # if tesseract
        if "tesseract" in recognizer:
            import pytesseract as pyt
            # read image
            image = cv2.imread(image_path)
            # arrange config
            lang_code = recognizer.split("-")[-1]
            custom_config = r'--oem 3 --psm 7'
            if lang_code != "":
                custom_config += ' -l {}'.format(lang_code)
            # recognize texts
            recognized_text = pyt.image_to_string(image, config=custom_config)
            recognized_texts.append(recognized_text)

    prediction_result = {"recognized_texts": recognized_texts}
    # return prediction results
    return prediction_result
