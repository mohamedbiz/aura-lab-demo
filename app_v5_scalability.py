"""
Aura Lab PIML v5 - With Scalability Score
Features:
- Same UI as v4
- Mock predictions for instant deployment
- NEW: Scalability Score based on Professor Dolatabadi's insight
- Industry-ready materials discovery
"""

import gradio as gr
import numpy as np
import json
from pymatgen.core import Composition, Element
from scalability_calculator import ScalabilityCalculator

# Load Pareto-optimal hypotheses
with open('asa_hypotheses_v2_optimized.json', 'r') as f:
    hypotheses = json.load(f)

# Initialize scalability calculator
scalability_calc = ScalabilityCalculator()

print("✅ Aura Lab v5 with Scalability Score loaded successfully!")

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
    """Generate mock predictions with Scalability Score."""
    try:
        avg_z, avg_mass, n_elements = extract_features(composition, space_group, a, b, c, alpha, beta, gamma)
        
        if avg_z is None:
            return "❌ Invalid composition formula. Please use standard chemical notation (e.g., LiCoO2, NaLiTm2F8)."
        
        # Mock predictions based on simple heuristics
        conductivity = max(0.1, 10.0 - (avg_mass / 20.0)) + np.random.uniform(-0.5, 0.5)
        stability = -2.0 + (n_elements * 0.3) + np.random.uniform(-0.2, 0.2)
        band_gap = max(0.0, (avg_z / 30.0) * 3.0) + np.random.uniform(-0.3, 0.3)
        
        # Calculate Scalability Score
        scalability_result = scalability_calc.calculate_scalability_score(composition)
        scalability_score = scalability_result['scalability_score']
        classification = scalability_result['classification']
        
        # Get metric details
        eai = scalability_result['metrics']['element_abundance_index']['score']
        sci = scalability_result['metrics']['synthesis_complexity_index']['score']
        mis = scalability_result['metrics']['manufacturing_integration_score']['score']
        
        result = f"""
## 🔮 Predicted Properties for **{composition}**

### ⚡ Ionic Conductivity
**{conductivity:.2f} mS/cm** - {"✅ Excellent" if conductivity > 5 else "⚠️ Moderate" if conductivity > 2 else "❌ Low"}

### 🏗️ Thermodynamic Stability  
**{stability:.3f} eV/atom** - {"✅ Stable" if stability > -0.5 else "⚠️ Metastable" if stability > -1.5 else "❌ Unstable"}

### 🌈 Band Gap
**{band_gap:.2f} eV** - {"✅ Insulator" if band_gap > 3 else "⚠️ Semiconductor" if band_gap > 0.5 else "❌ Conductor"}

---

## 🏭 Manufacturing Scalability Score

### Overall Score: **{scalability_score}/10** - {classification}

This score evaluates how easily this material can scale from lab to commercial production, based on:

#### 📦 Element Abundance Index: **{eai}/10**
- Measures availability and supply chain maturity of constituent elements
- Higher scores indicate abundant, accessible materials

#### ⚙️ Synthesis Complexity Index: **{sci}/10**
- Evaluates manufacturing difficulty (temperature, steps, equipment)
- Higher scores indicate simpler, lower-cost processes

#### 🔧 Manufacturing Integration Score: **{mis}/10**
- Assesses compatibility with existing battery manufacturing
- Higher scores indicate easier integration into production lines

---

### 📊 Structure Parameters
- **Space Group:** {space_group}
- **Lattice:** a={a:.2f}Å, b={b:.2f}Å, c={c:.2f}Å
- **Angles:** α={alpha}°, β={beta}°, γ={gamma}°

---

**💡 Insight:** The Scalability Score addresses the #1 bottleneck in materials commercialization: **translating lab discoveries to industrial production**.

**Note:** This is a demo version with mock property predictions. Scalability scores use real data from Materials Project and industry research.
"""
        return result
        
    except Exception as e:
        return f"❌ Error: {str(e)}"

