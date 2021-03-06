import cv2
from cv2 import xfeatures2d as non_free
import math
import numpy as np


class BagOfFeaturesTransform:
    def __init__(self, **kwargs):
        """
        Utilizes the visual bag of words algorithm to map image_file to feature vectors
        for the one-class SVM classifier.

        Process:
            - Partition each image into a grid and generate SURF descriptor from each patch
            - Compute K clusters from all of the features from all of the image_file (visual bag of words)
            - Construct normalized histogram for each image
            - Feature vector is then the values of the normalized histogram (vector quantization)

        :param kwargs:
            - num_clusters: (Integer) Size of the visual bag of words
            - patch_size: (Integer) size of patch to compute a descriptor
        """

        self._patch_size = kwargs.pop("patch_size", 16)
        self._num_clusters = kwargs.pop("num_clusters", 500)
        self._clusters = None
        self._img_descriptor_mapper = None

        return

    def initialize(self, image_data):
        """
        Initializes the bag of words descriptor and returns the mapped results of image_data

        :param image_data: ndarray [n, 3D image]
        :return: list [label, [1D image descriptor]]
        """
        termination_criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.1)
        bow_model = cv2.BOWKMeansTrainer(self._num_clusters, termination_criteria)

        key_point_tensor = {}
        for i in range(image_data.shape[0]):
            cv_image = image_data[i]
            descriptors, key_points = BagOfFeaturesTransform.extract_features_descriptors(cv_image, self._patch_size)

            key_point_tensor[i] = key_points
            bow_model.add(descriptors[1])

        self._clusters = bow_model.cluster()

        self._img_descriptor_mapper = cv2.BOWImgDescriptorExtractor(non_free.SURF_create(extended=True),
                                                                    cv2.FlannBasedMatcher_create())
        self._img_descriptor_mapper.setVocabulary(self._clusters)

        training_x = []
        for img_idx, img_descriptors in key_point_tensor.items():
            image_quantized_descriptor = self._img_descriptor_mapper.compute(image_data[img_idx], img_descriptors)
            training_x.append(image_quantized_descriptor)

        return np.vstack(training_x)

    def get_image_descriptor(self, cv_image):
        """
        Compute quantized image descriptor based on bag of features of the training data

        :param cv_image: (string) path to the image
        :return: (ndarray) numpy array
        """

        key_points = BagOfFeaturesTransform.extract_features(cv_image, self._patch_size)
        return self._img_descriptor_mapper.compute(cv_image, key_points)

    @staticmethod
    def extract_features_descriptors(image, patch_size=16):
        """
        Computes features based on the patch size

        :param image: input cv2 image
        :param patch_size: size of the patches in the grid
        :return: list of SURF descriptors
        """

        key_points = BagOfFeaturesTransform.extract_features(image, patch_size)

        surf = non_free.SURF_create(extended=True)
        descriptors = surf.compute(image, key_points)

        return descriptors, key_points

    @staticmethod
    def extract_features(image, patch_size=16):
        key_points = []
        blob_size = int(math.floor(patch_size / 2))

        start_loc = blob_size
        for x_loc in range(start_loc, image.shape[1], patch_size):
            for y_loc in range(start_loc, image.shape[0], patch_size):
                key_points.append(cv2.KeyPoint(x_loc, y_loc, blob_size))

        # note~ DEBUG CODE
        # key_point_image = cv2.drawKeypoints(image, key_points, None)
        # cv2.imshow("none", key_point_image)
        # cv2.waitKey(0)
        # kp, desc = surf.detectAndCompute(image, None)

        return key_points

    @staticmethod
    def read_image(image_file, resize_image=()):
        """
        Read an image and resize it, if necessary

        :param image_file: absolute image path
        :param resize_image: (x, y) tuple for new image dimensions
        :return: cv2 image
        """

        cv_image = cv2.imread(image_file)

        if cv_image is None:
            raise RuntimeError(f"Unable to open {image_file}")

        if len(resize_image) > 0:
            cv_image = cv2.resize(cv_image, resize_image)

        return cv_image
