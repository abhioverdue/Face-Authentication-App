from deepface import DeepFace
import numpy as np
import os
import pickle
from typing import Dict, List, Tuple, Optional
import config

class FaceRecognizer:
    def __init__(self):
        self.model_name = config.FACE_RECOGNITION_MODEL
        self.detector_backend = config.FACE_DETECTION_BACKEND
        self.distance_metric = config.DISTANCE_METRIC
        self.threshold = config.RECOGNITION_THRESHOLD
        
    def extract_embedding(self, img_path: str) -> Optional[np.ndarray]:
        try:
            embedding = DeepFace.represent(
                img_path=img_path,
                model_name=self.model_name,
                detector_backend=self.detector_backend,
                enforce_detection=True
            )
            return np.array(embedding[0]["embedding"])
        except Exception as e:
            print(f"Error extracting embedding: {e}")
            return None
    
    def build_database(self) -> Dict[str, List[np.ndarray]]:
        database = {}
        for person_name in os.listdir(config.DATABASE_DIR):
            person_path = os.path.join(config.DATABASE_DIR, person_name)
            if not os.path.isdir(person_path):
                continue
            embeddings = []
            for img_file in os.listdir(person_path):
                if img_file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    img_path = os.path.join(person_path, img_file)
                    embedding = self.extract_embedding(img_path)
                    if embedding is not None:
                        embeddings.append(embedding)
            if embeddings:
                database[person_name] = embeddings
                print(f"✓ Loaded {len(embeddings)} embeddings for {person_name}")
        
        with open(config.EMBEDDINGS_PATH, 'wb') as f:
            pickle.dump(database, f)
        print(f"✅ Database built with {len(database)} people")
        return database
    
    def load_database(self) -> Dict[str, List[np.ndarray]]:
        if os.path.exists(config.EMBEDDINGS_PATH):
            with open(config.EMBEDDINGS_PATH, 'rb') as f:
                return pickle.load(f)
        return self.build_database()
    
    def calculate_distance(self, embedding1: np.ndarray, embedding2: np.ndarray) -> float:
        if self.distance_metric == "cosine":
            return 1 - np.dot(embedding1, embedding2) / (
                np.linalg.norm(embedding1) * np.linalg.norm(embedding2)
            )
        elif self.distance_metric == "euclidean":
            return np.linalg.norm(embedding1 - embedding2)
        return float('inf')
    
    def recognize_face(self, img_path: str) -> Tuple[Optional[str], float, Dict]:
        query_embedding = self.extract_embedding(img_path)
        if query_embedding is None:
            return None, 0.0, {}
        
        database = self.load_database()
        if not database:
            return None, 0.0, {}
        
        best_match = None
        best_distance = float('inf')
        all_matches = {}
        
        for person_name, embeddings in database.items():
            distances = [self.calculate_distance(query_embedding, emb) for emb in embeddings]
            avg_distance = np.mean(distances)
            all_matches[person_name] = avg_distance
            if avg_distance < best_distance:
                best_distance = avg_distance
                best_match = person_name
        
        if best_distance <= self.threshold:
            confidence = 1 - best_distance
            return best_match, confidence, all_matches
        return None, 0.0, all_matches
    
    def quick_face_check(self, img_path: str) -> bool:
        try:
            faces = DeepFace.extract_faces(
                img_path=img_path,
                detector_backend=self.detector_backend,
                enforce_detection=False
            )
            return len(faces) > 0
        except:
            return False
