import streamlit as st
import random
import os
import io
import base64
from gtts import gTTS
import itertools

import streamlit as st
import random
import itertools
import os

# --- 1. THE EXPANDED 1,000 COMBO DICT ---
checklist_data = {
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
        "High Pick Up": {"v": "high_pick.mp4",  "p": "Chin the ball and keep it above your forehead through the jump.",  "detail": "As you take your two steps, rip the ball from your hip to above your head. This 'high-path' finish prevents defenders from stripping the ball low and allows you to use your body to shield the play."
},
        "Pivot Reverse": {"p": "Protect ball with back.", "v": "pivot_rev.mp4", "detail": "Use body to shield the drive."}
    },
    "Handle": {
        "Pocket": {"p": "Pull ball to back hip.", "v": "pocket.mp4", "detail": "Survey floor while ball hangs."},
        "Turn Pound": {"p": "Hand whips over top.", "v": "turn_pound.mp4", "detail": "High-velocity rhythmic dribble."},
        "Under-Dribble": {"p": "Ball below knee-height.", "v": "under.mp4", "detail": "Split pick and rolls effectively."},
        "Wrap Around": {"p": "Circular behind-back.", "v": "wrap.mp4", "detail": "Shield ball from reachers."},
        "In-and-Out": {"p": "Weight shift fake.", "v": "in_out.mp4", "detail": "Fake a cross, keep same hand."},
        "Exchange": {"p": "Rapid low transfer.", "v": "exchange.mp4", "detail": "Quick switch under the knees."},
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
# --- 2. GENERATE THE 1,000 COMBO DECK ---
if 'drill_deck' not in st.session_state:
    # This creates exactly 1,000 permutations
    combos = list(itertools.product(
        checklist_data["Footwork"].keys(), 
        checklist_data["Handle"].keys(), 
        checklist_data["Finishing"].keys()
    ))
    random.shuffle(combos)
    st.session_state.drill_deck = combos
    st.session_state.history = []

# (The rest of your UI/Video display code remains the same)
# --- 3. HELPERS ---
def fix_youtube_url(url):
    return url.replace("shorts/", "watch?v=") if "shorts" in url else url

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
st.set_page_config(page_title="Coach Pro", page_icon="🏀")

# Sidebar: HISTORY
st.sidebar.header("📜 Session History")
if st.sidebar.button("🔄 Reset Deck"):
    del st.session_state.drill_deck
    st.rerun()

for item in reversed(st.session_state.history):
    st.sidebar.write(f"- {item}")

st.title("🏀 Pro Skill Generator")

# --- 5. THE DRILL GENERATOR ---
# We use a unique key here to prevent any "Duplicate Element" errors
if st.button('🔥 GENERATE NEXT UNIQUE DRILL', use_container_width=True, key="main_drill_gen"):
    if st.session_state.drill_deck:
        # 1. Pick the drill from our shuffled 1,000+ combo deck
        f_key, h_key, fin_key = st.session_state.drill_deck.pop(0)
        
        # 2. Extract the data for these moves
        f_data = checklist_data["Footwork"][f_key]
        h_data = checklist_data["Handle"][h_key]
        fin_data = checklist_data["Finishing"][fin_key]
        
        # 3. Save to history
        drill_str = f"{h_key} + {f_key} + {fin_key}"
        st.session_state.history.append(drill_str)

        st.header(f"Stack: {drill_str}")
        st.write(f"Remaining combinations in deck: {len(st.session_state.drill_deck)}")
        
        # --- 6. DISPLAY THE VIDEOS ---
        video_folder = "videos"
        
        display_list = [
            ("Footwork", f_key, f_data), 
            ("Handle", h_key, h_data), 
            ("Finishing", fin_key, fin_data)
        ]

        for label, name, data in display_list:
            st.subheader(f"🎥 {label}: {name}")
            
            video_path = os.path.join(video_folder, data['v'])
            
            if os.path.exists(video_path):
                st.video(video_path)
                st.caption(f"📁 Playing: {data['v']}")
            else:
                # This helps you identify which of the 30 videos you still need to download
                st.error(f"❌ Video not found: Add '{data['v']}' to your videos folder.")
                
            with st.expander("Technical Breakdown"):
                st.write(data['detail'])
            st.info(f"**Coaching Key:** {data['p']}")
            st.divider()

        # Voice Trigger for the court
        speak_text(f"Next drill. {h_key}, {f_key}, and {fin_key}.")
        
    else:
        st.success("🎉 All unique combinations completed! Reset the deck in the sidebar to start over.")