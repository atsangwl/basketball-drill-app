import streamlit as st
import random
import os
import io
import base64
from gtts import gTTS
import itertools

# --- MOBILE OPTIMIZATION CSS ---
st.markdown("""
    <style>
    /* Make the Generate button huge and easy to tap with a thumb */
    div.stButton > button:first-child {
        height: 5em;
        font-size: 20px !important;
        font-weight: bold;
        border-radius: 15px;
        border: 2px solid #FF0000;
        background-color: #FF0000;
        color: white;
    }
    
    /* Center text for phone viewing */
    .stHeader, .stTitle {
        text-align: center;
    }

    /* Adjust video player to fit phone width perfectly */
    .stVideo {
        border-radius: 10px;
        border: 1px solid #333;
    }
    </style>
    """, unsafe_allow_html=True)
    

# --- 1. THE DATA DICTIONARY ---
checklist_data = {
    "Obstacles": {
        "Med Ball": "Hold med ball in off-hand; drop it during the second move.",
        "Rip Cone": "Touch the cone with your lead hand during the footwork phase.",
        "Tennis Ball Toss": "Coach tosses tennis ball; catch it while performing the handle.",
        "No Obstacle": "Pure focus on the mechanical execution."
    },
    "Footwork": {
        "The Drop": {"p": "Split feet wide, hips low.", "v": "the_drop.mp4", "detail": "Focus on width over depth."},
        "Punch Step": {"p": "Violent lead-foot plant.", "v": "punch_step.mp4", "detail": "Sells the drive to force a retreat."},
        "Negative Step": {"p": "Step back to spring forward.", "v": "neg_step.mp4", "detail": "Loads the glutes like a spring."},
        "Replacement": {"p": "Back foot replaces front spot.", "v": "replace.mp4", "detail": "Best for quick-release shots."},
        "Inverted Drag": {"p": "Back foot drags to stop.", "v": "inv_drag.mp4", "detail": "Decelerate instantly into a shot."},
        "Hip Swivel": {"p": "Rotate hips to the rim.", "v": "hip_swivel.mp4", "detail": "Change direction while ball hangs."},
        "Heel-to-Toe": {"p": "Roll weight to sell drive.", "v": "heel_toe.mp4", "detail": "Lure defender before a counter."},
        "Stutter Step": {"p": "High-frequency small steps.", "v": "stutter.mp4", "detail": "Disrupts defender's timing."},
        "Step-Back": {"p": "Push off lead foot.", "v": "step_back.mp4", "detail": "Creates 3+ feet of space."},
        "High Pick Up": {"v": "high_pick.mp4",  "p": "Chin the ball and keep it above your forehead through the jump.",  "detail": "Rip the ball from hip to above head to shield from defenders."},
        "Pivot Reverse": {"p": "Protect ball with back.", "v": "pivot_rev.mp4", "detail": "Use body to shield the drive."}
    },
    "Handle": {
        "Pocket": {"p": "Pull ball to back hip.", "v": "pocket.mp4", "detail": "Survey floor while ball hangs."},
        "Turn Pound": {"p": "Hand whips over top.", "v": "turn_pound.mp4", "detail": "High-velocity rhythmic dribble."},
        "Under-Dribble": {"p": "Ball below knee-height.", "v": "under.mp4", "detail": "Split pick and rolls effectively."},
        "Wrap Around": {"p": "Circular behind-back.", "v": "wrap.mp4", "detail": "Shield ball from reachers."},
        "In-and-Out": {"p": "Weight shift fake.", "v": "in_out.mp4", "detail": "Fake a cross, keep same hand."},
        "High Hang": {"p": "Float at waist height.", "v": "high_hang.mp4", "detail": "Time the defender's movements."},
        "Push Cross": {"p": "Aggressive long cross.", "v": "push_cross.mp4", "detail": "Cover ground on the break."},
        "Behind Legs": {"p": "Leg as a shield.", "v": "btwn_legs.mp4", "detail": "Safe change of direction."},
        "Crossover": {"p": "Low, wide shift.", "v": "cross.mp4", "detail": "Shift defender's center of gravity."}
    },
    "Finishing": {
        "The Veer": {"p": "Step into defender's path.", "v": "veer.mp4", "detail": "Kill verticality and force fouls."},
        "Extension": {"p": "Reach ball far from body.", "v": "extension.mp4", "detail": "Beat shot blockers' length."},
        "Inside Hand": {"p": "Far hand scoop.", "v": "inside_hand.mp4", "detail": "Use rim as a natural shield."},
        "Same Foot/Hand": {"p": "Unorthodox timing jump.", "v": "same_fh.mp4", "detail": "Mess up block timing."},
        "Bump Finish": {"p": "Initiate shoulder contact.", "v": "bump.mp4", "detail": "Create space before release."},
        "Euro Step": {"p": "Two-step lateral finish.", "v": "euro.mp4", "detail": "Navigate around paint help."},
        "Pro Hop": {"p": "Jump to two-foot land.", "v": "pro_hop.mp4", "detail": "Avoid charges in traffic."},
        "Rocker Step": {"p": "Fake layup to pull in.", "v": "rocker.mp4", "detail": "Lull defender into a freeze."},
        "Float Finish": {"p": "High-arc release.", "v": "floater.mp4", "detail": "Beat rotating centers' reach."},
        "Power Width": {"p": "Two-foot explosive finish.", "v": "power.mp4", "detail": "Maintain balance through contact."}
    }
}

