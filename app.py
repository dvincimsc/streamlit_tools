import re
import pandas as pd
import streamlit as st
from io import StringIO

st.set_page_config(page_title="Name & Percentage Extractor", layout="centered")

st.title("🧹 Data Cleaner: Extract Name & Percentage")
st.write("Paste raw data below. This tool will extract the **name** (before the 'Hub') and the **percentage** value.")

# Text input box
raw_input = st.text_area("📋 Paste Your Data Here", height=300, placeholder="Paste your text...")

def extract_data(raw_input):
    lines = raw_input.strip().splitlines()
    entries = []
    current_entry = []

    for line in lines:
        if re.match(r"^\d+\.$", line.strip()):  # Match "1.", "2.", etc.
            if current_entry:
                entries.append(current_entry)
                current_entry = []
        current_entry.append(line.strip())

    if current_entry:
        entries.append(current_entry)

    results = []

    for entry in entries:
        name = None
        percentage = None

        for i, line in enumerate(entry):
            if "hub" in line.lower():
                # Look back for the first non-numeric line before 'Hub'
                for j in range(i - 1, -1, -1):
                    candidate = entry[j].strip()
                    if not candidate.isdigit():
                        name = candidate
                        break
            if "%" in line:
                match = re.search(r'\d+%+', line)
                if match:
                    percentage = match.group(0)

        if name or percentage:
            results.append({
                "Name": name if name else "N/A",
                "Percentage": percentage if percentage else "N/A"
            })

    return results

# Process and display output
if raw_input.strip():
    data = extract_data(raw_input)
    if data:
        df = pd.DataFrame(data)
        st.success("✅ Extracted Data")
        st.dataframe(df, use_container_width=True)

        # Prepare CSV as string for copy
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        csv_data = csv_buffer.getvalue()

        st.download_button(
            label="📥 Download as CSV",
            data=csv_data,
            file_name="filtered_data.csv",
            mime="text/csv"
        )

        # Optional: Show CSV for copy
        with st.expander("📄 Copy CSV Data"):
            st.code(csv_data, language="csv")
    else:
        st.warning("No valid data extracted.")
