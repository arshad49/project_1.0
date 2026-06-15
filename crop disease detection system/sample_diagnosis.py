"""
Sample plant disease diagnosis with automatic report generation
Demonstrates the text-based diagnosis system
"""
from text_diagnosis import PlantDiseaseDiagnosis
from datetime import datetime


def demo_diagnosis():
    """Run demonstration diagnoses for common scenarios"""
    
    print("\n" + "="*70)
    print("PLANT DISEASE DIAGNOSIS - DEMONSTRATION")
    print("="*70)
    
    diagnosis = PlantDiseaseDiagnosis()
    
    # Scenario 1: Tomato with early blight symptoms
    print("\n\n📋 SCENARIO 1: Tomato Plant with Leaf Spots")
    print("-"*70)
    
    plant_type = "tomato"
    symptoms = [
        "dark spots on leaves",
        "concentric rings on leaves", 
        "yellowing around spots",
        "lower leaves affected first"
    ]
    additional_info = {
        'weather': 'humid',
        'watering': 'overhead',
        'severity': 'moderate'
    }
    
    print(f"Plant Type: {plant_type}")
    print(f"Symptoms: {', '.join(symptoms)}")
    print(f"Weather: {additional_info['weather']}")
    print(f"Watering: {additional_info['watering']}")
    print(f"Severity: {additional_info['severity']}")
    print("\n" + "="*70)
    
    result = diagnosis.diagnose(plant_type, symptoms, additional_info)
    report = diagnosis.generate_report(result)
    print(report)
    
    # Save report
    filename = f"diagnosis_report_tomato_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, 'w') as f:
        f.write(report)
    print(f"\n✓ Report saved to: {filename}\n")
    
    # Scenario 2: Apple tree with powdery mildew
    print("\n\n📋 SCENARIO 2: Apple Tree with White Coating")
    print("-"*70)
    
    plant_type = "apple"
    symptoms = [
        "white powdery coating on leaves",
        "distorted new growth",
        "stunted shoots"
    ]
    additional_info = {
        'weather': 'dry',
        'watering': 'soil-level',
        'severity': 'mild'
    }
    
    print(f"Plant Type: {plant_type}")
    print(f"Symptoms: {', '.join(symptoms)}")
    print(f"Weather: {additional_info['weather']}")
    print(f"Watering: {additional_info['watering']}")
    print(f"Severity: {additional_info['severity']}")
    print("\n" + "="*70)
    
    result = diagnosis.diagnose(plant_type, symptoms, additional_info)
    report = diagnosis.generate_report(result)
    print(report)
    
    # Save report
    filename = f"diagnosis_report_apple_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    with open(filename, 'w') as f:
        f.write(report)
    print(f"\n✓ Report saved to: {filename}\n")
    
    # Scenario 3: Healthy tomato plant
    print("\n\n📋 SCENARIO 3: Healthy Tomato Plant")
    print("-"*70)
    
    plant_type = "tomato"
    symptoms = [
        "vibrant green leaves",
        "steady growth",
        "no unusual spots"
    ]
    additional_info = {
        'weather': 'sunny',
        'watering': 'soil-level',
        'severity': 'none'
    }
    
    print(f"Plant Type: {plant_type}")
    print(f"Symptoms: {', '.join(symptoms)}")
    print("\n" + "="*70)
    
    result = diagnosis.diagnose(plant_type, symptoms, additional_info)
    report = diagnosis.generate_report(result)
    print(report)
    
    print("\n" + "="*70)
    print("DEMONSTRATION COMPLETE")
    print("="*70)
    print("\nTo run your own diagnosis, use:")
    print("  python main.py diagnose")
    print("\nOr provide specific data programmatically:")
    print("""
from text_diagnosis import PlantDiseaseDiagnosis

diagnosis = PlantDiseaseDiagnosis()
result = diagnosis.diagnose(
    plant_type="tomato",
    symptoms=["dark spots", "yellowing leaves"],
    additional_info={'weather': 'humid', 'severity': 'moderate'}
)
report = diagnosis.generate_report(result)
print(report)
""")


if __name__ == "__main__":
    demo_diagnosis()
