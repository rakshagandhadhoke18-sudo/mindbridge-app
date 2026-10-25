import streamlit as st
import re
import time

# ==========================================
# 1. PAGE CONFIGURATION & STYLING
# ==========================================
st.set_page_config(
    page_title="MindBridge - Student Wellbeing Companion",
    page_icon="🌱",
    layout="wide"
)

# Custom Styling for Warmth & Accessibility
st.markdown("""
    <style>
    .stApp {
        background-color: #F8F9FA;
    }
    .main-title {
        color: #2C3E50;
        font-family: 'Helvetica Neue', sans-serif;
        font-weight: 700;
    }
    .crisis-card {
        background-color: #FFF3CD;
        border-left: 6px solid #FFC107;
        padding: 20px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. ETHICAL SAFETY & CRISIS GUARDRAILS
# ==========================================
CRISIS_TRIGGERS = [
    r"\b(suicide|suicidal)\b",
    r"\b(kill|ending)\s+(myself|my life)\b",
    r"\b(want to|going to)\s+die\b",
    r"\bself[\s-]harm\b",
    r"\bcut(ting)?\s+myself\b",
    r"\bhurt\s+myself\b",
    r"\bno\s+reason\s+to\s+live\b",
    r"\bcannot\s+go\s+on\b",
    r"\bhopeless\b",
    r"\bworthless\b"
]

HELPLINES = {
    "United States": "988 (Suicide & Crisis Lifeline) | Text HOME to 741741",
    "India": "Tele-MANAS: 14416 or 1800-891-4416 | KIRAN: 1800-599-0019",
    "United Kingdom": "111 (NHS Mental Health Services) | Samaritans: 116 123",
    "Canada": "988 (Suicide Crisis Helpline)",
    "International": "Find your local helpline: https://findahelpline.com/"
}

def detect_crisis(text: str) -> bool:
    """Scans input text for severe depression or self-harm triggers."""
    lowered_text = text.lower()
    for pattern in CRISIS_TRIGGERS:
        if re.search(pattern, lowered_text):
            return True
    return False

def render_crisis_alert():
    """Immediately displays emergency support contact details."""
    st.error("⚠️ EMERGENCY SUPPORT NOTICE")
    st.markdown("""
    <div class="crisis-card">
        <h3>We care about your safety and well-being.</h3>
        <p>It sounds like you are going through an extremely difficult time. You do not have to carry this alone. Please reach out to professional support immediately.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.subheader("📞 Official Student & Crisis Helplines")
    for region, number in HELPLINES.items():
        st.markdown(f"**{region}:** {number}")
    
    st.warning("If you are in immediate physical danger, please call your local emergency services (e.g., 911, 112, 100) or go to the nearest hospital emergency room.")

# ==========================================
# 3. EMPATHETIC CHAT BOT ENGINE
# ==========================================
def generate_empathetic_response(user_input: str) -> str:
    text = user_input.lower()
    
    if "exam" in text or "test" in text or "grade" in text:
        return ("Exams and grading pressures can feel overwhelming, especially in engineering where expectations run high. "
                "Remember that your worth as a person is not defined by a test score. "
                "Let's break your study material into manageable 25-minute focus blocks. What subject feels heaviest right now?")
    
    elif "code" in text or "bug" in text or "project" in text or "assignment" in text:
        return ("Debugging or tackling a massive project can be mentally exhausting. It's completely normal to feel stuck. "
                "Sometimes stepping away for a 5-minute breathing break gives your brain the space to find the solution. "
                "Would you like to try a short breathing exercise or organize a quick task list?")
    
    elif "fail" in text or "behind" in text or "imposter" in text:
        return ("Feeling behind or questioning whether you belong in engineering is something almost every student experiences at some point. "
                "You belong here, and taking small, realistic steps is enough for today. "
                "Try using the 'Thought Reframer' tab to re-examine these thoughts, or let's plan just one small task together.")
    
    else:
        return ("I hear you, and it is completely valid to feel stressed given everything on your plate. "
                "Taking a moment to pause is a strong first step. "
                "How can I best support you right now? We can plan a study session, reframe a negative thought, or do a quick calming exercise.")

# ==========================================
# 4. INITIALIZE SESSION STATE
# ==========================================
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm your Wellbeing Companion. Engineering school is tough, but you don't have to navigate it alone. How are you feeling today?"}
    ]

# ==========================================
# 5. USER INTERFACE
# ==========================================
st.markdown("<h1 class='main-title'>🌱 MindBridge: Student Wellbeing Companion</h1>", unsafe_allow_html=True)
st.caption("A supportive space for engineering students to manage stress, plan focus time, and build resilience.")

# Navigation Tabs
tab_chat, tab_pomodoro, tab_reframe, tab_breathing = st.tabs([
    "💬 Empathetic Chat", 
    "⏱️ Pomodoro Planner", 
    "🧠 Thought Reframer", 
    "🫁 Breathing Exercise"
])

