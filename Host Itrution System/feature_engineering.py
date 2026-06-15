"""
Feature Engineering Module - Extract and preprocess features for ML models
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.decomposition import PCA
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FeatureExtractor:
    """Extract and engineer features from raw system data"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.feature_names = []
        
    def extract_statistical_features(self, data: List[Dict]) -> pd.DataFrame:
        """Extract statistical features from collected data"""
        try:
            df = pd.DataFrame(data)
            
            # Flatten nested dictionaries
            if 'system_metrics' in df.columns:
                system_df = pd.json_normalize(df['system_metrics'])
                df = pd.concat([df.drop('system_metrics', axis=1), system_df], axis=1)
            
            if 'network_metrics' in df.columns:
                network_df = pd.json_normalize(df['network_metrics'])
                df = pd.concat([df.drop('network_metrics', axis=1), network_df], axis=1)
            
            if 'process_info' in df.columns:
                # Extract process statistics
                process_stats = []
                for pinfo in df['process_info']:
                    if isinstance(pinfo, tuple) and len(pinfo) > 1:
                        process_stats.append(pinfo[1])
                    else:
                        process_stats.append({})
                
                process_df = pd.json_normalize(process_stats)
                df = pd.concat([df.drop('process_info', axis=1), process_df], axis=1)
            
            if 'user_activity' in df.columns:
                user_df = pd.json_normalize(df['user_activity'])
                df = pd.concat([df.drop('user_activity', axis=1), user_df], axis=1)
            
            if 'auth_events' in df.columns:
                auth_df = pd.json_normalize(df['auth_events'])
                df = pd.concat([df.drop('auth_events', axis=1), auth_df], axis=1)
            
            return df
        except Exception as e:
            logger.error(f"Error extracting statistical features: {e}")
            return pd.DataFrame()
    
    def create_temporal_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create time-based features"""
        try:
            if 'timestamp' in df.columns:
                timestamps = pd.to_datetime(df['timestamp'])
                df['hour'] = timestamps.dt.hour
                df['day_of_week'] = timestamps.dt.dayofweek
                df['is_weekend'] = (timestamps.dt.dayofweek >= 5).astype(int)
                df['is_business_hours'] = ((timestamps.dt.hour >= 9) & 
                                          (timestamps.dt.hour <= 17)).astype(int)
            
            # Calculate rolling statistics if we have enough data
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            
            for col in numeric_cols:
                if len(df) > 10:
                    df[f'{col}_rolling_mean'] = df[col].rolling(window=10, min_periods=1).mean()
                    df[f'{col}_rolling_std'] = df[col].rolling(window=10, min_periods=1).std()
                    df[f'{col}_diff'] = df[col].diff()
            
            return df
        except Exception as e:
            logger.error(f"Error creating temporal features: {e}")
            return df
    
    def create_security_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create security-specific features"""
        try:
            # Failed login ratio
            if 'failed_logins' in df.columns and 'successful_logins' in df.columns:
                df['failed_login_ratio'] = df['failed_logins'] / (df['successful_logins'] + 1)
            
            # Process anomaly indicators
            if 'zombie_processes' in df.columns and 'total_processes' in df.columns:
                df['zombie_ratio'] = df['zombie_processes'] / (df['total_processes'] + 1)
            
            # High resource usage processes
            if 'high_cpu_processes' in df.columns and 'total_processes' in df.columns:
                df['high_cpu_ratio'] = df['high_cpu_processes'] / (df['total_processes'] + 1)
            
            if 'high_memory_processes' in df.columns and 'total_processes' in df.columns:
                df['high_memory_ratio'] = df['high_memory_processes'] / (df['total_processes'] + 1)
            
            # Network connection anomalies
            if 'num_connections' in df.columns and 'active_users' in df.columns:
                df['connections_per_user'] = df['num_connections'] / (df['active_users'] + 1)
            
            # I/O intensity
            if 'io_counters' in df.columns:
                io_data = pd.json_normalize(df['io_counters'])
                if 'read_bytes' in io_data.columns and 'write_bytes' in io_data.columns:
                    df['io_ratio'] = io_data['read_bytes'] / (io_data['write_bytes'] + 1)
            
            return df
        except Exception as e:
            logger.error(f"Error creating security features: {e}")
            return df
    
    def handle_missing_values(self, df: pd.DataFrame, strategy: str = 'mean') -> pd.DataFrame:
        """Handle missing values in the dataset"""
        try:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            
            for col in numeric_cols:
                if df[col].isnull().any():
                    if strategy == 'mean':
                        df[col] = df[col].fillna(df[col].mean())
                    elif strategy == 'median':
                        df[col] = df[col].fillna(df[col].median())
                    elif strategy == 'zero':
                        df[col] = df[col].fillna(0)
            
            # Fill categorical columns with mode
            categorical_cols = df.select_dtypes(include=['object']).columns
            for col in categorical_cols:
                if df[col].isnull().any():
                    df[col] = df[col].fillna(df[col].mode()[0] if len(df[col].mode()) > 0 else 'unknown')
            
            return df
        except Exception as e:
            logger.error(f"Error handling missing values: {e}")
            return df
    
    def normalize_features(self, df: pd.DataFrame, method: str = 'standard') -> Tuple[pd.DataFrame, object]:
        """Normalize numerical features"""
        try:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            
            if len(numeric_cols) == 0:
                return df, None
            
            if method == 'standard':
                scaler = StandardScaler()
            elif method == 'minmax':
                scaler = MinMaxScaler()
            else:
                scaler = StandardScaler()
            
            df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
            self.scaler = scaler
            
            return df, scaler
        except Exception as e:
            logger.error(f"Error normalizing features: {e}")
            return df, None
    
    def reduce_dimensions(self, X: np.ndarray, n_components: int = 10) -> Tuple[np.ndarray, PCA]:
        """Reduce feature dimensions using PCA"""
        try:
            pca = PCA(n_components=n_components)
            X_reduced = pca.fit_transform(X)
            
            logger.info(f"PCA explained variance ratio: {sum(pca.explained_variance_ratio_):.4f}")
            
            return X_reduced, pca
        except Exception as e:
            logger.error(f"Error reducing dimensions: {e}")
            return X, None
    
    def select_top_features(self, df: pd.DataFrame, target: pd.Series = None, 
                           top_n: int = 20) -> Tuple[pd.DataFrame, List[str]]:
        """Select top features based on importance"""
        try:
            from sklearn.ensemble import RandomForestClassifier
            from sklearn.feature_selection import mutual_info_classif, f_classif
            
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            
            # Remove non-informative columns
            exclude_cols = ['timestamp', 'boot_time']
            feature_cols = [col for col in numeric_cols if col not in exclude_cols]
            
            if target is not None and len(feature_cols) > 0:
                # Use mutual information for feature selection
                X = df[feature_cols].fillna(0)
                y = target
                
                mi_scores = mutual_info_classif(X, y, random_state=42)
                
                # Select top features
                top_indices = np.argsort(mi_scores)[::-1][:top_n]
                selected_features = [feature_cols[i] for i in top_indices]
                
                logger.info(f"Selected {len(selected_features)} top features")
                
                return df[selected_features], selected_features
            else:
                return df[feature_cols], feature_cols
                
        except Exception as e:
            logger.error(f"Error selecting features: {e}")
            return df, []
    
    def prepare_features(self, raw_data: List[Dict], fit_scaler: bool = True) -> Tuple[np.ndarray, List[str]]:
        """Complete feature preparation pipeline"""
        try:
            # Extract statistical features
            df = self.extract_statistical_features(raw_data)
            
            if df.empty:
                logger.error("Empty dataframe after feature extraction")
                return np.array([]), []
            
            # Create temporal features
            df = self.create_temporal_features(df)
            
            # Create security features
            df = self.create_security_features(df)
            
            # Handle missing values
            df = self.handle_missing_values(df)
            
            # Get feature names
            numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
            exclude_cols = ['timestamp', 'boot_time']
            feature_names = [col for col in numeric_cols if col not in exclude_cols]
            
            # Convert to numpy array
            X = df[feature_names].values
            
            # Normalize
            if fit_scaler:
                X, _ = self.normalize_features(df[feature_names])
                X = X.values if hasattr(X, 'values') else X
            
            logger.info(f"Prepared {X.shape[1]} features from {X.shape[0]} samples")
            
            return X, feature_names
            
        except Exception as e:
            logger.error(f"Error in feature preparation: {e}")
            return np.array([]), []


