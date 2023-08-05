# import logging
# import os
#
# import cv2
# import joblib
# import numpy as np
#
# from face_engine import RESOURCES
#
#
# class SpoofDetector(PluginModel):
#     """Spoof detector object"""
#
#     suffix = '_spoof_detector'
#
#     def is_spoof(self, image, threshold):
#         """Check if image is spoof or not
#
#         :param image: cropped face image
#         :type image: numpy.array
#
#         :param threshold: decision threshold
#         :type threshold: float
#
#         :return: answer
#         :rtype: bool
#         """
#         raise NotImplementedError()
#
#     def make_prediction(self, image):
#         """Make prediction on how likely the image is spoof
#
#         :param image: cropped face image
#         :type image: numpy.array
#
#         :return: prediction score
#         """
#         raise NotImplementedError()
#
#
# class PADSpoofDetector(SpoofDetector, name='pad'):
#     """ Image-based Presentation Attack Detection.
#     This method is based luminance of the face images. More specifically, the
#     feature histograms are extracted from each image band separately.
#     Here, YCbCr and LUV color spaces are used for feature histograms
#     calculations.
#
#     References:
#         [1] https://github.com/ee09115/spoofing_detection
#
#         [2] https://link.springer.com/chapter/10.1007%2F978-3-030-05288-1_15
#
#         [3] https://arxiv.org/pdf/1511.06316v1.pdf
#     """
#
#     def __init__(self) -> None:
#         try:
#             self._clf_model = joblib.load(
#                 os.path.join(
#                     RESOURCES,
#                     "data/print-attack_ycrcb_luv_extraTreesClassifier.pkl")
#             )
#         except RuntimeError:
#             logging.error(
#                 "Model 'pad' not found." +
#                 "Use `fetch_models` and try again."
#             )
#
#     def is_spoof(self, image, threshold):
#         prediction = self.make_prediction(image)
#         return np.mean(prediction) >= threshold
#
#     def make_prediction(self, image):
#         feature_vector = self._extract_features(image)
#         prediction = self._clf_model.predict_proba(feature_vector)
#         return prediction[0][1]
#
#     def _extract_features(self, image):
#         img_ycrcb = cv2.cvtColor(image, cv2.COLOR_BGR2YCR_CB)
#         img_luv = cv2.cvtColor(image, cv2.COLOR_BGR2LUV)
#         ycrcb_hist = self._calc_hist(img_ycrcb)
#         luv_hist = self._calc_hist(img_luv)
#         feature_vector = np.append(ycrcb_hist.ravel(), luv_hist.ravel())
#         return feature_vector.reshape(1, len(feature_vector))
#
#     @staticmethod
#     def _calc_hist(image):
#         histogram = [0] * 3
#         for j in range(3):
#             histr = cv2.calcHist([image], [j], None, [256], [0, 256])
#             histr *= 255.0 / histr.max()
#             histogram[j] = histr
#         return np.array(histogram)
