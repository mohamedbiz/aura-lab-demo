"""
Scalability Score Calculator for AURA Lab
Calculates manufacturing scalability scores for predicted materials
"""

import json
import re
from typing import Dict, List, Tuple
from pymatgen.core import Composition


class ScalabilityCalculator:
    """Calculate scalability scores for battery materials"""
    
    def __init__(self, element_data_path='element_data.json', 
                 material_class_data_path='material_class_data.json'):
        """Initialize with element and material class databases"""
        with open(element_data_path, 'r') as f:
            self.element_db = json.load(f)
        
        with open(material_class_data_path, 'r') as f:
            self.material_class_db = json.load(f)
    
    def calculate_element_abundance_index(self, formula: str) -> Tuple[float, Dict]:
        """
        Calculate Element Abundance Index (EAI) for a material
        
        Args:
            formula: Chemical formula (e.g., "Li6PS5Cl")
        
        Returns:
            (eai_score, details_dict)
        """
        try:
            comp = Composition(formula)
        except:
            # Fallback for invalid formulas
            return 5.0, {"error": "Invalid formula"}
        
        element_scores = []
        element_details = []
        total_atoms = sum(comp.values())
        
        for element, count in comp.items():
            element_symbol = str(element)
            atomic_fraction = count / total_atoms
            
            if element_symbol in self.element_db['elements']:
                elem_data = self.element_db['elements'][element_symbol]
                abundance_score = elem_data['abundance_score']
                supply_chain_score = elem_data['supply_chain_score']
                
                # Element score = (abundance × 0.6) + (supply chain × 0.4)
                element_score = (abundance_score * 0.6) + (supply_chain_score * 0.4)
                
                element_scores.append(element_score * atomic_fraction)
                element_details.append({
                    'element': element_symbol,
                    'atomic_fraction': round(atomic_fraction, 3),
                    'crustal_abundance_ppm': elem_data['crustal_abundance_ppm'],
                    'abundance_score': abundance_score,
                    'supply_chain_score': supply_chain_score,
                    'element_score': round(element_score, 2)
                })
            else:
                # Unknown element - assign moderate score
                element_scores.append(5.0 * atomic_fraction)
                element_details.append({
                    'element': element_symbol,
                    'atomic_fraction': round(atomic_fraction, 3),
                    'element_score': 5.0,
                    'note': 'Unknown element - default score'
                })
        
        eai = sum(element_scores)
        
        return round(eai, 2), {
            'elements': element_details,
            'weighted_average': round(eai, 2)
        }
    
    def classify_material(self, formula: str) -> str:
        """
        Classify material into a category for synthesis complexity estimation
        
        Args:
            formula: Chemical formula
        
        Returns:
            material_class key
        """
        formula_lower = formula.lower()
        
        # Simple heuristic classification
        if 's' in formula_lower and ('p' in formula_lower or 'cl' in formula_lower or 'br' in formula_lower):
            return 'sulfide_electrolytes'
        elif 'zr' in formula_lower and 'o' in formula_lower:
            return 'oxide_electrolytes_garnet'
        elif ('ti' in formula_lower or 'ta' in formula_lower) and 'o' in formula_lower:
            return 'oxide_electrolytes_perovskite'
        elif ('p' in formula_lower or 'si' in formula_lower) and 'o' in formula_lower:
            return 'oxide_electrolytes_nasicon'
        elif 'co' in formula_lower and 'o' in formula_lower:
            return 'layered_cathodes'
        elif 'mn' in formula_lower and 'o' in formula_lower:
            return 'spinel_cathodes'
        elif 'fe' in formula_lower and 'p' in formula_lower and 'o' in formula_lower:
            return 'olivine_cathodes'
        else:
            return 'default'
    
    def calculate_synthesis_complexity_index(self, formula: str) -> Tuple[float, Dict]:
        """
        Calculate Synthesis Complexity Index (SCI) for a material
        
        Args:
            formula: Chemical formula
        
        Returns:
            (sci_score, details_dict)
        """
        material_class = self.classify_material(formula)
        class_data = self.material_class_db['material_classes'][material_class]
        
        temperature_penalty = class_data['temperature_penalty']
        step_penalty = class_data['step_penalty']
        equipment_penalty = class_data['equipment_penalty']
        
        sci = 10 - (temperature_penalty + step_penalty + equipment_penalty)
        sci = max(0, min(10, sci))  # Clamp to [0, 10]
        
        return round(sci, 2), {
            'material_class': class_data['name'],
            'typical_temperature_c': class_data['typical_temperature_c'],
            'temperature_penalty': temperature_penalty,
            'synthesis_steps': class_data['typical_steps'],
            'step_penalty': step_penalty,
            'equipment_level': class_data['equipment_level'],
            'equipment_penalty': equipment_penalty,
            'total_penalty': temperature_penalty + step_penalty + equipment_penalty
        }
    
    def calculate_manufacturing_integration_score(self, formula: str) -> Tuple[float, Dict]:
        """
        Calculate Manufacturing Integration Score (MIS) for a material
        
        Args:
            formula: Chemical formula
        
        Returns:
            (mis_score, details_dict)
        """
        material_class = self.classify_material(formula)
        class_data = self.material_class_db['material_classes'][material_class]
        
        interface_stability = class_data['interface_stability_score']
        process_compatibility = class_data['process_compatibility_score']
        scale_demonstration = class_data['scale_demonstration_score']
        
        mis = (interface_stability + process_compatibility + scale_demonstration) / 3
        
        return round(mis, 2), {
            'interface_stability_score': interface_stability,
            'process_compatibility_score': process_compatibility,
            'scale_demonstration_score': scale_demonstration
        }
    
    def calculate_scalability_score(self, formula: str) -> Dict:
        """
        Calculate complete Scalability Score for a material
        
        Args:
            formula: Chemical formula
        
        Returns:
            Complete scoring dictionary
        """
        # Calculate three core metrics
        eai, eai_details = self.calculate_element_abundance_index(formula)
        sci, sci_details = self.calculate_synthesis_complexity_index(formula)
        mis, mis_details = self.calculate_manufacturing_integration_score(formula)
        
        # Weighted average: EAI (40%) + SCI (35%) + MIS (25%)
        scalability_score = (eai * 0.40) + (sci * 0.35) + (mis * 0.25)
        scalability_score = round(scalability_score, 2)
        
        # Classification
        if scalability_score >= 8.0:
            classification = "Highly Scalable"
            color = "#10b981"  # green
        elif scalability_score >= 6.0:
            classification = "Scalable"
            color = "#3b82f6"  # blue
        elif scalability_score >= 4.0:
            classification = "Challenging"
            color = "#f59e0b"  # orange
        else:
            classification = "Not Scalable"
            color = "#ef4444"  # red
        
        return {
            'formula': formula,
            'scalability_score': scalability_score,
            'classification': classification,
            'color': color,
            'metrics': {
                'element_abundance_index': {
                    'score': eai,
                    'weight': 0.40,
                    'contribution': round(eai * 0.40, 2),
                    'details': eai_details
                },
                'synthesis_complexity_index': {
                    'score': sci,
                    'weight': 0.35,
                    'contribution': round(sci * 0.35, 2),
                    'details': sci_details
                },
                'manufacturing_integration_score': {
                    'score': mis,
                    'weight': 0.25,
                    'contribution': round(mis * 0.25, 2),
                    'details': mis_details
                }
            }
        }


