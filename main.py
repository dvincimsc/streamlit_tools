import streamlit as st
import re

st.set_page_config(layout="wide")

# Extract file ID from Google Drive link
def extract_file_id(link):
    match = re.search(r"(?:id=|/d/)([\w-]{25,})", link)
    return match.group(1) if match else None

# Convert to embed iframe link
def to_embed_iframe(file_id):
    return f"https://drive.google.com/file/d/{file_id}/preview"

# Proper case conversion
def to_proper_case(s):
    return " ".join([word.capitalize() for word in s.split()])

st.title("Google Drive Viewer with Metadata Display & Rotation")

# Input box
input_data = st.text_area("Paste your tab-, comma-, or newline-separated data below:")

if input_data:
    # Split input into lines and group them into blocks separated by empty lines
    records = []
    current_record = []

    for line in input_data.strip().splitlines():
        if line.strip() == "":
            if current_record:
                records.append(current_record)
                current_record = []
        else:
            current_record.append(line.strip())

    if current_record:
        records.append(current_record)

    # Process each record
    for idx, record in enumerate(records):
        st.markdown(f"### Record {idx + 1}")

        drive_links = []
        other_data = []
        name_fields = {"first name": "", "middle name": "", "last name": ""}

        # Separate drive links and other info, also collect names
        for item in record:
            if "drive.google.com" in item:
                drive_links.append(item)
            else:
                other_data.append(item)
                if ":" in item:
                    key, value = item.split(":", 1)
                    k_lower = key.strip().lower()
                    if k_lower in name_fields:
                        name_fields[k_lower] = value.strip()

        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("Google Drive Previews")
            for i, link in enumerate(drive_links):
                file_id = extract_file_id(link)
                if file_id:
                    iframe_url = to_embed_iframe(file_id)

                    # Rotation control
                    rotation_key = f"rotation_{idx}_{i}"
                    if rotation_key not in st.session_state:
                        st.session_state[rotation_key] = 0

                    rotation_angle = st.number_input(
                        f"Rotate File {i+1} (degrees)",
                        min_value=0,
                        max_value=360,
                        value=st.session_state[rotation_key],
                        step=90,
                        key=rotation_key
                    )

                    # Apply rotation in iframe container
                    st.markdown(
                        f"""
                        <div style="width:100%; height:300px; overflow:hidden;">
                            <iframe src="{iframe_url}" width="100%" height="300" style="border:none; transform: rotate({rotation_angle}deg); transform-origin:center;"></iframe>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    # Editable link
                    st.text_input("Link", link, key=f"link_{idx}_{i}")

                else:
                    st.warning(f"Could not extract file ID from: {link}")

        with col2:
            st.subheader("Additional Information")

            # If we have names, display full name first
            if name_fields["first name"] or name_fields["middle name"] or name_fields["last name"]:
                full_name = " ".join(filter(None, [
                    to_proper_case(name_fields["first name"]),
                    to_proper_case(name_fields["middle name"]),
                    to_proper_case(name_fields["last name"])
                ]))
                st.text(f"Full Name: {full_name}")

            # Show all other info
            for item in other_data:
                st.text(item)

        st.markdown("---")