def show_top_candidates():
    """Display top Pareto-optimal candidates with scalability scores."""
    result = "# 🏆 Top 10 Pareto-Optimal Candidates\n\n"
    result += "These materials were discovered through multi-objective optimization and ranked by scalability:\n\n"
    
    # Calculate scalability for all hypotheses
    hyp_with_scalability = []
    for hyp in hypotheses[:10]:
        try:
            scalability_result = scalability_calc.calculate_scalability_score(hyp['composition'])
            hyp['scalability_score'] = scalability_result['scalability_score']
            hyp['scalability_class'] = scalability_result['classification']
            hyp_with_scalability.append(hyp)
        except:
            hyp['scalability_score'] = 0
            hyp['scalability_class'] = "Unknown"
            hyp_with_scalability.append(hyp)
    
    # Sort by scalability score
    hyp_with_scalability.sort(key=lambda x: x['scalability_score'], reverse=True)
    
    for i, hyp in enumerate(hyp_with_scalability, 1):
        result += f"### {i}. **{hyp['composition']}** - Scalability: {hyp['scalability_score']}/10 ({hyp['scalability_class']})\n"
        result += f"- **Conductivity:** {hyp['conductivity']:.2f} mS/cm\n"
        result += f"- **Stability:** {hyp['stability']:.3f} eV/atom\n"
        result += f"- **Band Gap:** {hyp['band_gap']:.2f} eV\n"
        result += f"- **Space Group:** {hyp['space_group']}\n\n"
    
    return result

