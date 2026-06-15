"""
Text-based Plant Disease Diagnosis System
Diagnoses plant diseases based on symptom descriptions rather than images
"""
import json
from datetime import datetime


class PlantDiseaseDiagnosis:
    """Diagnose plant diseases based on symptom descriptions"""
    
    def __init__(self):
        self.disease_knowledge_base = self._create_knowledge_base()
        self.patient_data = {}
        
    def _create_knowledge_base(self):
        """Create knowledge base of plant diseases and symptoms"""
        return {
            'tomato': {
                'early_blight': {
                    'name': 'Early Blight',
                    'scientific_name': 'Alternaria solani',
                    'symptoms': [
                        'dark spots on leaves',
                        'concentric rings on leaves',
                        'yellowing around spots',
                        'lower leaves affected first',
                        'brown lesions on stem'
                    ],
                    'treatment': [
                        'Remove infected leaves immediately',
                        'Apply copper-based fungicide every 7-10 days',
                        'Improve air circulation around plants',
                        'Water at soil level, avoid wetting leaves',
                        'Mulch around base to prevent soil splash'
                    ],
                    'prevention': [
                        'Rotate crops annually (3-year cycle)',
                        'Use resistant varieties',
                        'Maintain proper plant spacing (24-36 inches)',
                        'Apply preventive fungicide during humid weather'
                    ],
                    'urgency': 'medium',
                    'spread_risk': 'high'
                },
                'late_blight': {
                    'name': 'Late Blight',
                    'scientific_name': 'Phytophthora infestans',
                    'symptoms': [
                        'water-soaked spots on leaves',
                        'white fungal growth on leaf undersides',
                        'rapid browning and death of foliage',
                        'dark lesions on stems',
                        'brown rot on fruits'
                    ],
                    'treatment': [
                        'Remove and destroy infected plants immediately',
                        'Apply fungicide containing chlorothalonil or mancozeb',
                        'Do not compost infected material',
                        'Treat nearby plants preventively'
                    ],
                    'prevention': [
                        'Plant early blight-resistant varieties',
                        'Ensure good drainage',
                        'Avoid overhead watering',
                        'Monitor weather conditions (cool, wet weather favors disease)'
                    ],
                    'urgency': 'high',
                    'spread_risk': 'very high'
                },
                'bacterial_spot': {
                    'name': 'Bacterial Spot',
                    'scientific_name': 'Xanthomonas campestris',
                    'symptoms': [
                        'small water-soaked spots',
                        'spots turn brown or black',
                        'yellow halo around spots',
                        'spots on fruits (scabby)',
                        'leaf drop in severe cases'
                    ],
                    'treatment': [
                        'Apply copper-based bactericide',
                        'Remove infected plant material',
                        'Avoid working with wet plants',
                        'Disinfect tools after use'
                    ],
                    'prevention': [
                        'Use disease-free seeds',
                        'Practice crop rotation',
                        'Control weeds',
                        'Avoid overhead irrigation'
                    ],
                    'urgency': 'medium',
                    'spread_risk': 'high'
                },
                'healthy': {
                    'name': 'Healthy Plant',
                    'scientific_name': 'N/A',
                    'symptoms': [
                        'vibrant green leaves',
                        'steady growth',
                        'no unusual spots or discoloration',
                        'strong stems',
                        'normal flowering and fruiting'
                    ],
                    'treatment': [
                        'Continue current care routine',
                        'Regular monitoring for early detection',
                        'Maintain consistent watering schedule',
                        'Apply balanced fertilizer'
                    ],
                    'prevention': [
                        'Regular inspection',
                        'Proper watering and nutrition',
                        'Good garden hygiene',
                        'Beneficial insect habitat'
                    ],
                    'urgency': 'low',
                    'spread_risk': 'none'
                }
            },
            'potato': {
                'early_blight': {
                    'name': 'Early Blight',
                    'symptoms': ['dark spots with concentric rings', 'yellowing leaves'],
                    'treatment': ['Apply fungicide', 'Remove infected foliage'],
                    'prevention': ['Crop rotation', 'Resistant varieties'],
                    'urgency': 'medium',
                    'spread_risk': 'high'
                },
                'late_blight': {
                    'name': 'Late Blight',
                    'symptoms': ['water-soaked lesions', 'white mold', 'rapid wilting'],
                    'treatment': ['Destroy infected plants', 'Apply fungicide'],
                    'prevention': ['Good drainage', 'Resistant varieties'],
                    'urgency': 'high',
                    'spread_risk': 'very high'
                }
            },
            'apple': {
                'apple_scab': {
                    'name': 'Apple Scab',
                    'scientific_name': 'Venturia inaequalis',
                    'symptoms': [
                        'olive-green spots on leaves',
                        'corky spots on fruit',
                        'distorted leaves',
                        'premature leaf drop'
                    ],
                    'treatment': [
                        'Apply fungicide (captan or ziram) at bud break',
                        'Rake and destroy fallen leaves',
                        'Prune for better air circulation',
                        'Apply lime sulfur in dormant season'
                    ],
                    'prevention': [
                        'Plant scab-resistant varieties',
                        'Annual pruning',
                        'Clean up fallen leaves in autumn',
                        'Preventive fungicide sprays in spring'
                    ],
                    'urgency': 'medium',
                    'spread_risk': 'high'
                },
                'powdery_mildew': {
                    'name': 'Powdery Mildew',
                    'scientific_name': 'Podosphaera leucotricha',
                    'symptoms': [
                        'white powdery coating on leaves',
                        'distorted new growth',
                        'stunted shoots',
                        'russeting on fruit'
                    ],
                    'treatment': [
                        'Apply sulfur-based fungicide',
                        'Prune infected shoots',
                        'Improve air circulation',
                        'Apply horticultural oil'
                    ],
                    'prevention': [
                        'Resistant varieties',
                        'Proper pruning',
                        'Avoid excessive nitrogen fertilizer',
                        'Good site selection'
                    ],
                    'urgency': 'low',
                    'spread_risk': 'medium'
                }
            }
        }
    
    def diagnose(self, plant_type, symptoms, additional_info=None):
        """
        Diagnose plant disease based on symptoms
        
        Args:
            plant_type: Type of plant (tomato, potato, apple, etc.)
            symptoms: List of observed symptoms
            additional_info: Optional dict with extra information
            
        Returns:
            Diagnosis result dictionary
        """
        plant_type = plant_type.lower().strip()
        
        if plant_type not in self.disease_knowledge_base:
            return self._create_unknown_diagnosis(plant_type)
        
        plant_diseases = self.disease_knowledge_base[plant_type]
        
        # Score each disease based on symptom matching
        disease_scores = {}
        for disease_key, disease_info in plant_diseases.items():
            score = self._calculate_symptom_match(symptoms, disease_info['symptoms'])
            disease_scores[disease_key] = score
        
        # Get best match
        best_match = max(disease_scores, key=disease_scores.get)
        confidence = disease_scores[best_match]
        
        diagnosis_info = plant_diseases[best_match]
        
        result = {
            'plant_type': plant_type.title(),
            'diagnosis': diagnosis_info['name'],
            'scientific_name': diagnosis_info.get('scientific_name', 'Not specified'),
            'confidence': min(confidence, 100),
            'matched_symptoms': self._get_matched_symptoms(symptoms, diagnosis_info['symptoms']),
            'all_symptoms': diagnosis_info['symptoms'],
            'treatment': diagnosis_info['treatment'],
            'prevention': diagnosis_info['prevention'],
            'urgency': diagnosis_info['urgency'],
            'spread_risk': diagnosis_info['spread_risk'],
            'additional_notes': self._generate_additional_notes(best_match, additional_info)
        }
        
        return result
    
    def _calculate_symptom_match(self, observed_symptoms, disease_symptoms):
        """Calculate match percentage between observed and disease symptoms"""
        if not observed_symptoms:
            return 0
        
        observed_lower = [s.lower() for s in observed_symptoms]
        disease_lower = [s.lower() for s in disease_symptoms]
        
        matches = 0
        for obs in observed_lower:
            for disease_sym in disease_lower:
                if obs in disease_sym or disease_sym in obs:
                    matches += 1
                    break
        
        # Weight by proportion of disease symptoms matched
        symptom_match_ratio = matches / len(disease_symptoms)
        
        # Also consider how many observed symptoms found a match
        observation_accuracy = matches / len(observed_symptoms) if observed_symptoms else 0
        
        # Combined score (weighted average)
        combined_score = (symptom_match_ratio * 0.7 + observation_accuracy * 0.3) * 100
        
        return combined_score
    
    def _get_matched_symptoms(self, observed, disease_symptoms):
        """Get list of matched symptoms"""
        observed_lower = [s.lower() for s in observed]
        disease_lower = [s.lower() for s in disease_symptoms]
        
        matched = []
        for obs in observed:
            for i, disease_sym in enumerate(disease_symptoms):
                if obs.lower() in disease_lower[i] or disease_lower[i] in obs.lower():
                    matched.append(disease_symptoms[i])
                    break
        
        return matched
    
    def _generate_additional_notes(self, disease_key, additional_info):
        """Generate additional notes based on disease and info provided"""
        notes = []
        
        if disease_key == 'healthy':
            notes.append("✓ Your plant appears healthy! Continue monitoring regularly.")
        elif disease_key == 'late_blight':
            notes.append("⚠ LATE BLIGHT IS HIGHLY CONTAGIOUS! Take immediate action to prevent spread.")
            notes.append("Consider removing entire plant if infection is severe.")
        elif disease_key == 'bacterial_spot':
            notes.append("🦠 Bacterial infections can spread quickly through water and tools.")
            notes.append("Always disinfect tools after working with infected plants.")
        
        if additional_info:
            if additional_info.get('weather') == 'humid':
                notes.append("💧 High humidity favors fungal growth. Improve ventilation.")
            if additional_info.get('watering') == 'overhead':
                notes.append("💦 Switch to soil-level watering to reduce leaf wetness.")
            if additional_info.get('severity') == 'severe':
                notes.append("🚨 Severe infection detected. Consider aggressive treatment or plant removal.")
        
        return "\n".join(notes)
    
    def _create_unknown_diagnosis(self, plant_type):
        """Create response for unknown plant type"""
        return {
            'plant_type': plant_type.title(),
            'diagnosis': 'Unknown Plant Type',
            'scientific_name': 'N/A',
            'confidence': 0,
            'matched_symptoms': [],
            'all_symptoms': [],
            'treatment': ['Consult with local agricultural extension office', 
                         'Take photos and seek expert identification',
                         'Research common diseases for your specific plant variety'],
            'prevention': ['Maintain good garden hygiene',
                          'Monitor plants regularly',
                          'Keep records of plant health'],
            'urgency': 'unknown',
            'spread_risk': 'unknown',
            'additional_notes': f"We don't have specific information about {plant_type} in our database yet."
        }
    
    def generate_report(self, diagnosis_result, output_format='text'):
        """Generate a formatted report from diagnosis results"""
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if output_format == 'text':
            report = self._generate_text_report(diagnosis_result, timestamp)
        elif output_format == 'json':
            report = json.dumps({
                'timestamp': timestamp,
                **diagnosis_result
            }, indent=2)
        else:
            report = self._generate_text_report(diagnosis_result, timestamp)
        
        return report
    
    def _generate_text_report(self, result, timestamp):
        """Generate human-readable text report"""
        urgency_icons = {
            'high': '🔴',
            'medium': '🟡',
            'low': '🟢',
            'unknown': '⚪'
        }
        
        risk_icons = {
            'very high': '🔴🔴',
            'high': '🔴',
            'medium': '🟡',
            'low': '🟢',
            'none': '✅',
            'unknown': '⚪'
        }
        
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║          PLANT DISEASE DIAGNOSIS REPORT                      ║
╚══════════════════════════════════════════════════════════════╝

