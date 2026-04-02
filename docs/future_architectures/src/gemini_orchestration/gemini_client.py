import os
import json
import logging
import google.generativeai as genai
from PIL import Image

class GeminiMultimodalClient:
    """
    The Digital Oversoul interface. This client establishes a persistent, 
    multimodal connection to Gemini 3.1 Pro, allowing the digital layer to 
    act as the Priors Generator in the Active Inference loop.
    """
    def __init__(self, system_instruction: str = None):
        # Initialize the API using the environment variable
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("CRITICAL: GEMINI_API_KEY environment variable not set.")
            
        genai.configure(api_key=api_key)
        
        # We rely on Gemini 3.1 Pro for its advanced multimodal and long-context reasoning
        self.model_name = 'gemini-3.1-pro'
        
        # Default system instruction sets the conceptual framework for the model
        default_instruction = (
            "You are the orchestration layer for a bio-digital supercomputer. "
            "You will receive visual data from bioreactor microscopy and temporal "
            "data from neural telemetry. Your task is to maintain tissue viability, "
            "prevent necrotic core formation, and optimize synaptic integration."
        )
        
        self.system_instruction = system_instruction or default_instruction
        self.model = genai.GenerativeModel(
            model_name=self.model_name,
            system_instruction=self.system_instruction
        )
        logging.info(f"Initialized {self.model_name} Multimodal Client.")

    def analyze_bioreactor_state(self, image_path: str, telemetry_context: dict) -> dict:
        """
        Passes live microscopy and current hardware telemetry to Gemini for 
        a holistic, multimodal assessment of the organoid's health and computational readiness.
        """
        try:
            microscopy_frame = Image.open(image_path)
        except FileNotFoundError:
            logging.error(f"Microscopy frame not found at {image_path}")
            return {}

        prompt = f"""
        Analyze the provided microscopy frame of the cortical organoid.
        Current Hardware Telemetry:
        {json.dumps(telemetry_context, indent=2)}

        Evaluate the following parameters:
        1. Necrotic Core Risk: Are there dark, dense central regions indicating hypoxia?
        2. Synaptic Density: Is there healthy neurite outgrowth at the periphery?
        3. Hardware Adjustment: Provide specific integer adjustments for perfusion 
           flow rate (ul/min) and orbital agitation (RPM).

        Return ONLY a valid JSON object with the keys: 
        "necrotic_risk_level" (string: low/medium/high/critical), 
        "synaptic_health" (string: poor/stable/optimal), 
        "target_perfusion_ul_min" (float), 
        "target_agitation_rpm" (int).
        """
        
        response = self.model.generate_content([prompt, microscopy_frame])
        
        try:
            # Strip markdown formatting if present and parse JSON
            cleaned_response = response.text.replace('```json', '').replace('```', '').strip()
            return json.loads(cleaned_response)
        except json.JSONDecodeError as e:
            logging.error(f"Failed to parse Gemini response into JSON: {e}")
            logging.debug(f"Raw response: {response.text}")
            return {}
