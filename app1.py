import streamlit as st
from pathlib import Path
import google.generativeai as genai

from app import api_key

# Configure genai with API key
genai.configure(api_key=api_key)

# Set up the models
generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

# apply safety settings
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

# Model configuration
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    safety_settings=safety_settings
)

#page configuration
st.set_page_config(page_title="VitalImage Analytics", page_icon=":robot:")

#logo
#st.image("skill_curb.jpeg", width=60)

# title
st.title("🧑‍⚕️ Your Doctor Image 📷 Analysis")

#subtitle
st.subheader("An application that can help users identify medical images")

# upload the dieseases image
uploaded_file = st.file_uploader("Upload the medical image for analysis", type=["png", "jpg", "jpeg"])
if uploaded_file:
    st.image(uploaded_file,width=350,caption="Uploaded Dieases Image")

# create a submit button
submit_button = st.button("Generate the Analysis")

if submit_button:
    if uploaded_file is not None:
        #process the uploaded image
        image_data = uploaded_file.getvalue()

        # image ready
        image_parts = [
            {
                "mime_type": "image/jpeg",  # Corrected 'mime_type'
                "data": image_data
            },
        ]

        # making a prompt ready
        prompt_parts = [
            image_parts[0],
            system_prompt,
        ]

        # #Generative a response based on promt and image
        st.title("Here is the analysis based on your image ")
        response = model.generate_content(prompt_parts)
        # Display the generated response text
        st.write(response.text)

    else:
        st.error("Please upload a valid medical image to proceed.")