class DataPreprocessor:
    """Preprocess data for training and inference"""
    
    def __init__(self):
        self.feature_extractor = FeatureExtractor()
        self.is_fitted = False
        
    def preprocess_for_training(self, data: List[Dict], labels: np.ndarray = None
                                ) -> Tuple[np.ndarray, np.ndarray, List[str]]:
        """Prepare data for model training"""
        X, feature_names = self.feature_extractor.prepare_features(data, fit_scaler=True)
        
        if labels is None:
            # For unsupervised learning, create dummy labels
            labels = np.zeros(len(X))
        
        self.is_fitted = True
        
        return X, labels, feature_names
    
    def preprocess_for_inference(self, data: Dict) -> Tuple[np.ndarray, List[str]]:
        """Prepare single data point for inference"""
        # Wrap single data point in list
        X, feature_names = self.feature_extractor.prepare_features([data], fit_scaler=False)
        
        return X, feature_names
    
    def get_feature_statistics(self, X: np.ndarray, feature_names: List[str]) -> pd.DataFrame:
        """Get statistics about features"""
        try:
            stats = pd.DataFrame({
                'feature': feature_names,
                'mean': np.mean(X, axis=0),
                'std': np.std(X, axis=0),
                'min': np.min(X, axis=0),
                'max': np.max(X, axis=0),
                'median': np.median(X, axis=0)
            })
            
            return stats
        except Exception as e:
            logger.error(f"Error computing feature statistics: {e}")
            return pd.DataFrame()


if __name__ == "__main__":
    # Test feature extraction
    from data_collector import DataCollector
    
    collector = DataCollector()
    raw_data = [collector.collect_all_data() for _ in range(5)]
    
    preprocessor = DataPreprocessor()
    X, y, feature_names = preprocessor.preprocess_for_training(raw_data)
    
    print(f"Feature matrix shape: {X.shape}")
    print(f"Number of features: {len(feature_names)}")
    print(f"Features: {feature_names[:10]}...")  # Show first 10 features
