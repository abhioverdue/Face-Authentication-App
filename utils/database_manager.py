import os
import shutil
import json
import config
from typing import List, Dict, Optional
from datetime import datetime
import numpy as np

class DatabaseManager:
    
    @staticmethod
    def get_registered_users() -> List[str]:
        """Get list of all registered users"""
        if not os.path.exists(config.DATABASE_DIR):
            return []
        return [name for name in os.listdir(config.DATABASE_DIR) 
                if os.path.isdir(os.path.join(config.DATABASE_DIR, name))]
    
    @staticmethod
    def register_new_user(name: str, image_paths: List[str], employee_id: str = "", 
                         department: str = "", notes: str = "") -> bool:
        """Register a new user with face images"""
        try:
            user_dir = os.path.join(config.DATABASE_DIR, name)
            os.makedirs(user_dir, exist_ok=True)
            
            # Copy images
            for i, img_path in enumerate(image_paths):
                dest_path = os.path.join(user_dir, f"photo_{i+1}.jpg")
                shutil.copy(img_path, dest_path)
            
            # Save metadata
            DatabaseManager._save_user_metadata(name, {
                'full_name': str(name),
                'employee_id': str(employee_id),
                'department': str(department),
                'notes': str(notes),
                'photo_count': int(len(image_paths)),
                'registered_date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'last_seen': None,
                'total_access_count': 0
            })
            
            # Rebuild face database
            from utils.face_recognition import FaceRecognizer
            recognizer = FaceRecognizer()
            recognizer.build_database()
            return True
            
        except Exception as e:
            print(f"Registration error: {e}")
            return False
    
    @staticmethod
    def delete_user(name: str) -> bool:
        """Delete a registered user"""
        try:
            user_dir = os.path.join(config.DATABASE_DIR, name)
            if os.path.exists(user_dir):
                shutil.rmtree(user_dir)
                DatabaseManager._remove_user_metadata(name)
                
                # Rebuild face database
                from utils.face_recognition import FaceRecognizer
                recognizer = FaceRecognizer()
                recognizer.build_database()
                return True
            return False
            
        except Exception as e:
            print(f"Deletion error: {e}")
            return False
    
    @staticmethod
    def get_user_image_count(name: str) -> int:
        """Get number of images for a user"""
        user_dir = os.path.join(config.DATABASE_DIR, name)
        if not os.path.exists(user_dir):
            return 0
        return len([f for f in os.listdir(user_dir) 
                   if f.lower().endswith(('.jpg', '.jpeg', '.png'))])
    
    @staticmethod
    def get_user_info(name: str) -> Optional[Dict]:
        """Get metadata about a user"""
        metadata = DatabaseManager._load_all_metadata()
        return metadata.get(name)
    
    @staticmethod
    def log_access(name: str, confidence: float, emotion: str = "", suspicious: bool = False):
        """Log successful user access attempt"""
        access_logs = DatabaseManager._load_access_logs()
        
        # Convert all values to JSON-serializable Python types
        log_entry = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'user_name': str(name),
            'confidence': float(round(float(confidence) * 100, 2)),
            'emotion': str(emotion),
            'suspicious': bool(suspicious),  # This handles numpy.bool_ automatically
            'status': 'granted'
        }
        
        access_logs.append(log_entry)
        
        # Keep only last 1000 logs
        if len(access_logs) > 1000:
            access_logs = access_logs[-1000:]
        
        DatabaseManager._save_access_logs(access_logs)
        
        # Update user metadata
        metadata = DatabaseManager._load_all_metadata()
        if name in metadata:
            metadata[name]['last_seen'] = log_entry['timestamp']
            metadata[name]['total_access_count'] = int(metadata[name].get('total_access_count', 0) + 1)
            DatabaseManager._save_all_metadata(metadata)
    
    @staticmethod
    def log_access_denied(confidence: float = 0.0):
        """Log denied access attempt"""
        access_logs = DatabaseManager._load_access_logs()
        
        log_entry = {
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'user_name': 'Unknown',
            'confidence': float(round(float(confidence) * 100, 2)),
            'emotion': '',
            'suspicious': False,
            'status': 'denied'
        }
        
        access_logs.append(log_entry)
        
        # Keep only last 1000 logs
        if len(access_logs) > 1000:
            access_logs = access_logs[-1000:]
            
        DatabaseManager._save_access_logs(access_logs)
    
    @staticmethod
    def get_access_logs(limit: int = 50) -> List[Dict]:
        """Get recent access logs"""
        logs = DatabaseManager._load_access_logs()
        return logs[-limit:][::-1]
    
    @staticmethod
    def get_statistics() -> Dict:
        """Get system statistics"""
        users = DatabaseManager.get_registered_users()
        logs = DatabaseManager._load_access_logs()
        
        return {
            'total_users': len(users),
            'total_photos': sum([DatabaseManager.get_user_image_count(u) for u in users]),
            'total_accesses': len([l for l in logs if l.get('status') == 'granted']),
            'total_denials': len([l for l in logs if l.get('status') == 'denied']),
            'suspicious_count': len([l for l in logs if l.get('suspicious', False)]),
            'total_logs': len(logs)
        }
    
    # ========================================
    # PRIVATE HELPER METHODS
    # ========================================
    
    @staticmethod
    def _load_all_metadata() -> Dict:
        """Load all user metadata from JSON"""
        if os.path.exists(config.USER_INFO_PATH):
            try:
                with open(config.USER_INFO_PATH, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("Warning: Could not decode user_info.json")
                return {}
        return {}
    
    @staticmethod
    def _save_all_metadata(metadata: Dict):
        """Save all user metadata to JSON"""
        with open(config.USER_INFO_PATH, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    @staticmethod
    def _save_user_metadata(name: str, data: Dict):
        """Save metadata for a specific user"""
        metadata = DatabaseManager._load_all_metadata()
        metadata[name] = data
        DatabaseManager._save_all_metadata(metadata)
    
    @staticmethod
    def _remove_user_metadata(name: str):
        """Remove metadata for a specific user"""
        metadata = DatabaseManager._load_all_metadata()
        if name in metadata:
            del metadata[name]
            DatabaseManager._save_all_metadata(metadata)
    
    @staticmethod
    def _load_access_logs() -> List[Dict]:
        """Load access logs from JSON"""
        if os.path.exists(config.ACCESS_LOGS_PATH):
            try:
                with open(config.ACCESS_LOGS_PATH, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("Warning: Could not decode access_logs.json")
                return []
        return []
    
    @staticmethod
    def _save_access_logs(logs: List[Dict]):
        """Save access logs to JSON - handles numpy types automatically"""
        # Simple conversion function
        def convert_value(value):
            """Convert numpy types to Python native types"""
            if isinstance(value, (np.integer, np.int64, np.int32, np.int16, np.int8)):
                return int(value)
            elif isinstance(value, (np.floating, np.float64, np.float32, np.float16)):
                return float(value)
            elif isinstance(value, np.bool_):
                return bool(value)
            elif isinstance(value, (list, tuple)):
                return [convert_value(v) for v in value]
            elif isinstance(value, dict):
                return {k: convert_value(v) for k, v in value.items()}
            else:
                return value
        
        # Clean all logs
        clean_logs = []
        for log in logs:
            clean_log = {key: convert_value(value) for key, value in log.items()}
            clean_logs.append(clean_log)
        
        # Save to JSON
        with open(config.ACCESS_LOGS_PATH, 'w') as f:
            json.dump(clean_logs, f, indent=2)