# ------------------------------------------
# TAB 1: EMPATHETIC CHAT & SAFETY GUARDRAILS
# ------------------------------------------
with tab_chat:
    st.subheader("Supportive Chat")
    
    # Display message history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat Input Box
    if user_prompt := st.chat_input("Share what's on your mind..."):
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        with st.chat_message("user"):
            st.write(user_prompt)

        # ETHICAL SAFETY GUARDRAIL CHECK
        if detect_crisis(user_prompt):
            with st.chat_message("assistant"):
                render_crisis_alert()
            st.session_state.messages.append({
                "role": "assistant", 
                "content": "[CRISIS TRIGGERED: Emergency helpline resources rendered]"
            })
        else:
            response = generate_empathetic_response(user_prompt)
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.write(response)

# ------------------------------------------
# TAB 2: POMODORO PLANNER
# ------------------------------------------
with tab_pomodoro:
    st.subheader("⏱️ Low-Stress Pomodoro Planner")
    st.write("Break daunting engineering projects into small, digestible focus sessions.")

    col1, col2 = st.columns([2, 1])
    
    with col1:
        task_name = st.text_input("What single task are we focusing on?", placeholder="e.g., Read section 3.2 of Signals & Systems")
        work_duration = st.slider("Focus Duration (minutes)", min_value=1, max_value=60, value=25, step=1)
        
        if st.button("▶️ Start Focus Timer", use_container_width=True):
            if task_name:
                progress_bar = st.progress(0.0)
                status_text = st.empty()
                total_seconds = work_duration * 60
                
                for elapsed in range(total_seconds):
                    time.sleep(1)
                    remaining = total_seconds - (elapsed + 1)
                    mins, secs = divmod(remaining, 60)
                    progress_bar.progress((elapsed + 1) / total_seconds)
                    status_text.metric(label=f"Focusing on: {task_name}", value=f"{mins:02d}:{secs:02d}")
                
                st.success("🎉 Focus session complete! Take a well-deserved break.")
                st.balloons()
            else:
                st.warning("Please enter a task name first.")

    with col2:
        st.info("""
        **Tips for Engineering Students:**
        - Hide your phone in another room.
        - Close unnecessary browser tabs.
        - Focus on *progress*, not perfection.
        """)

# ------------------------------------------
# TAB 3: THOUGHT REFRAMER (CBT TOOL)
# ------------------------------------------
with tab_reframe:
    st.subheader("🧠 Negative Thought Reframer")
    st.write("Cognitive reframing helps identify unhelpful thinking patterns and reframe them into realistic, balanced perspectives.")

    negative_thought = st.text_area(
        "What negative or distressing thought are you experiencing?",
        placeholder="e.g., 'If I fail this algorithms exam, my engineering career is over.'"
    )

    if st.button("Reframe Thought"):
        if detect_crisis(negative_thought):
            render_crisis_alert()
        elif negative_thought.strip():
            st.markdown("### Balanced Perspective Breakdown")
            
            col_a, col_b = st.columns(2)
            with col_a:
                st.error("**Original Thought**")
                st.write(f'"{negative_thought}"')
                st.caption("Distortion: Catastrophizing / All-or-Nothing Thinking")

            with col_b:
                st.success("**Empathetic Reframe**")
                st.write("""
                "This exam is important, but a single test score does not dictate my entire future or career. 
                I have overcome challenging topics before, and I can take actionable steps today to prepare as best as I can."
                """)
                st.caption("Balanced & Compassionate Realism")
        else:
            st.warning("Please enter a thought to reframe.")

# ------------------------------------------
# TAB 4: BREATHING EXERCISE WIDGET
# ------------------------------------------
with tab_breathing:
    st.subheader("🫁 Box Breathing for Stress Reduction")
    st.write("Box breathing (4-4-4-4) is a proven technique to calm the nervous system when feeling overwhelmed.")

    if st.button("🫁 Start Guided Breathing"):
        guide_box = st.empty()
        
        cycles = 2
        for cycle in range(cycles):
            for i in range(1, 5):
                guide_box.info(f"🌬️ **Inhale slowly... ({i}/4)**")
                time.sleep(1)
            for i in range(1, 5):
                guide_box.warning(f"⏸️ **Hold breath... ({i}/4)**")
                time.sleep(1)
            for i in range(1, 5):
                guide_box.success(f"💨 **Exhale completely... ({i}/4)**")
                time.sleep(1)
            for i in range(1, 5):
                guide_box.warning(f"⏸️ **Hold breath... ({i}/4)**")
                time.sleep(1)
        
        guide_box.success("✨ Great job! Take a deep breath and carry this calmness into your next task.")

# Footer Safety Reminder
st.divider()
st.caption("🛡️ **Disclaimer & Safety Notice:** MindBridge is an informational and wellness support tool. It is not a substitute for professional mental health care, diagnosis, or treatment.")