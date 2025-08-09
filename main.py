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

st.title("📁 Google Drive Viewer with Metadata Display")

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
        st.markdown(f"### 📄 Record {idx + 1}")

        drive_links = [item for item in record if "drive.google.com" in item]
        other_data = [item for item in record if "drive.google.com" not in item]

        col1, col2 = st.columns([2, 1])

        with col1:
            st.subheader("📸 Google Drive Previews")
            for i, link in enumerate(drive_links):
                file_id = extract_file_id(link)
                if file_id:
                    iframe_url = to_embed_iframe(file_id)
                    st.markdown(
                        f'<iframe src="{iframe_url}" width="100%" height="300" style="border: none;"></iframe>',
                        unsafe_allow_html=True
                    )
                    st.text_input("📋 Copyable Link", link, key=f"link_{idx}_{i}", disabled=True)
                else:
                    st.warning(f"⚠️ Could not extract file ID from: {link}")

        with col2:
            st.subheader("📝 Additional Information")
            for i, item in enumerate(other_data):
                st.text(item if i == 0 else item.upper())

        # Horizontal separator between records
        st.markdown("---")
