# app.py
import streamlit as st
import pandas as pd
from rules import RULES
from ai_engine import analyze_ticket

st.set_page_config(layout="wide")
st.title("✈️ Airline Ticket Audit System")

# -----------------------------
# 20 Hardcoded tickets
# -----------------------------
tickets = pd.DataFrame([
    {"TicketNo":"1761000000001","Our_Fare":500,"Agent_Fare":480,"Our_Tax_ZK":25,"Agent_Tax_ZK":0,"Our_Tax_YQ":40,"Agent_Tax_YQ":40,"Our_Tax_WO":15,"Agent_Tax_WO":15,"Our_Comm":50,"Agent_Comm":80,"Penalty":0,"Tourcode":"TC0","Waiver":"W23","NoShow":True},
    {"TicketNo":"1761000000002","Our_Fare":620,"Agent_Fare":620,"Our_Tax_ZK":0,"Agent_Tax_ZK":0,"Our_Tax_YQ":45,"Agent_Tax_YQ":45,"Our_Tax_WO":18,"Agent_Tax_WO":18,"Our_Comm":62,"Agent_Comm":62,"Penalty":0,"Tourcode":"NONE","Waiver":"","NoShow":False},
    {"TicketNo":"1761000000003","Our_Fare":780,"Agent_Fare":780,"Our_Tax_ZK":30,"Agent_Tax_ZK":15,"Our_Tax_YQ":55,"Agent_Tax_YQ":55,"Our_Tax_WO":20,"Agent_Tax_WO":20,"Our_Comm":78,"Agent_Comm":78,"Penalty":150,"Tourcode":"CORP2025","Waiver":"","NoShow":True},
    {"TicketNo":"1761000000004","Our_Fare":1050,"Agent_Fare":950,"Our_Tax_ZK":40,"Agent_Tax_ZK":40,"Our_Tax_YQ":60,"Agent_Tax_YQ":40,"Our_Tax_WO":25,"Agent_Tax_WO":25,"Our_Comm":105,"Agent_Comm":105,"Penalty":300,"Tourcode":"EXCH2025","Waiver":"","NoShow":False},
    {"TicketNo":"1761000000005","Our_Fare":890,"Agent_Fare":890,"Our_Tax_ZK":22,"Agent_Tax_ZK":22,"Our_Tax_YQ":45,"Agent_Tax_YQ":45,"Our_Tax_WO":16,"Agent_Tax_WO":16,"Our_Comm":89,"Agent_Comm":120,"Penalty":0,"Tourcode":"PROMO2025","Waiver":"WAIVE-COMM","NoShow":False},
    {"TicketNo":"1761000000006","Our_Fare":450,"Agent_Fare":450,"Our_Tax_ZK":20,"Agent_Tax_ZK":0,"Our_Tax_YQ":35,"Agent_Tax_YQ":35,"Our_Tax_WO":10,"Agent_Tax_WO":10,"Our_Comm":45,"Agent_Comm":45,"Penalty":0,"Tourcode":"NONE","Waiver":"","NoShow":True},
    {"TicketNo":"1761000000007","Our_Fare":700,"Agent_Fare":680,"Our_Tax_ZK":28,"Agent_Tax_ZK":28,"Our_Tax_YQ":50,"Agent_Tax_YQ":50,"Our_Tax_WO":18,"Agent_Tax_WO":18,"Our_Comm":70,"Agent_Comm":70,"Penalty":100,"Tourcode":"TC5","Waiver":"","NoShow":False},
    {"TicketNo":"1761000000008","Our_Fare":300,"Agent_Fare":300,"Our_Tax_ZK":15,"Agent_Tax_ZK":15,"Our_Tax_YQ":25,"Agent_Tax_YQ":25,"Our_Tax_WO":8,"Agent_Tax_WO":8,"Our_Comm":30,"Agent_Comm":30,"Penalty":0,"Tourcode":"NONE","Waiver":"","NoShow":False},
    {"TicketNo":"1761000000009","Our_Fare":1200,"Agent_Fare":1150,"Our_Tax_ZK":50,"Agent_Tax_ZK":50,"Our_Tax_YQ":70,"Agent_Tax_YQ":70,"Our_Tax_WO":30,"Agent_Tax_WO":30,"Our_Comm":120,"Agent_Comm":150,"Penalty":400,"Tourcode":"CORP","Waiver":"","NoShow":False},
    {"TicketNo":"1761000000010","Our_Fare":650,"Agent_Fare":650,"Our_Tax_ZK":0,"Agent_Tax_ZK":0,"Our_Tax_YQ":48,"Agent_Tax_YQ":48,"Our_Tax_WO":17,"Agent_Tax_WO":17,"Our_Comm":65,"Agent_Comm":65,"Penalty":0,"Tourcode":"NONE","Waiver":"","NoShow":False},
    {"TicketNo":"1761000000011","Our_Fare":520,"Agent_Fare":500,"Our_Tax_ZK":25,"Agent_Tax_ZK":25,"Our_Tax_YQ":40,"Agent_Tax_YQ":40,"Our_Tax_WO":15,"Agent_Tax_WO":15,"Our_Comm":52,"Agent_Comm":52,"Penalty":50,"Tourcode":"TC5","Waiver":"","NoShow":False},
    {"TicketNo":"1761000000012","Our_Fare":480,"Agent_Fare":480,"Our_Tax_ZK":20,"Agent_Tax_ZK":20,"Our_Tax_YQ":35,"Agent_Tax_YQ":35,"Our_Tax_WO":12,"Agent_Tax_WO":12,"Our_Comm":48,"Agent_Comm":48,"Penalty":0,"Tourcode":"NONE","Waiver":"","NoShow":False},
    {"TicketNo":"1761000000013","Our_Fare":900,"Agent_Fare":850,"Our_Tax_ZK":35,"Agent_Tax_ZK":35,"Our_Tax_YQ":55,"Agent_Tax_YQ":55,"Our_Tax_WO":22,"Agent_Tax_WO":22,"Our_Comm":90,"Agent_Comm":90,"Penalty":200,"Tourcode":"CORP","Waiver":"","NoShow":False},
    {"TicketNo":"1761000000014","Our_Fare":400,"Agent_Fare":400,"Our_Tax_ZK":18,"Agent_Tax_ZK":0,"Our_Tax_YQ":30,"Agent_Tax_YQ":30,"Our_Tax_WO":10,"Agent_Tax_WO":10,"Our_Comm":40,"Agent_Comm":40,"Penalty":0,"Tourcode":"NONE","Waiver":"","NoShow":True},
    {"TicketNo":"1761000000015","Our_Fare":1100,"Agent_Fare":1100,"Our_Tax_ZK":45,"Agent_Tax_ZK":45,"Our_Tax_YQ":65,"Agent_Tax_YQ":65,"Our_Tax_WO":28,"Agent_Tax_WO":28,"Our_Comm":110,"Agent_Comm":110,"Penalty":0,"Tourcode":"NONE","Waiver":"","NoShow":False},
    {"TicketNo":"1761000000016","Our_Fare":750,"Agent_Fare":700,"Our_Tax_ZK":30,"Agent_Tax_ZK":30,"Our_Tax_YQ":50,"Agent_Tax_YQ":50,"Our_Tax_WO":20,"Agent_Tax_WO":20,"Our_Comm":75,"Agent_Comm":75,"Penalty":150,"Tourcode":"TC5","Waiver":"","NoShow":False},
    {"TicketNo":"1761000000017","Our_Fare":560,"Agent_Fare":560,"Our_Tax_ZK":22,"Agent_Tax_ZK":22,"Our_Tax_YQ":38,"Agent_Tax_YQ":38,"Our_Tax_WO":14,"Agent_Tax_WO":14,"Our_Comm":56,"Agent_Comm":56,"Penalty":0,"Tourcode":"NONE","Waiver":"","NoShow":False},
    {"TicketNo":"1761000000018","Our_Fare":980,"Agent_Fare":950,"Our_Tax_ZK":40,"Agent_Tax_ZK":40,"Our_Tax_YQ":60,"Agent_Tax_YQ":60,"Our_Tax_WO":25,"Agent_Tax_WO":25,"Our_Comm":98,"Agent_Comm":98,"Penalty":250,"Tourcode":"CORP","Waiver":"","NoShow":False},
    {"TicketNo":"1761000000019","Our_Fare":430,"Agent_Fare":430,"Our_Tax_ZK":18,"Agent_Tax_ZK":18,"Our_Tax_YQ":32,"Agent_Tax_YQ":32,"Our_Tax_WO":10,"Agent_Tax_WO":10,"Our_Comm":43,"Agent_Comm":43,"Penalty":0,"Tourcode":"NONE","Waiver":"","NoShow":False},
    {"TicketNo":"1761000000020","Our_Fare":670,"Agent_Fare":640,"Our_Tax_ZK":28,"Agent_Tax_ZK":28,"Our_Tax_YQ":48,"Agent_Tax_YQ":48,"Our_Tax_WO":18,"Agent_Tax_WO":18,"Our_Comm":67,"Agent_Comm":67,"Penalty":120,"Tourcode":"TC5","Waiver":"","NoShow":False}
])