Report Generated: {timestamp}

┌──────────────────────────────────────────────────────────────┐
│ PLANT INFORMATION                                            │
└──────────────────────────────────────────────────────────────┘

Plant Type: {result['plant_type']}
Diagnosis: {result['diagnosis']}
Scientific Name: {result['scientific_name']}
Confidence Level: {result['confidence']:.1f}%

┌──────────────────────────────────────────────────────────────┐
│ SYMPTOM ANALYSIS                                             │
└──────────────────────────────────────────────────────────────┘

Matched Symptoms:
"""
        
        for symptom in result['matched_symptoms']:
            report += f"  ✓ {symptom}\n"
        
        if not result['matched_symptoms']:
            report += "  No specific symptoms matched\n"
        
        report += f"""
┌──────────────────────────────────────────────────────────────┐
│ RISK ASSESSMENT                                              │
└──────────────────────────────────────────────────────────────┘

Urgency Level: {urgency_icons.get(result['urgency'], '⚪')} {result['urgency'].upper()}
Spread Risk: {risk_icons.get(result['spread_risk'], '⚪')} {result['spread_risk'].upper()}

┌──────────────────────────────────────────────────────────────┐
│ RECOMMENDED TREATMENT                                        │
└──────────────────────────────────────────────────────────────┘