# Create Gradio interface
with gr.Blocks(title="Aura Lab - Scalable Materials Discovery") as demo:
    gr.Markdown("""
    # 🧪 Aura Lab - AI-Powered **Scalable** Materials Discovery
    
    ## Discover Next-Generation Battery Materials Ready for Industrial Production
    
    This platform uses **Physics-Informed Machine Learning (PIML)** to predict material properties **AND** evaluate manufacturing scalability.
    
    ### 🚀 What's New in v5:
    - ✨ **Scalability Score** - Evaluates commercial viability
    - 📦 **Element Abundance Analysis** - Identifies supply chain risks
    - ⚙️ **Synthesis Complexity Assessment** - Estimates manufacturing costs
    - 🔧 **Integration Readiness** - Measures production compatibility
    
    ### How It Works:
    1. **Enter a chemical formula** (e.g., LiCoO2, NaLiTm2F8)
    2. **Adjust structure parameters** (optional)
    3. **Get instant predictions** for performance AND scalability
    
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
                
                predict_btn = gr.Button("🚀 Predict Properties + Scalability", variant="primary", size="lg")
            
            with gr.Column():
                output = gr.Markdown(label="Prediction Results")
        
        predict_btn.click(
            fn=predict_properties,
            inputs=[composition_input, space_group_input, a_input, b_input, c_input, alpha_input, beta_input, gamma_input],
            outputs=output
        )
    
    with gr.Tab("🏆 Top Discoveries"):
        gr.Markdown("## AI-Discovered Pareto-Optimal Materials (Ranked by Scalability)")
        top_candidates_output = gr.Markdown()
        show_btn = gr.Button("📊 Show Top 10 Candidates", variant="primary")
        show_btn.click(fn=show_top_candidates, outputs=top_candidates_output)
    
    with gr.Tab("🏭 About Scalability Score"):
        gr.Markdown("""
        ## What is the Scalability Score?
        
        The **Scalability Score** addresses the #1 bottleneck in materials commercialization: **translating promising lab discoveries into real-world industrial production**.
        
        ### Why It Matters
        
        According to industry experts, **scalability is the single biggest challenge** in bringing new battery materials to market. A material might show excellent performance in the lab, but fail to scale due to:
        - Rare or expensive elements
        - Complex, energy-intensive synthesis
        - Incompatibility with existing manufacturing processes
        
        ### The Three Core Metrics
        
        #### 1. **Element Abundance Index (EAI)** - Weight: 40%
        
        Evaluates the natural availability and supply chain maturity of constituent elements.
        
        **Data Points:**
        - **Crustal Abundance (ppm)**: How common is each element in Earth's crust?
        - **Supply Chain Maturity**: Is production established, concentrated, or constrained?
        
        **Example:**
        - Sodium (23,600 ppm, mature supply) → High score
        - Germanium (1.5 ppm, by-product metal) → Low score
        
        ---
        
        #### 2. **Synthesis Complexity Index (SCI)** - Weight: 35%
        
        Assesses the difficulty and cost of manufacturing the material.
        
        **Data Points:**
        - **Processing Temperature**: Lower temperatures = lower energy costs
        - **Number of Synthesis Steps**: Fewer steps = higher yields
        - **Equipment Requirements**: Standard equipment = easier scale-up
        
        **Example:**
        - Sulfide electrolytes (550°C, 3 steps, standard equipment) → High score
        - Garnet electrolytes (1100°C, 4 steps, specialized equipment) → Lower score
        
        ---
        
        #### 3. **Manufacturing Integration Score (MIS)** - Weight: 25%
        
        Measures how easily the material integrates into battery production lines.
        
        **Data Points:**
        - **Interface Stability**: Does it react with other battery components?
        - **Process Compatibility**: Can existing equipment be used?
        - **Scale Demonstration**: Has it been produced at pilot or commercial scale?
        
        **Example:**
        - LiFePO4 (olivine cathode) → High score (commercial production)
        - Novel perovskites → Low score (lab-scale only)
        
        ---
        
        ### Score Interpretation
        
        | Score Range | Classification | Meaning |
        |------------|---------------|---------|
        | 8.0 - 10.0 | **Highly Scalable** | Ready for near-term commercialization |
        | 6.0 - 7.9 | **Scalable** | Viable with moderate development |
        | 4.0 - 5.9 | **Challenging** | Significant barriers to scale-up |
        | 0.0 - 3.9 | **Not Scalable** | Fundamental scalability issues |
        
        ---
        
        ### Data Sources
        
        - **Element Abundance**: CRC Handbook of Chemistry and Physics, USGS Commodity Statistics
        - **Supply Chain Data**: MIT/Berkeley research (Huang, Ceder, Olivetti, 2021)
        - **Synthesis Parameters**: Literature review of 100+ battery materials papers
        - **Manufacturing Data**: Industry reports, company announcements, patent filings
        
        ---
        
        **By incorporating the Scalability Score, Aura Lab transforms from a research tool into an industry-ready platform for practical, commercially viable materials discovery.** 🚀
        """)
    
    with gr.Tab("ℹ️ About"):
        gr.Markdown("""
        ## About This Demo
        
        This is **version 5** of the Aura Lab materials discovery platform, now featuring **Manufacturing Scalability Assessment**.
        
        ### Technology Stack:
        - **Physics-Informed Machine Learning (PIML)**
        - **Materials Project Database** (21,307 lithium compounds)
        - **Multi-Objective Optimization** (Pareto frontier)
        - **Scalability Framework** (based on MIT/Berkeley research)
        - **Pymatgen** for materials science calculations
        
        ### Model Performance (Full Version):
        - Conductivity Model: R² = 0.715
        - Stability Model: R² = 0.708
        - Band Gap Model: R² = 0.552
        
        ### Features:
        - ✅ Real-time property prediction
        - ✅ Manufacturing scalability assessment
        - ✅ 50 Pareto-optimal candidates
        - ✅ Interactive structure parameter tuning
        - ✅ Materials science validation
        - ✅ Industry-ready insights
        
        ---
        
        **Note:** This demo uses mock property predictions for instant deployment. Scalability scores use real data from peer-reviewed research and industry sources.
        
        **Developed by:** Aura Lab  
        **Powered by:** Gradio + Pymatgen + Scikit-learn + XGBoost  
        **Research Foundation:** MIT/Berkeley Manufacturing Scalability Study (2021)
        """)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
