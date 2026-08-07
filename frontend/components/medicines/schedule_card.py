import streamlit as st


def render_schedule(schedule):

    st.markdown("## ⏰ Today's Medicine Schedule")

    if not schedule:
        st.info("No medicines scheduled for today.")
        return

    icons = {
        "Morning": "🌅",
        "After Breakfast": "🍳",
        "After Lunch": "🍽️",
        "After Dinner": "🌙",
        "Night": "🌙"
    }

    with st.container(border=True):

        for i, slot in enumerate(schedule):

            time = slot.get("time", "")
            medicines = slot.get("medicines", [])

            # Compact time header
            medicine_count = len(medicines)

            label = "Medicine" if medicine_count == 1 else "Medicines"

            st.markdown(
                f"### {icons.get(time, '🕒')} {time} ({medicine_count} {label})"
            )

            for med in medicines:

                freq = med.get("frequency", "Scheduled")
                dosage = med.get("dosage", "-")

                if "SOS" in freq or "Required" in freq:
                    badge = "🟡 SOS"
                elif "Once" in freq:
                    badge = "🟢 Once Daily"
                elif "Twice" in freq:
                    badge = "🔵 Twice Daily"
                elif "Three" in freq:
                    badge = "🟣 Three Times"
                else:
                    badge = "⚪ Scheduled"

                with st.container(border=True):

                    c1, c2, c3 = st.columns([5, 2, 2])

                    with c1:
                        st.markdown(f"**💊 {med.get('name','')}**")
                        
                    with c2:
                        st.markdown("**Dose**")
                        st.markdown(f"<span style='font-size:16px'>{dosage}</span>", unsafe_allow_html=True)

                    with c3:
                        st.info(badge)
            
            if i < len(schedule) - 1:
                st.markdown("---")

        st.caption("Medication schedule generated from the uploaded prescription.")