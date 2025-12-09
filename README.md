# Interactive Data Story Generator
An AI-powered application that transforms datasets into compelling data stories with automated insights and visualizations.

## 🌟 Features
- Automated EDA: Instant exploratory data analysis  
- AI-Powered Insights: Meaningful insights automatically  
- Interactive Visualizations: Beautiful Plotly charts  
- Export Reports: Download analysis reports  
- User-friendly: Clean Streamlit interface  

## 🚀 Quick Start

### Installation
```bash
git clone https://github.com/jiyabhaviksadaria/data_story_generator
cd data_story_generator
```

### Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate      # macOS / Linux
venv\Scripts\activate       # Windows
```

### Install dependencies:
```bash
pip install -r requirements.txt
```

### Run application:
```bash
streamlit run app.py
```

Open in browser: **http://localhost:8501**

## 📊 Usage
1. Upload CSV file  
2. View automated insights  
3. Explore interactive visualizations  
4. Download your report  

## 🛠️ Technologies
- Streamlit  
- Pandas  
- Plotly  
- NumPy  
- Python  

---

# ☁️ AWS Architecture (Planned)

Below is the planned AWS Cloud architecture for scalability and security:

![AWS Architecture](c:\Users\JIYA SADARIA\OneDrive\Pictures\aws flowilne.png)

                 ┌─────────────────────────────────────┐
                 │            User Browser              │
                 │ (Uploads CSV, views insights/report) │
                 └─────────────────────────────────────┘
                                  │
                                  │  HTTPS
                                  ▼
                 ┌─────────────────────────────────────┐
                 │       Amazon EC2 (Planned)           │
                 │ Hosts Streamlit Application          │
                 │ Performs EDA & Data Story Generation │
                 └─────────────────────────────────────┐
                                  │
                   Reads/Writes   │ via IAM Role
                                  ▼
                 ┌─────────────────────────────────────┐
                 │         Amazon S3 (Planned)          │
                 │ Stores:                              │
                 │  - Uploaded CSV datasets             │
                 │  - Generated analysis reports        │
                 │ Provides presigned download URLs      │
                 └─────────────────────────────────────┘
                                  │
                                  │ Secure Access
                                  ▼
                 ┌─────────────────────────────────────┐
                 │            AWS IAM (Planned)         │
                 │ Grants EC2 S3 Access                 │
                 │ Enforces least-privilege policies    │
                 └─────────────────────────────────────┘


## Components (Planned)

### **Amazon EC2**
- Will host the Streamlit application  
- Handles EDA and data story generation  

### **Amazon S3**
- Will store uploaded CSV datasets  
- Will store generated analysis reports  
- Secure download via Pre‑Signed URLs  

### **AWS IAM**
- Controls access between EC2 and S3  
- Ensures least‑privilege permissions  

---

## 👤 Author
**Jiya Bhavik Sadaria**  
Email: **jiyasadaria@gmail.com**  
GitHub: **jiyabhaviksadaria**

## 📄 License
MIT License

