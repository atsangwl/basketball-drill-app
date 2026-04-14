import streamlit as st
import random
import os
import io
import base64
from gtts import gTTS

# --- 1. MOBILE-FIRST & SHOOTING STARS THEME ---
st.set_page_config(page_title="Shooting Stars Pro", page_icon="🏀")

st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    h1, h2, h3, p, span, div, label { color: #FFFFFF !important; }
    div.stButton > button:first-child {
        height: 4.5em; width: 100%; font-size: 22px !important;
        font-weight: bold; background-color: #FF0000;
        color: white !important; border-radius: 15px; border: 2px solid #CC0000;
    }
    .stAlert { background-color: #FF0000 !important; color: white !important; }
    hr { border-top: 1px solid #FF0000; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. THE SMART DATA DICTIONARY ---
checklist_data = {
    "Obstacles": {
        "Med Ball": "Off-hand stability.", "Rip Cone": "Low hip touch.", 
        "Tennis Ball": "Reaction catch.", "No Obstacle": "Pure mechanics."
    },
    "Footwork": {
        # Active moves (Can keep dribbling)
        "The Drop": {"p": "Feet wide, hips low.", "v": "the_drop.mp4", "is_gather": False},
        "Punch Step": {"p": "Violent lead plant.", "v": "punch_step.mp4", "is_gather": False},
        "Negative Step": {"p": "Spring forward.", "v": "neg_step.mp4", "is_gather": False},
        # Gather moves (Dribble ends HERE)
        "Step-Back": {"p": "Push off lead foot.", "v": "step_back.mp4", "is_gather": True},
        "High Pick Up": {"p": "Chin the ball.", "v": "high_pick.mp4", "is_gather": True},
        "Pivot Reverse": {"p": "Shield with back.", "v": "pivot_rev.mp4", "is_gather": True}
    },
    "Handle": {
        "Pocket": {"p": "Pull to hip.", "v": "pocket.mp4"},
        "Crossover": {"p": "Low and wide.", "v": "cross.mp4"},
        "In-and-Out": {"p": "Weight shift fake.", "v": "in_out.mp4"},
        "Behind Legs": {"p": "Leg as shield.", "v": "btwn_legs.mp4"}
    },
    "Finishing": {
        # These require a "Live Dribble" to start (The Euro/Veer IS the gather)
        "The Veer": {"v": "veer.mp4", "needs_live_dribble": True, "p": "Step into defender's path."},
        "Euro Step": {"v": "euro.mp4", "needs_live_dribble": True, "p": "Two lateral steps."},
        # These can happen AFTER a gather move (Terminal Finishes)
        "Power Width": {"v": "power.mp4", "needs_live_dribble": False, "p": "Two-foot explosive finish."},
        "Jump Shot": {"v": "jump_shot.mp4", "needs_live_dribble": False, "p": "Release at peak."},
        "Float Finish": {"v": "floater.mp4", "needs_live_dribble": False, "p": "High arc release."}
    }
}

# --- 3. THE SMART GENERATOR ---
if 'drill_deck' not in st.session_state:
    combos = []
    active_f = [k for k, v in checklist_data["Footwork"].items() if not v["is_gather"]]
    all_f = list(checklist_data["Footwork"].keys())
    all_h = list(checklist_data["Handle"].keys())
    
    for _ in range(1000):
        h1, h2 = random.sample(all_h, 2)
        f1 = random.choice(active_f) # Must be active to allow Move 2
        f2 = random.choice(all_f)
        
        # LOGIC CHECK: If f2 is a gather (Pivot/High Pick), 
        # the finish CANNOT need a live dribble (No Euro/Veer)
        if checklist_data["Footwork"][f2]["is_gather"]:
            valid_finishes = [k for k, v in checklist_data["Finishing"].items() if not v["needs_live_dribble"]]
        else:
            valid_finishes = list(checklist_data["Finishing"].keys())
            
        fin = random.choice(valid_finishes)
        obs = random.choice(list(checklist_data["Obstacles"].keys()))
        combos.append((h1, f1, h2, f2, fin, obs))
        
    st.session_state.drill_deck = combos
    st.session_state.history = []

def speak_text(text):
    try:
        b64 = base64.b64encode(io.BytesIO().tap(lambda f: gTTS(text, lang='en').write_to_fp(f)).getvalue()).decode()
        st.markdown(f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">', unsafe_allow_html=True)
    except: pass

# --- 4. UI ---
st.title("🏀 SHOOTING STARS")

if st.button('🔥 GENERATE PRO DRILL', key="main_gen"):
    if st.session_state.drill_deck:
        h1, f1, h2, f2, fin, obs = st.session_state.drill_deck.pop(0)
        vf = "videos"

        st.warning(f"🎯 **OBSTACLE:** {obs}\n\n{checklist_data['Obstacles'][obs]}")

        # --- SET 1 ---
        st.header("1️⃣ THE SHIFT")
        c1, c2 = st.columns(2)
        with c1:
            st.subheader(h1)
            v1 = os.path.join(vf, checklist_data["Handle"][h1]["v"])
            if os.path.exists(v1): st.video(v1)
        with c2:
            st.subheader(f1)
            v2 = os.path.join(vf, checklist_data["Footwork"][f1]["v"])
            if os.path.exists(v2): st.video(v2)

        # --- SET 2 ---
        st.header("2️⃣ THE ATTACK")
        c3, c4 = st.columns(2)
        with c3:
            st.subheader(h2)
            v3 = os.path.join(vf, checklist_data["Handle"][h2]["v"])
            if os.path.exists(v3): st.video(v3)
        with c4:
            st.subheader(f2)
            if checklist_data["Footwork"][f2]["is_gather"]: st.error("🛑 GATHER (BALL PICKUP)")
            v4 = os.path.join(vf, checklist_data["Footwork"][f2]["v"])
            if os.path.exists(v4): st.video(v4)

        # --- FINISH ---
        st.header("🏁 THE FINISH")
        st.subheader(fin)
        v5 = os.path.join(vf, checklist_data["Finishing"][fin]["v"])
        if os.path.exists(v5): st.video(v5)

        speak_text(f"Next drill. {h1} and {f1}. Then {h2} and {f2}. Finish with {fin}.")
    else:
        st.success("Session Complete! Reset the deck.")