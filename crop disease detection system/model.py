"""
Crop Disease Detection Model
Uses transfer learning with MobileNetV2 for efficient disease classification
"""
import numpy as np
from tensorflow import keras
from tensorflow.keras import layers
from config import MODEL_PATH, DISEASE_CLASSES, IMG_SIZE


class CropDiseaseModel:
    """Deep learning model for crop disease detection"""
    
    def __init__(self, img_size=IMG_SIZE, num_classes=len(DISEASE_CLASSES)):
        self.img_size = img_size
        self.num_classes = num_classes
        self.model = None
        self.history = None
        
    def create_model(self):
        """
        Create MobileNetV2 based model for disease detection
        Using transfer learning for better performance with less data
        """
        # Load pre-trained MobileNetV2 (lightweight and efficient)
        base_model = keras.applications.MobileNetV2(
            input_shape=(self.img_size, self.img_size, 3),
            include_top=False,
            weights='imagenet',
            pooling='avg'
        )
        
        # Freeze the base model (transfer learning)
        base_model.trainable = False
        
        # Build the complete model
        inputs = keras.Input(shape=(self.img_size, self.img_size, 3))
        
        # Data augmentation layer
        x = layers.Rescaling(1./255)(inputs)
        
        # Base model
        x = base_model(x, training=False)
        
        # Custom classification head
        x = layers.Dense(128, activation='relu')(x)
        x = layers.Dropout(0.3)(x)
        x = layers.Dense(64, activation='relu')(x)
        x = layers.Dropout(0.2)(x)
        
        # Output layer
        outputs = layers.Dense(self.num_classes, activation='softmax')(x)
        
        self.model = keras.Model(inputs, outputs)
        
        # Compile model
        self.model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        print("Model created successfully")
        print(f"Total parameters: {self.model.count_params():,}")
        
        return self.model
    
    def unfreeze_and_finetune(self, fine_tune_from=100):
        """
        Unfreeze some layers of base model for fine-tuning
        Call this after initial training
        """
        # Unfreeze the top layers of the base model
        for layer in self.model.layers[1].layers[fine_tune_from:]:
            layer.trainable = True
        
        # Recompile with lower learning rate
        self.model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.0001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        print(f"Fine-tuning enabled from layer {fine_tune_from}")
    
    def train(self, X_train, y_train, X_val=None, y_val=None, 
              epochs=10, batch_size=32, callbacks=None):
        """
        Train the model
        Returns training history
        """
        if self.model is None:
            self.create_model()
        
        # Validation data
        validation_data = None
        if X_val is not None and y_val is not None:
            validation_data = (X_val, y_val)
        
        # Train model
        self.history = self.model.fit(
            X_train, y_train,
            epochs=epochs,
            batch_size=batch_size,
            validation_data=validation_data,
            callbacks=callbacks
        )
        
        print("Training completed")
        return self.history
    
    def evaluate(self, X_test, y_test):
        """Evaluate model on test data"""
        if self.model is None:
            raise ValueError("Model not created. Call create_model() first.")
        
        results = self.model.evaluate(X_test, y_test, verbose=0)
        print(f"Test Loss: {results[0]:.4f}")
        print(f"Test Accuracy: {results[1]:.4f}")
        
        return results
    
    def predict(self, images):
        """
        Make predictions
        images: numpy array of shape (batch_size, height, width, channels)
        Returns: tuple of (predicted_class_indices, confidence_scores)
        """
        if self.model is None:
            raise ValueError("Model not created. Call create_model() or load_model() first.")
        
        predictions = self.model.predict(images)
        predicted_classes = np.argmax(predictions, axis=1)
        confidence_scores = np.max(predictions, axis=1)
        
        return predicted_classes, confidence_scores, predictions
    
    def predict_detailed(self, image):
        """
        Make prediction for a single image with detailed output
        Returns dictionary with class name, confidence, and all probabilities
        """
        pred_classes, conf_scores, all_probs = self.predict(image)
        
        pred_class_idx = pred_classes[0]
        confidence = conf_scores[0]
        class_name = DISEASE_CLASSES[pred_class_idx]
        
        # Get top 3 predictions
        top_3_indices = np.argsort(all_probs[0])[::-1][:3]
        top_3_predictions = [
            {
                'class': DISEASE_CLASSES[idx],
                'confidence': float(all_probs[0][idx])
            }
            for idx in top_3_indices
        ]
        
        result = {
            'predicted_class': class_name,
            'confidence': float(confidence),
            'top_3_predictions': top_3_predictions,
            'all_probabilities': all_probs[0].tolist()
        }
        
        return result
    
    def save_model(self, model_path=None):
        """Save trained model"""
        if model_path is None:
            model_path = MODEL_PATH
        
        if self.model is None:
            raise ValueError("No model to save")
        
        self.model.save(model_path)
        print(f"Model saved to {model_path}")
    
    def load_model(self, model_path=None):
        """Load trained model"""
        if model_path is None:
            model_path = MODEL_PATH
        
        try:
            self.model = keras.models.load_model(model_path)
            print(f"Model loaded from {model_path}")
            return True
        except Exception as e:
            print(f"Error loading model: {str(e)}")
            return False
    
    def summary(self):
        """Display model architecture summary"""
        if self.model is None:
            print("No model created yet")
            return
        
        self.model.summary()


def create_crop_disease_model():
    """Helper function to create and initialize model"""
    model = CropDiseaseModel()
    model.create_model()
    return model


if __name__ == "__main__":
    # Example usage
    model = create_crop_disease_model()
    model.summary()