# -----------------------------
# Session state
# -----------------------------
if "selected_ticket" not in st.session_state:
    st.session_state.selected_ticket = None
if "ai_result" not in st.session_state:
    st.session_state.ai_result = None

# -----------------------------
# Outer screen: Ticket list
# -----------------------------
if st.session_state.selected_ticket is None:

    selected = st.selectbox(
        "Select Ticket Number",
        tickets["TicketNo"].tolist()
    )
    if st.button("Open Ticket"):
        st.session_state.selected_ticket = selected
        st.rerun()

    display_cols = [
        "TicketNo", "Our_Fare", "Agent_Fare",
        "Our_Tax_ZK", "Agent_Tax_ZK",
        "Our_Tax_YQ", "Agent_Tax_YQ",
        "Our_Tax_WO", "Agent_Tax_WO",
        "Our_Comm", "Agent_Comm",
        "Penalty", "Tourcode", "Waiver", "NoShow"
    ]

    st.dataframe(
        tickets[display_cols],
        use_container_width=True,
        hide_index=True
    )

# -----------------------------
# Inner screen: Ticket detail
# -----------------------------
else:
    ticket = tickets[tickets["TicketNo"] == st.session_state.selected_ticket].iloc[0]

    if st.button("⬅ Back"):
        st.session_state.selected_ticket = None
        st.session_state.ai_result = None
        st.rerun()

    st.subheader(f"🎫 Ticket Details: {ticket['TicketNo']}")

    def render_input(label, value, field_name):
        highlighted = st.session_state.ai_result.get("highlight_fields", []) if st.session_state.ai_result else []
        bg = "#ffcccc" if field_name in highlighted else "#ffffff"
        st.markdown(f"""
            <style>
            input[aria-label="{label}"] {{
                background-color: {bg};
            }}
            </style>
        """, unsafe_allow_html=True)
        return st.text_input(label, value, disabled=True, key=field_name)

    col1, col2, col3 = st.columns(3)
    with col1:
        render_input("Our Fare", ticket["Our_Fare"], "Our_Fare")
        render_input("Our ZK Tax", ticket["Our_Tax_ZK"], "Our_Tax_ZK")
        render_input("Our YQ Tax", ticket["Our_Tax_YQ"], "Our_Tax_YQ")
        render_input("Our WO Tax", ticket["Our_Tax_WO"], "Our_Tax_WO")
        render_input("Our Commission", ticket["Our_Comm"], "Our_Comm")

    with col2:
        render_input("Agent Fare", ticket["Agent_Fare"], "Agent_Fare")
        render_input("Agent ZK Tax", ticket["Agent_Tax_ZK"], "Agent_Tax_ZK")
        render_input("Agent YQ Tax", ticket["Agent_Tax_YQ"], "Agent_Tax_YQ")
        render_input("Agent WO Tax", ticket["Agent_Tax_WO"], "Agent_Tax_WO")
        render_input("Agent Commission", ticket["Agent_Comm"], "Agent_Comm")

    with col3:
        render_input("Penalty", ticket["Penalty"], "Penalty")
        render_input("Tour Code", ticket["Tourcode"], "Tourcode")
        render_input("Waiver", ticket["Waiver"], "Waiver")
        render_input("No Show", str(ticket["NoShow"]), "NoShow")

    st.divider()
    st.text_area("Auditor Comment", height=120)

    col1, col2 = st.columns([8, 2])
    with col2:
        if st.button("🤖 Analyze with AI"):
            st.session_state.ai_result = analyze_ticket(ticket.to_dict(), RULES)
            st.rerun()


    if st.session_state.ai_result:
        st.markdown("### 🔴 AI Analysis")
        st.markdown(
            f"""
            <div style="color:red">
            <b>Status:</b> {st.session_state.ai_result['status']}<br>
            <b>Comment:</b> {st.session_state.ai_result['comment']}<br>
            <b>Leak Type:</b> {st.session_state.ai_result['leak_type']}<br>
            <b>Suggested Fix:</b> {st.session_state.ai_result['suggested_fix']}<br>
            <b>Amount Impact:</b> {st.session_state.ai_result['amount_impact']}
            </div>
            """,
            unsafe_allow_html=True
        )