---
title: Aura Lab - Scalable Materials Discovery
emoji: 🏭
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
---

# 🚀 Aura Lab v5: AI-Powered **Scalable** Materials Discovery

Find materials that are not just high-performance, but also **ready for industrial production**!

## 🆕 What's New in v5

### Manufacturing Scalability Score

We now evaluate not just **performance**, but also **commercial viability**. The Scalability Score addresses the #1 bottleneck identified by industry experts: **translating lab discoveries to industrial production**.

**Three Core Metrics:**
- 📦 **Element Abundance Index (40%)** - Supply chain risk assessment
- ⚙️ **Synthesis Complexity Index (35%)** - Manufacturing cost estimation
- 🔧 **Manufacturing Integration Score (25%)** - Production compatibility

## Features

- 🎯 **Test a Material**: Get instant predictions for performance AND scalability
- 🏆 **AI's Best Picks**: Top 10 materials ranked by scalability
- 🏭 **Scalability Insights**: Detailed breakdown of commercial viability
- ℹ️ **Research-Backed**: Based on MIT/Berkeley manufacturing study

## Predicted Properties

1. **⚡ Ionic Conductivity**: How fast lithium ions move (mS/cm)
2. **🏗️ Thermodynamic Stability**: How stable the material is (eV/atom)
3. **💎 Band Gap**: Insulating properties (eV)
4. **🏭 Scalability Score**: Commercial viability (0-10)

## Scalability Score Interpretation

| Score | Classification | Meaning |
|-------|---------------|---------|
| 8.0-10.0 | **Highly Scalable** | Ready for near-term commercialization |
| 6.0-7.9 | **Scalable** | Viable with moderate development |
| 4.0-5.9 | **Challenging** | Significant barriers to scale-up |
| 0.0-3.9 | **Not Scalable** | Fundamental scalability issues |

## Technology

- **Models**: Random Forest, Gradient Boosting, XGBoost
- **Dataset**: 21,307 lithium materials from Materials Project
- **Features**: 41 engineered features + scalability metrics
- **Performance**: R²=0.715 (conductivity), R²=0.708 (stability), R²=0.552 (band gap)
- **Scalability Data**: CRC Handbook, USGS, MIT/Berkeley research

## Example: Li6PS5Cl (Sulfide Electrolyte)

**Performance:**
- Conductivity: 8.5 mS/cm ⭐⭐⭐⭐⭐
- Stability: -0.3 eV/atom ⭐⭐⭐⭐
- Band Gap: 3.2 eV ⭐⭐⭐⭐⭐

**Scalability: 6.58/10 - Scalable**
- Element Abundance Index: 6.58/10 (Li is moderately abundant)
- Synthesis Complexity Index: 7.0/10 (550°C, 3 steps)
- Manufacturing Integration Score: 6.0/10 (Requires buffer layers)

## Research Foundation

**"Manufacturing scalability implications of materials choice in inorganic solid-state batteries"**  
Huang, Ceder, Olivetti (MIT/Berkeley, 2021)  
*Joule*, Volume 5, Issue 3

## About Aura Lab

We're building an AI-accelerated materials discovery platform that finds not just high-performance materials, but **commercially viable, scalable materials** ready for industrial production.

**Mission**: Accelerate the energy transition by discovering battery materials that can actually reach the market.

---

**Developed by:** Aura Lab  
**Powered by:** Gradio + Pymatgen + Scikit-learn + XGBoost  
**Live Demo:** https://aura-lab-demo.onrender.com