# --- 2. GENERATE THE PRO STACK DECK ---
if 'drill_deck' not in st.session_state:
    combos = []
    # Creating a sample of 1,000 unique "Pro Stacks"
    for _ in range(1000):
        h1, h2 = random.sample(list(checklist_data["Handle"].keys()), 2)
        f1, f2 = random.sample(list(checklist_data["Footwork"].keys()), 2)
        fin = random.choice(list(checklist_data["Finishing"].keys()))
        obs = random.choice(list(checklist_data["Obstacles"].keys()))
        combos.append((h1, h2, f1, f2, fin, obs))
        
    random.shuffle(combos)
    st.session_state.drill_deck = combos
    st.session_state.history = []

# --- 3. HELPERS ---
def speak_text(text):
    try:
        tts = gTTS(text=text, lang='en')
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        b64 = base64.b64encode(fp.read()).decode()
        md = f'<audio autoplay="true" src="data:audio/mp3;base64,{b64}">'
        st.markdown(md, unsafe_allow_html=True)
    except: pass

# --- 4. APP UI ---
st.set_page_config(page_title="Shooting Stars Pro", page_icon="🏀")

# Sidebar: HISTORY
st.sidebar.header("📜 Session History")
if st.sidebar.button("🔄 Reset Deck"):
    del st.session_state.drill_deck
    st.rerun()

for item in reversed(st.session_state.history):
    st.sidebar.write(f"- {item}")

st.title("🏀 SHOOTING STARS Generator")

# --- 5. DRILL GENERATOR LOGIC ---
if st.button('🔥 GENERATE NEXT PRO STACK', use_container_width=True, key="main_drill_gen"):
    if st.session_state.drill_deck:
        # Unpack all 6 elements
        h1, h2, f1, f2, fin, obs = st.session_state.drill_deck.pop(0)
        
        # Get data for display
        h1_d, h2_d = checklist_data["Handle"][h1], checklist_data["Handle"][h2]
        f1_d, f2_d = checklist_data["Footwork"][f1], checklist_data["Footwork"][f2]
        fin_d = checklist_data["Finishing"][fin]
        obs_detail = checklist_data["Obstacles"][obs]

        # Save to history
        drill_str = f"{h1}+{h2} | {f1}+{f2} | {fin}"
        st.session_state.history.append(f"{drill_str} ({obs})")

        # Main Header Display
        st.header(f"Stack: {drill_str}")
        st.warning(f"🎯 **OBSTACLE:** {obs} — {obs_detail}")
        st.write(f"Remaining Drills: {len(st.session_state.drill_deck)}")
        
        # --- 6. DISPLAY VIDEOS ---
        video_folder = "videos"
        display_list = [
            ("Handle 1", h1, h1_d), ("Handle 2", h2, h2_d),
            ("Footwork 1", f1, f1_d), ("Footwork 2", f2, f2_d),
            ("Finishing", fin, fin_d)
        ]

        for label, name, data in display_list:
            st.subheader(f"🎥 {label}: {name}")
            video_path = os.path.join(video_folder, data['v'])
            
            if os.path.exists(video_path):
                st.video(video_path)
            else:
                st.error(f"❌ Video Missing: {data['v']}")
                
            with st.expander("Show Details"):
                st.write(data['detail'])
            st.info(f"**Key:** {data['p']}")
            st.divider()

        # Voice Trigger
        speak_text(f"Next drill. {h1}, {h2}. Footwork {f1}, {f2}. Finish with {fin}. Obstacle is {obs}.")
        
    else:
        st.success("🎉 Session Complete! Reset the deck to start a new practice.")