"""
        
        for i, treatment in enumerate(result['treatment'], 1):
            report += f"{i}. {treatment}\n"
        
        report += f"""
┌──────────────────────────────────────────────────────────────┐
│ PREVENTION MEASURES                                          │
└──────────────────────────────────────────────────────────────┘

"""
        
        for i, prevention in enumerate(result['prevention'], 1):
            report += f"{i}. {prevention}\n"
        
        if result['additional_notes']:
            report += f"""
┌──────────────────────────────────────────────────────────────┐
│ ADDITIONAL NOTES                                             │
└──────────────────────────────────────────────────────────────┘

{result['additional_notes']}
"""
        
        report += """
═══════════════════════════════════════════════════════════════

DISCLAIMER: This diagnosis is based on symptom descriptions provided.
For critical cases, consult with a professional plant pathologist or
your local agricultural extension office.

═══════════════════════════════════════════════════════════════
"""
        
        return report


def interactive_diagnosis():
    """Interactive command-line diagnosis session"""
    print("\n" + "="*70)
    print("PLANT DISEASE DIAGNOSIS SYSTEM")
    print("="*70)
    print("\nThis system will help diagnose plant diseases based on symptoms.\n")
    
    diagnosis = PlantDiseaseDiagnosis()
    
    # Get plant type
    print("What type of plant is affected?")
    print("Common options: tomato, potato, apple, grape, pepper, corn")
    plant_type = input("> ").strip()
    
    # Get symptoms
    print("\nDescribe the symptoms you observe (comma-separated):")
    print("Examples: dark spots on leaves, yellowing, wilting, white powder")
    symptoms_input = input("> ").strip()
    symptoms = [s.strip() for s in symptoms_input.split(',')]
    
    # Get additional info
    print("\nAdditional information (optional, press Enter to skip):")
    print("Weather conditions (humid/dry/wet)?")
    weather = input("> ").strip()
    
    print("Watering method (overhead/soil-level)?")
    watering = input("> ").strip()
    
    print("Severity (mild/moderate/severe)?")
    severity = input("> ").strip()
    
    additional_info = {
        'weather': weather,
        'watering': watering,
        'severity': severity
    }
    
    # Perform diagnosis
    print("\n" + "="*70)
    print("ANALYZING SYMPTOMS...")
    print("="*70 + "\n")
    
    result = diagnosis.diagnose(plant_type, symptoms, additional_info)
    
    # Generate and display report
    report = diagnosis.generate_report(result)
    print(report)
    
    # Save report
    save = input("\nWould you like to save this report? (yes/no): ").strip().lower()
    if save == 'yes':
        filename = f"plant_diagnosis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(filename, 'w') as f:
            f.write(report)
        print(f"\n✓ Report saved to: {filename}")
    
    return result


if __name__ == "__main__":
    interactive_diagnosis()
