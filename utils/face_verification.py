from deepface import DeepFace
import config
from typing import Tuple, Dict

class FaceVerifier:
    def __init__(self):
        self.model_name = config.FACE_RECOGNITION_MODEL
        self.detector_backend = config.FACE_DETECTION_BACKEND
        self.distance_metric = config.DISTANCE_METRIC
        self.threshold = config.VERIFICATION_THRESHOLD
    
    def verify_faces(self, img1_path: str, img2_path: str) -> Tuple[bool, float, Dict]:
        try:
            result = DeepFace.verify(
                img1_path=img1_path,
                img2_path=img2_path,
                model_name=self.model_name,
                detector_backend=self.detector_backend,
                distance_metric=self.distance_metric,
                enforce_detection=True
            )
            is_verified = result["verified"]
            distance = result["distance"]
            confidence = 1 - (distance / result["threshold"]) if distance < result["threshold"] else 0
            return is_verified, confidence, result
        except Exception as e:
            print(f"Verification error: {e}")
            return False, 0.0, {"error": str(e)}
