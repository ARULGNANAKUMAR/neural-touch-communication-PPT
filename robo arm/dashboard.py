import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import random
import time

# Page configuration
st.set_page_config(
    page_title="🏭 AI Smart Factory 4.0 Dashboard",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    /* Main container styling */
    .main {
        background: linear-gradient(135deg, #0a0f1e 0%, #141b2b 100%);
        padding: 20px;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(145deg, #1a1f2f 0%, #242a3a 100%);
        border-left: 4px solid;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        margin: 10px 0;
    }
    
    .metric-title {
        color: #a0a0a0;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .metric-value {
        font-size: 32px;
        font-weight: bold;
        margin: 5px 0;
    }
    
    .metric-trend {
        font-size: 12px;
        color: #4ecdc4;
    }
    
    /* KPI cards */
    .kpi-card {
        background: #1a1f2f;
        border: 1px solid;
        border-radius: 12px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    
    .kpi-title {
        color: #888;
        font-size: 11px;
        margin-bottom: 5px;
    }
    
    .kpi-value {
        font-size: 24px;
        font-weight: bold;
    }
    
    /* Status indicators */
    .status-critical {
        background: #ff6b6b;
        color: white;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        text-align: center;
    }
    
    .status-warning {
        background: #ff9f43;
        color: white;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        text-align: center;
    }
    
    .status-caution {
        background: #4ecdc4;
        color: white;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        text-align: center;
    }
    
    .status-normal {
        background: #00d4ff;
        color: white;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        text-align: center;
    }
    
    /* Headers */
    .section-header {
        color: #00d4ff;
        font-size: 18px;
        font-weight: bold;
        margin: 20px 0 10px 0;
        padding-bottom: 10px;
        border-bottom: 2px solid #2a2f3f;
    }
    
    /* Prediction box */
    .prediction-box {
        background: linear-gradient(145deg, #1e2436 0%, #2a2f3f 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        border: 1px solid;
    }
    
    /* DateTime */
    .datetime {
        color: #888;
        font-size: 14px;
        text-align: right;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for data persistence
if 'temp_data' not in st.session_state:
    st.session_state.temp_data = []
    st.session_state.stress_data = []
    st.session_state.risk_data = []
    st.session_state.energy_data = []
    st.session_state.timestamps = []
    st.session_state.machine_data = {}
    st.session_state.employee_data = {}

# Employee names
EMPLOYEES = ["Akash", "Radhakrishina", "Vijayaraja", "Selvaragavan", "Shyam Antonyraj", "Karthik"]

# Machine types
MACHINES = ["CNC Mill", "Lathe", "Press", "Robot Arm", "Conveyor", "Packager", "Welder", "Assembler"]

def generate_data():
    """Generate realistic factory data"""
    timestamp = datetime.now()
    
    # Temperature with trend
    base_temp = 65 + random.uniform(-5, 15)
    temp = base_temp + random.uniform(-2, 2)
    
    # Stress with trend
    base_stress = 85 + random.uniform(-10, 20)
    stress = base_stress + random.uniform(-5, 5)
    
    # Risk calculation
    temp_factor = (temp - 40) / 50 * 40
    stress_factor = (stress - 50) / 80 * 30
    random_factor = random.uniform(0, 15)
    risk = min(100, max(0, temp_factor + stress_factor + random_factor))
    
    # Energy consumption
    energy = random.uniform(150, 350)
    
    # Environment factors
    gas_level = random.uniform(0, 100)
    vibration = random.uniform(0, 15)
    humidity = random.uniform(30, 80)
    
    # Determine environment status
    if temp > 85 or gas_level > 80 or vibration > 12:
        env_status = "⚠️ DANGER"
        env_color = "#ff6b6b"
    elif temp > 75 or gas_level > 65 or vibration > 9:
        env_status = "⚠️ WARNING"
        env_color = "#ff9f43"
    else:
        env_status = "✅ GOOD"
        env_color = "#4ecdc4"
    
    # Machine data
    machine_data = []
    for i, machine in enumerate(MACHINES):
        machine_temp = random.uniform(45, 95)
        machine_vib = random.uniform(1, 15)
        machine_power = random.uniform(50, 150)
        
        if machine_temp > 90 or machine_vib > 13:
            status = "CRITICAL"
            status_color = "critical"
        elif machine_temp > 80 or machine_vib > 10:
            status = "WARNING"
            status_color = "warning"
        elif machine_temp > 70 or machine_vib > 7:
            status = "CAUTION"
            status_color = "caution"
        else:
            status = "NORMAL"
            status_color = "normal"
        
        machine_data.append({
            'Machine': f"{machine}-{i+1:02d}",
            'Temperature': f"{machine_temp:.1f}°C",
            'Vibration': f"{machine_vib:.2f}mm/s",
            'Power': f"{machine_power:.1f}kW",
            'Status': status,
            'Status_Color': status_color
        })
    
    # Employee data
    employee_data = []
    for emp in EMPLOYEES:
        fatigue = random.randint(20, 95)
        stress_level = random.randint(25, 90)
        heart_rate = random.randint(65, 110)
        shift_hours = random.randint(1, 8)
        
        risk_score = (fatigue * 0.4 + stress_level * 0.3 + (heart_rate - 65) * 0.3)
        
        if risk_score > 70:
            risk_level = "HIGH"
            risk_color = "critical"
        elif risk_score > 50:
            risk_level = "MEDIUM"
            risk_color = "warning"
        elif risk_score > 30:
            risk_level = "LOW-MED"
            risk_color = "caution"
        else:
            risk_level = "LOW"
            risk_color = "normal"
        
        employee_data.append({
            'Name': emp,
            'Fatigue': f"{fatigue}%",
            'Stress': f"{stress_level}%",
            'Heart Rate': f"{heart_rate} BPM",
            'Shift Hours': f"{shift_hours}h",
            'Risk Level': risk_level,
            'Risk_Color': risk_color
        })
    
    # Store data in session state
    st.session_state.temp_data.append(temp)
    st.session_state.stress_data.append(stress)
    st.session_state.risk_data.append(risk)
    st.session_state.energy_data.append(energy)
    st.session_state.timestamps.append(timestamp)
    
    # Keep only last 50 points
    if len(st.session_state.temp_data) > 50:
        st.session_state.temp_data = st.session_state.temp_data[-50:]
        st.session_state.stress_data = st.session_state.stress_data[-50:]
        st.session_state.risk_data = st.session_state.risk_data[-50:]
        st.session_state.energy_data = st.session_state.energy_data[-50:]
        st.session_state.timestamps = st.session_state.timestamps[-50:]
    
    return {
        'temp': temp,
        'stress': stress,
        'risk': risk,
        'energy': energy,
        'env_status': env_status,
        'env_color': env_color,
        'gas_level': gas_level,
        'vibration': vibration,
        'humidity': humidity,
        'machine_data': machine_data,
        'employee_data': employee_data
    }

def create_gauge_chart(value, title, color):
    """Create a gauge chart"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title, 'font': {'color': 'white'}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': 'white'},
            'bar': {'color': color},
            'bgcolor': '#1a1f2f',
            'borderwidth': 2,
            'bordercolor': '#2a2f3f',
            'steps': [
                {'range': [0, 33], 'color': '#4ecdc4'},
                {'range': [33, 66], 'color': '#ff9f43'},
                {'range': [66, 100], 'color': '#ff6b6b'}
            ],
        },
        number={'font': {'color': 'white', 'size': 24}}
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=250,
        margin=dict(l=20, r=20, t=50, b=20)
    )
    
    return fig

def create_time_series_plot(data, title, color):
    """Create a time series plot"""
    if len(st.session_state.timestamps) > 0 and len(data) > 0:
        fig = go.Figure()
        
        # Create rgba color for fill (convert hex to rgba)
        if color == "#ff6b6b":
            fill_color = "rgba(255, 107, 107, 0.2)"
        elif color == "#4ecdc4":
            fill_color = "rgba(78, 205, 196, 0.2)"
        elif color == "#ff9f43":
            fill_color = "rgba(255, 159, 67, 0.2)"
        else:
            fill_color = "rgba(255, 255, 255, 0.2)"
        
        fig.add_trace(go.Scatter(
            x=st.session_state.timestamps,
            y=data,
            mode='lines',
            name=title,
            line=dict(color=color, width=2),
            fill='tozeroy',
            fillcolor=fill_color
        ))
        
        # Add mean line
        mean_val = np.mean(data)
        fig.add_hline(y=mean_val, line_dash="dash", line_color="#666",
                     annotation_text=f"Mean: {mean_val:.1f}", 
                     annotation_position="bottom right",
                     annotation_font_color="white")
        
        fig.update_layout(
            title=title,
            title_font_color='white',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=300,
            margin=dict(l=40, r=40, t=40, b=40),
            xaxis=dict(
                showgrid=True,
                gridcolor='#2a2f3f',
                tickfont=dict(color='white'),
                title_font_color='white'
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='#2a2f3f',
                tickfont=dict(color='white'),
                title_font_color='white'
            ),
            legend=dict(font=dict(color='white'))
        )
        
        return fig
    return None

def main():
    # Header with datetime
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("<h1 style='color: #00d4ff; text-align: left;'>🏭 AI-POWERED INDUSTRY 4.0 CONTROL CENTER</h1>", 
                   unsafe_allow_html=True)
    with col2:
        current_time = datetime.now().strftime("%A, %B %d, %Y - %H:%M:%S")
        st.markdown(f"<div class='datetime'>{current_time}</div>", unsafe_allow_html=True)
    
    # Generate or update data
    data = generate_data()
    
    # Top Metrics Row
    st.markdown("<div class='section-header'>📊 REAL-TIME METRICS</div>", unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
            <div class='metric-card' style='border-left-color: #ff6b6b;'>
                <div class='metric-title'>🔥 MACHINE TEMP</div>
                <div class='metric-value' style='color: #ff6b6b;'>{data['temp']:.1f}°C</div>
                <div class='metric-trend'>▲ +2.5%</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class='metric-card' style='border-left-color: #4ecdc4;'>
                <div class='metric-title'>😓 WORKER STRESS</div>
                <div class='metric-value' style='color: #4ecdc4;'>{data['stress']:.0f} BPM</div>
                <div class='metric-trend'>▼ -1.2%</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
            <div class='metric-card' style='border-left-color: #ff9f43;'>
                <div class='metric-title'>⚠️ AI RISK</div>
                <div class='metric-value' style='color: #ff9f43;'>{data['risk']:.1f}%</div>
                <div class='metric-trend'>▲ +3.8%</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
            <div class='metric-card' style='border-left-color: {data['env_color']};'>
                <div class='metric-title'>🌍 ENVIRONMENT</div>
                <div class='metric-value' style='color: {data['env_color']};'>{data['env_status']}</div>
                <div class='metric-trend'>Humidity: {data['humidity']:.1f}%</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col5:
        st.markdown(f"""
            <div class='metric-card' style='border-left-color: #a55eea;'>
                <div class='metric-title'>⚡ ENERGY USE</div>
                <div class='metric-value' style='color: #a55eea;'>{data['energy']:.0f} kW</div>
                <div class='metric-trend'>▼ -0.8%</div>
            </div>
        """, unsafe_allow_html=True)
    
    # KPI Row
    st.markdown("<div class='section-header'>📈 KEY PERFORMANCE INDICATORS</div>", unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        machines_active = random.randint(58, 64)
        st.markdown(f"""
            <div class='kpi-card' style='border-color: #00d4ff;'>
                <div class='kpi-title'>🛠️ ACTIVE MACHINES</div>
                <div class='kpi-value' style='color: #00d4ff;'>{machines_active}/64</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        employees_present = random.randint(42, 50)
        st.markdown(f"""
            <div class='kpi-card' style='border-color: #4ecdc4;'>
                <div class='kpi-title'>👥 EMPLOYEES</div>
                <div class='kpi-value' style='color: #4ecdc4;'>{employees_present}/50</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        alerts = random.randint(0, 8)
        alert_color = "#ff6b6b" if alerts > 5 else "#ff9f43" if alerts > 2 else "#4ecdc4"
        st.markdown(f"""
            <div class='kpi-card' style='border-color: {alert_color};'>
                <div class='kpi-title'>🚨 ACTIVE ALERTS</div>
                <div class='kpi-value' style='color: {alert_color};'>{alerts}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        oee = random.uniform(72, 98)
        st.markdown(f"""
            <div class='kpi-card' style='border-color: #ff9f43;'>
                <div class='kpi-title'>📊 OEE SCORE</div>
                <div class='kpi-value' style='color: #ff9f43;'>{oee:.1f}%</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col5:
        uptime = random.uniform(98.5, 99.9)
        st.markdown(f"""
            <div class='kpi-card' style='border-color: #a55eea;'>
                <div class='kpi-title'>⏱️ UPTIME</div>
                <div class='kpi-value' style='color: #a55eea;'>{uptime:.1f}%</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col6:
        production = random.randint(420, 580)
        st.markdown(f"""
            <div class='kpi-card' style='border-color: #6c5ce7;'>
                <div class='kpi-title'>📦 PRODUCTION</div>
                <div class='kpi-value' style='color: #6c5ce7;'>{production}/hr</div>
            </div>
        """, unsafe_allow_html=True)
    
    # AI Prediction Panel
    st.markdown("<div class='section-header'>🤖 AI PREDICTIVE ANALYTICS</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        if data['risk'] > 80:
            prediction = "🔴 CRITICAL: Immediate action required! High probability of equipment failure in next 15 minutes."
            pred_color = "#ff6b6b"
        elif data['risk'] > 60:
            prediction = "🟡 WARNING: Elevated risk levels. Predictive maintenance recommended within 2 hours."
            pred_color = "#ff9f43"
        elif data['risk'] > 40:
            prediction = "🔵 CAUTION: Minor anomalies detected. Schedule inspection within 24 hours."
            pred_color = "#4ecdc4"
        else:
            prediction = "🟢 NORMAL: All systems operating optimally. No issues predicted."
            pred_color = "#00d4ff"
        
        st.markdown(f"""
            <div class='prediction-box' style='border-color: {pred_color};'>
                <div style='color: {pred_color}; font-size: 16px; font-weight: bold;'>{prediction}</div>
                <div style='color: #888; margin-top: 10px;'>Last analyzed: {datetime.now().strftime("%H:%M:%S")}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        # Gauge chart for confidence
        confidence = 95 if data['risk'] < 40 else 86 if data['risk'] < 60 else 79 if data['risk'] < 80 else 92
        fig = create_gauge_chart(confidence, "Confidence", pred_color)
        st.plotly_chart(fig, use_container_width=True)
    
    # Graphs Row
    st.markdown("<div class='section-header'>📈 TREND ANALYSIS</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.session_state.temp_data:
            fig = create_time_series_plot(st.session_state.temp_data, "🌡️ Machine Temperature Trend", "#ff6b6b")
            if fig:
                st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if st.session_state.stress_data:
            fig = create_time_series_plot(st.session_state.stress_data, "💓 Worker Stress Index", "#4ecdc4")
            if fig:
                st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        if st.session_state.risk_data:
            fig = create_time_series_plot(st.session_state.risk_data, "⚠️ AI Risk Prediction", "#ff9f43")
            if fig:
                st.plotly_chart(fig, use_container_width=True)
    
    # Machine Health Table
    st.markdown("<div class='section-header'>🏭 MACHINE HEALTH MONITORING</div>", unsafe_allow_html=True)
    
    # Convert machine data to DataFrame
    machine_df = pd.DataFrame(data['machine_data'])
    
    # Display machine table with custom styling using dataframe
    st.dataframe(
        machine_df.drop('Status_Color', axis=1),
        use_container_width=True,
        height=300,
        column_config={
            'Machine': 'Machine ID',
            'Temperature': 'Temperature',
            'Vibration': 'Vibration',
            'Power': 'Power',
            'Status': st.column_config.Column(
                'Status',
                help='Machine health status',
                width='medium'
            )
        }
    )
    
    # Employee Risk Table
    st.markdown("<div class='section-header'>👥 EMPLOYEE SAFETY MONITORING</div>", unsafe_allow_html=True)
    
    # Convert employee data to DataFrame
    employee_df = pd.DataFrame(data['employee_data'])
    
    # Display employee table
    st.dataframe(
        employee_df.drop('Risk_Color', axis=1),
        use_container_width=True,
        height=300,
        column_config={
            'Name': 'Employee Name',
            'Fatigue': 'Fatigue Level',
            'Stress': 'Stress Level',
            'Heart Rate': 'Heart Rate',
            'Shift Hours': 'Shift Hours',
            'Risk Level': st.column_config.Column(
                'Risk Level',
                help='Employee risk assessment',
                width='medium'
            )
        }
    )
    
    # Status Bar
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"✅ **System Status:** ONLINE | Last Update: {datetime.now().strftime('%H:%M:%S')}")
    
    with col2:
        latency = random.randint(8, 25)
        st.markdown(f"📶 **Network:** Stable | Latency: {latency}ms")
    
    with col3:
        data_points = len(st.session_state.temp_data)
        st.markdown(f"💾 **Data Points:** {data_points} | Buffer: 50")
    
    # Auto-refresh
    time.sleep(1.5)
    st.rerun()

if __name__ == "__main__":
    main()
