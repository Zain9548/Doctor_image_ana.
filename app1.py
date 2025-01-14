import streamlit as st
from pathlib import Path
import openai

# Configure OpenAI with API key
openai.api_key = "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"  

# Set up the model parameters
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

# apply safety settings (same as before if needed)
safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

# System prompt for the model
system_prompt = """
As a highly skilled medical practitioner specializing in image analysis, you are tasked with examining medical images for a renowned hospital.
Your expertise is crucial in identifying any anomalies, diseases, or health issues that may be present in the images.

Your Responsibilities include:

1. Detailed Analysis: Thoroughly analyze each image, focusing on identifying any abnormal findings.
2. Findings Report: Document all observed anomalies or signs of disease. Clearly articulate these findings in a structured format.
3. Recommendations and Next Steps: Based on your analysis, suggest potential next steps, including further tests or treatments as applicable.
4. Treatment Suggestions: If appropriate, recommend possible treatment options or interventions.

Important Notes:
1. Scope of Response: Only respond if the image pertains to human health issues.
2. Clarity of Image: In cases where the image quality impedes clear analysis, note that certain details may be obscured.
3. Disclaimer: Accompany your analysis with the disclaimer: "Consult with a Doctor before making any decisions".
4. Your insights are invaluable in guiding clinical decisions. Please proceed with the analysis, adhering to the structured approach outlined above.

Please provide me an output response with these 4 headings Detailed Analysis,finding Report,Recommendation and Next steps,Treatment Suggestion
"""

# page configuration
st.set_page_config(page_title="VitalImage Analytics", page_icon=":robot:")

# title
st.title("🧑‍⚕️ Your Doctor Image 📷 Analysis")

# subtitle
st.subheader("An application that can help users identify medical images")

# upload the diseases image
uploaded_file = st.file_uploader("Upload the medical image for analysis", type=["png", "jpg", "jpeg"])
if uploaded_file:
    st.image(uploaded_file, width=350, caption="Uploaded Disease Image")

# create a submit button
submit_button = st.button("Generate the Analysis")

if submit_button:
    if uploaded_file is not None:
        # process the uploaded image
        image_data = uploaded_file.getvalue()

        # OpenAI does not support image generation directly, so we need to use the image analysis API here.
        # You can send the image to a service (or model) that handles medical image analysis, and then use OpenAI for the textual response.

        # For now, let's use a simple text prompt to simulate the analysis:
        response = openai.Completion.create(
            engine="text-davinci-003",  # You can replace this with a model of your choice
            prompt=system_prompt,
            max_tokens=4096,
            temperature=0.4
        )

        # Display the generated response text
        st.write(response.choices[0].text)

    else:
        st.error("Please upload a valid medical image to proceed.")
