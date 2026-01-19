"""
Aura Lab PIML v4 Demo - Simplified Version
Features:
- Same UI as full version
- Mock predictions for instant deployment
- No large model files needed
"""

import gradio as gr
import numpy as np
import json
from pymatgen.core import Composition, Element

# Load Pareto-optimal hypotheses
with open('asa_hypotheses_v2_optimized.json', 'r') as f:
    hypotheses = json.load(f)

print("Demo loaded successfully!")

def extract_features(composition, space_group=216, a=9.9, b=9.9, c=9.9, alpha=90, beta=90, gamma=90):
    """Extract features from composition and structure for mock prediction."""
    try:
        comp = Composition(composition)
        elements = [Element(el) for el in comp.elements]
        fractions = [comp.get_atomic_fraction(el) for el in comp.elements]
        
        # Simple feature extraction for mock predictions
        avg_atomic_number = np.average([el.Z for el in elements], weights=fractions)
        avg_atomic_mass = np.average([el.atomic_mass for el in elements], weights=fractions)
        
        return avg_atomic_number, avg_atomic_mass, len(elements)
    except Exception as e:
        return None, None, None

def predict_properties(composition, space_group, a, b, c, alpha, beta, gamma):
    """Generate mock predictions based on composition features."""
    try:
        avg_z, avg_mass, n_elements = extract_features(composition, space_group, a, b, c, alpha, beta, gamma)
        
        if avg_z is None:
            return "❌ Invalid composition formula. Please use standard chemical notation (e.g., LiCoO2, NaLiTm2F8)."
        
        # Mock predictions based on simple heuristics
        # Conductivity: higher for lighter elements
        conductivity = max(0.1, 10.0 - (avg_mass / 20.0)) + np.random.uniform(-0.5, 0.5)
        
        # Stability: more stable with more elements
        stability = -2.0 + (n_elements * 0.3) + np.random.uniform(-0.2, 0.2)
        
        # Band gap: higher for heavier elements
        band_gap = max(0.0, (avg_z / 30.0) * 3.0) + np.random.uniform(-0.3, 0.3)
        
        result = f"""
## 🔮 Predicted Properties for **{composition}**

### ⚡ Ionic Conductivity
**{conductivity:.2f} mS/cm** - {"✅ Excellent" if conductivity > 5 else "⚠️ Moderate" if conductivity > 2 else "❌ Low"}

### 🏗️ Thermodynamic Stability  
**{stability:.3f} eV/atom** - {"✅ Stable" if stability > -0.5 else "⚠️ Metastable" if stability > -1.5 else "❌ Unstable"}

### 🌈 Band Gap
**{band_gap:.2f} eV** - {"✅ Insulator" if band_gap > 3 else "⚠️ Semiconductor" if band_gap > 0.5 else "❌ Conductor"}

---

### 📊 Structure Parameters
- **Space Group:** {space_group}
- **Lattice:** a={a:.2f}Å, b={b:.2f}Å, c={c:.2f}Å
- **Angles:** α={alpha}°, β={beta}°, γ={gamma}°

---

**Note:** This is a demo version with mock predictions. For production use, integrate trained ML models.
"""
        return result
        
    except Exception as e:
        return f"❌ Error: {str(e)}"

def show_top_candidates():
    """Display top Pareto-optimal candidates."""
    result = "# 🏆 Top 10 Pareto-Optimal Candidates\n\n"
    result += "These materials were discovered through multi-objective optimization:\n\n"
    
    for i, hyp in enumerate(hypotheses[:10], 1):
        result += f"### {i}. **{hyp['composition']}**\n"
        result += f"- **Conductivity:** {hyp['conductivity']:.2f} mS/cm\n"
        result += f"- **Stability:** {hyp['stability']:.3f} eV/atom\n"
        result += f"- **Band Gap:** {hyp['band_gap']:.2f} eV\n"
        result += f"- **Space Group:** {hyp['space_group']}\n\n"
    
    return result

# Create Gradio interface
with gr.Blocks(title="Aura Lab - AI Materials Discovery", theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🧪 Aura Lab - AI-Powered Materials Discovery
    
    ## Discover Next-Generation Battery Materials
    
    This demo uses **Physics-Informed Machine Learning (PIML)** to predict material properties for solid-state battery electrolytes.
    
    ### How It Works:
    1. **Enter a chemical formula** (e.g., LiCoO2, NaLiTm2F8)
    2. **Adjust structure parameters** (optional)
    3. **Get instant predictions** for conductivity, stability, and band gap
    
    ---
    """)
    
    with gr.Tab("🔬 Predict Properties"):
        with gr.Row():
            with gr.Column():
                composition_input = gr.Textbox(
                    label="Chemical Formula",
                    placeholder="e.g., LiCoO2, NaLiTm2F8, Li7La3Zr2O12",
                    value="NaLiTm2F8"
                )
                
                with gr.Accordion("⚙️ Advanced Structure Parameters", open=False):
                    space_group_input = gr.Number(label="Space Group", value=216)
                    with gr.Row():
                        a_input = gr.Number(label="a (Å)", value=9.9)
                        b_input = gr.Number(label="b (Å)", value=9.9)
                        c_input = gr.Number(label="c (Å)", value=9.9)
                    with gr.Row():
                        alpha_input = gr.Number(label="α (°)", value=90)
                        beta_input = gr.Number(label="β (°)", value=90)
                        gamma_input = gr.Number(label="γ (°)", value=90)
                
                predict_btn = gr.Button("🚀 Predict Properties", variant="primary", size="lg")
            
            with gr.Column():
                output = gr.Markdown(label="Prediction Results")
        
        predict_btn.click(
            fn=predict_properties,
            inputs=[composition_input, space_group_input, a_input, b_input, c_input, alpha_input, beta_input, gamma_input],
            outputs=output
        )
    
    with gr.Tab("🏆 Top Discoveries"):
        gr.Markdown("## AI-Discovered Pareto-Optimal Materials")
        top_candidates_output = gr.Markdown()
        show_btn = gr.Button("📊 Show Top 10 Candidates", variant="primary")
        show_btn.click(fn=show_top_candidates, outputs=top_candidates_output)
    
    with gr.Tab("ℹ️ About"):
        gr.Markdown("""
        ## About This Demo
        
        This is a **simplified demonstration version** of the Aura Lab materials discovery platform.
        
        ### Technology Stack:
        - **Physics-Informed Machine Learning (PIML)**
        - **Materials Project Database** (21,307 lithium compounds)
        - **Multi-Objective Optimization** (Pareto frontier)
        - **Pymatgen** for materials science calculations
        
        ### Model Performance (Full Version):
        - Conductivity Model: R² = 0.715
        - Stability Model: R² = 0.708
        - Band Gap Model: R² = 0.552
        
        ### Features:
        - ✅ Real-time property prediction
        - ✅ 50 Pareto-optimal candidates
        - ✅ Interactive structure parameter tuning
        - ✅ Materials science validation
        
        ---
        
        **Note:** This demo uses mock predictions for instant deployment. The full version with trained models is available for download.
        
        **Developed by:** Aura Lab  
        **Powered by:** Gradio + Pymatgen + Scikit-learn + XGBoost
        """)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
