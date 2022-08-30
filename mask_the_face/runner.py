import os
import random
import dlib
import cv2
import numpy as np

from argparse import Namespace
from typing import List, Tuple, Union
from imutils import face_utils
from PIL import Image

from mask_the_face.utils.aux_functions import (
    get_available_mask_types,
    shape_to_landmarks,
    rect_to_bb,
    mask_face,
    get_six_points,
)


class Runner(object):
    def __init__(self, dlib_model_dir: str) -> None:
        # check necessary input files
        path_to_dlib_model = os.path.join(
            dlib_model_dir, "shape_predictor_68_face_landmarks.dat"
        )
        if not os.path.exists(path_to_dlib_model):
            raise ValueError("dlib model file does not exists!!!")

        # Setup dlib face detector and predictor
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(path_to_dlib_model)
        return

    def _gen_args(
        self,
        mask_type: str,
        pattern: str,
        pattern_weight: float,
        color: str,
        color_weight: float,
        code: str,
    ) -> Namespace:
        # set input arguments (match original module's input)
        args = Namespace()
        args.path = ""
        args.mask_type = mask_type
        args.pattern = pattern
        args.pattern_weight = pattern_weight
        args.color = color
        args.color_weight = color_weight
        args.code = code
        args.verbose = False
        args.write_original_image = False
        args.feature = False
        args.write_path = "_masked"

        # Set up dlib face detector and predictor
        args.detector = self.detector
        args.predictor = self.predictor

        # Extract data from code
        mask_code = "".join(args.code.split()).split(",")
        args.code_count = np.zeros(len(mask_code))
        args.mask_dict_of_dict = {}

        for i, entry in enumerate(mask_code):
            mask_dict = {}
            mask_color = ""
            mask_texture = ""
            mask_type = entry.split("-")[0]
            if len(entry.split("-")) == 2:
                mask_variation = entry.split("-")[1]
                if "#" in mask_variation:
                    mask_color = mask_variation
                else:
                    mask_texture = mask_variation
            mask_dict["type"] = mask_type
            mask_dict["color"] = mask_color
            mask_dict["texture"] = mask_texture
            args.mask_dict_of_dict[i] = mask_dict
        return args

    # return: masked image list (BGR format) per 'mask_type'
    def run(
        self,
        image_path: Union[str, bytes, Image.Image],
        mask_type: str = "surgical",
        pattern: str = "",
        pattern_weight: float = 0.5,
        color: str = "#FFFFFF",
        color_weight: float = 0.5,
        code: str = "",
    ) -> Tuple[List[np.ndarray], List[str], List[np.ndarray], np.ndarray]:
        # setup args
        args = self._gen_args(
            mask_type, pattern, pattern_weight, color, color_weight, code
        )

        # Read the image
        if isinstance(image_path, str):
            image = cv2.imread(image_path)
        elif isinstance(image_path, bytes):
            image = cv2.imdecode(np.frombuffer(image_path, np.uint8), -1)
        elif isinstance(image_path, Image.Image):
            image = cv2.cvtColor(np.array(image_path), cv2.COLOR_RGB2BGR)
        else:
            raise ValueError("Bad input")

        # # setup args
        # args = copy.deepcopy(self.args)

        original_image = image.copy()
        # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = image
        face_locations = args.detector(gray, 1)
        mask_type = args.mask_type
        # verbose = args.verbose
        if args.code:
            ind = random.randint(0, len(args.code_count) - 1)
            mask_dict = args.mask_dict_of_dict[ind]
            mask_type = mask_dict["type"]
            args.color = mask_dict["color"]
            args.pattern = mask_dict["texture"]
            args.code_count[ind] += 1

        elif mask_type == "random":
            available_mask_types = get_available_mask_types()
            mask_type = random.choice(available_mask_types)

        # if verbose:
        #     tqdm.write("Faces found: {:2d}".format(len(face_locations)))

        # Process each face in the image
        masked_images = []
        mask_binary_array = []
        mask = []
        for (i, face_location) in enumerate(face_locations):
            shape = args.predictor(gray, face_location)
            shape = face_utils.shape_to_np(shape)
            face_landmarks = shape_to_landmarks(shape)
            face_location = rect_to_bb(face_location)
            # draw_landmarks(face_landmarks, image)
            six_points_on_face, angle = get_six_points(face_landmarks, image)
            mask = []
            if mask_type != "all":
                if len(masked_images) > 0:
                    image = masked_images.pop(0)
                image, mask_binary = mask_face(
                    image,
                    face_location,
                    six_points_on_face,
                    angle,
                    args,
                    type=mask_type,
                )

                # compress to face tight
                face_height = face_location[2] - face_location[0]
                face_width = face_location[1] - face_location[3]
                masked_images.append(image)
                mask_binary_array.append(mask_binary)
                mask.append(mask_type)
            else:
                available_mask_types = get_available_mask_types()
                for m in range(len(available_mask_types)):
                    if len(masked_images) == len(available_mask_types):
                        image = masked_images.pop(m)
                    img, mask_binary = mask_face(
                        image,
                        face_location,
                        six_points_on_face,
                        angle,
                        args,
                        type=available_mask_types[m],
                    )
                    masked_images.insert(m, img)
                    mask_binary_array.insert(m, mask_binary)
                mask = available_mask_types
                cc = 1

        return masked_images, mask, mask_binary_array, original_image

    def postprocess(self, masked_images: List[np.ndarray]) -> List[Image.Image]:
        return [
            Image.fromarray(cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB))
            for bgr_image in masked_images
        ]