# Convenience function for quick calculations
def calculate_scalability(formula: str, 
                         element_data_path='element_data.json',
                         material_class_data_path='material_class_data.json') -> Dict:
    """
    Quick function to calculate scalability score
    
    Args:
        formula: Chemical formula
        element_data_path: Path to element database
        material_class_data_path: Path to material class database
    
    Returns:
        Scalability score dictionary
    """
    calculator = ScalabilityCalculator(element_data_path, material_class_data_path)
    return calculator.calculate_scalability_score(formula)


if __name__ == "__main__":
    # Test the calculator
    calculator = ScalabilityCalculator()
    
    test_formulas = [
        "Li6PS5Cl",  # Sulfide electrolyte
        "NaLiTm2F8",  # Novel discovery
        "LiFePO4",  # Olivine cathode
        "LiCoO2",  # Layered cathode
    ]
    
    print("=" * 80)
    print("AURA Lab Scalability Score Calculator - Test Results")
    print("=" * 80)
    
    for formula in test_formulas:
        result = calculator.calculate_scalability_score(formula)
        print(f"\nFormula: {formula}")
        print(f"Scalability Score: {result['scalability_score']}/10")
        print(f"Classification: {result['classification']}")
        print(f"  - Element Abundance Index: {result['metrics']['element_abundance_index']['score']}/10")
        print(f"  - Synthesis Complexity Index: {result['metrics']['synthesis_complexity_index']['score']}/10")
        print(f"  - Manufacturing Integration Score: {result['metrics']['manufacturing_integration_score']['score']}/10")
        print("-" * 80)
