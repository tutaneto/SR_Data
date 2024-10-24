"""
Streamlit-based visual interface for SR_Data visualization selection
"""
import streamlit as st
import os
import json

def main():
    st.title("SR_Data Visualization Interface")

    # Visualization Type Selection
    viz_type = st.selectbox(
        "Select Visualization Type",
        ["IPCA", "SELIC", "PIB_IBGE", "Ibov_Dolar"]
    )

    # Time Range Selection
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date")
    with col2:
        end_date = st.date_input("End Date")

    # Aspect Ratio Selection
    aspect_ratio = st.selectbox(
        "Select Aspect Ratio",
        ["1:1", "9:18", "18:9", "16:9", "4:3"]
    )

    # Additional Parameters
    num_columns = st.slider("Number of Columns", 1, 4, 1)

    # Generate Button
    if st.button("Generate Visualization"):
        # Create queue entry
        queue_dir = "../wwwsec/output"
        os.makedirs(queue_dir, exist_ok=True)

        # Save parameters
        params = {
            "type": viz_type,
            "start_date": start_date.strftime("%Y-%m-%d"),
            "end_date": end_date.strftime("%Y-%m-%d"),
            "aspect_ratio": aspect_ratio,
            "num_columns": num_columns
        }

        # Write to queue
        with open(os.path.join(queue_dir, "queue.txt"), "w") as f:
            f.write(f"1 {viz_type}")

        # Save parameters for the visualization
        with open(os.path.join(queue_dir, "viz_params.json"), "w") as f:
            json.dump(params, f)

        st.success(f"Added {viz_type} visualization to queue!")
        st.info("The generated image will be available in the graphics/ folder")

if __name__ == "__main__":
    main()
