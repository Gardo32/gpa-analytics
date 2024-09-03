import colorsys
import streamlit as st

preset_colors = [
    ("Default dark", {
        "primaryColor": "#ff4b4b",
        "backgroundColor": "#0e1117",
        "secondaryBackgroundColor": "#262730",
        "textColor": "#fafafa",
    }),
    ("Default light", {
        "primaryColor": "#ff4b4b",
        "backgroundColor": "#ffffff",
        "secondaryBackgroundColor": "#f0f2f6",
        "textColor": "#31333F",
    })
]

default_color = preset_colors[0][1]

def sync_rgb_to_hls(key):
    rgb = st.session_state[key][1:]
    rgb = tuple(int(rgb[i:i+2], 16) / 255 for i in (0, 2, 4))
    hls = colorsys.rgb_to_hls(*rgb)
    st.session_state[f"{key}H"] = round(hls[0] * 360)
    st.session_state[f"{key}L"] = round(hls[1] * 100)
    st.session_state[f"{key}S"] = round(hls[2] * 100)

def sync_hls_to_rgb(key):
    h = st.session_state[f"{key}H"] / 360
    l = st.session_state[f"{key}L"] / 100
    s = st.session_state[f"{key}S"] / 100
    rgb = colorsys.hls_to_rgb(h, l, s)
    st.session_state[key] = f"#{round(rgb[0] * 255):02x}{round(rgb[1] * 255):02x}{round(rgb[2] * 255):02x}"

def set_color(key, color):
    st.session_state[key] = color
    sync_rgb_to_hls(key)

if 'primaryColor' not in st.session_state:
    for key, color in default_color.items():
        set_color(key, color)

st.title("Streamlit color theme editor")

def on_preset_color_selected():
    color = preset_colors[st.session_state.preset_color][1]
    for key, value in color.items():
        set_color(key, value)

st.selectbox("Preset colors", key="preset_color", options=range(len(preset_colors)), format_func=lambda idx: preset_colors[idx][0], on_change=on_preset_color_selected)


def color_picker(label, key, l_only=True):
    col1, col2 = st.columns([1, 3])
    with col1:
        st.color_picker(label, key=key, on_change=sync_rgb_to_hls, args=(key,))
    with col2:
        st.slider(f"H for {label}", key=f"{key}H", min_value=0, max_value=360, on_change=sync_hls_to_rgb, args=(key,), format="%d°", label_visibility="collapsed")
        st.slider(f"L for {label}", key=f"{key}L", min_value=0, max_value=100, on_change=sync_hls_to_rgb, args=(key,), format="%d%%", label_visibility="collapsed")
        if not l_only:
            st.slider(f"S for {label}", key=f"{key}S", min_value=0, max_value=100, on_change=sync_hls_to_rgb, args=(key,), format="%d%%", label_visibility="collapsed")

color_picker('Primary color', key="primaryColor")
color_picker('Text color', key="textColor")
color_picker('Background color', key="backgroundColor")
color_picker('Secondary background color', key="secondaryBackgroundColor")

# Apply theme to the page
st.checkbox("Apply theme to this page", value=True, disabled=True)

def reconcile_theme_config():
    keys = ['primaryColor', 'backgroundColor', 'secondaryBackgroundColor', 'textColor']
    has_changed = False
    for key in keys:
        if st._config.get_option(f'theme.{key}') != st.session_state[key]:
            st._config.set_option(f'theme.{key}', st.session_state[key])
            has_changed = True
    if has_changed:
        st.rerun()

reconcile_theme_config()

# Sidebar sample components (Input widgets)
with st.sidebar:
    st.header("Sample Input Widgets")
    st.text_input("Text Input")
    st.number_input("Number Input", min_value=0, max_value=100, value=50)
    st.selectbox("Selectbox", options=["Option 1", "Option 2", "Option 3"])
    st.slider("Slider", min_value=0, max_value=100, value=50)
    st.checkbox("Checkbox")
    st.radio("Radio Buttons", options=["Option 1", "Option 2", "Option 3"])
    st.button("Button")
