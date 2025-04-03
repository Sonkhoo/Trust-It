from transformers import pipeline, AutoModelForCausalLM, AutoTokenizer
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import HuggingFacePipeline
import os
from huggingface_hub import login
from dotenv import load_dotenv
import logging
import torch

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables from .env file
load_dotenv()

# Login to Hugging Face
token = os.getenv("HUGGINGFACE_TOKEN")
if not token:
    raise ValueError("HUGGINGFACE_TOKEN not found in environment variables")
login(token)

# Load pre-trained scam detection model
# Using a publicly available model for text classification
try:
    scam_classifier = pipeline(
        "text-classification",
        model="facebook/roberta-hate-speech-dynabench-r4-target",
        max_length=512,  # Set appropriate max length
        truncation=True  # Enable truncation
    )
    logger.info("Successfully loaded scam classifier model")
except Exception as e:
    logger.error(f"Error loading scam classifier: {str(e)}")
    raise

# Setup explanation generator
prompt_template = """
Analyze this message and explain why it might be spam:
Message: {text}
Classification: {label} ({score:.2f}%)
"""

# Use a smaller model for explanation generation
try:
    # Load model and tokenizer directly
    model_id = "facebook/opt-125m"
    tokenizer = AutoTokenizer.from_pretrained(model_id)
    model = AutoModelForCausalLM.from_pretrained(model_id)
    
    # Create a custom pipeline with proper parameters
    text_generator = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_length=256,
        max_new_tokens=128,
        do_sample=True,
        temperature=0.7,
        device_map="auto" if torch.cuda.is_available() else "cpu"
    )
    
    # Create the LLM from the pipeline
    llm = HuggingFacePipeline(pipeline=text_generator)
    
    logger.info("Successfully loaded explanation generator model")
except Exception as e:
    logger.error(f"Error loading explanation generator: {str(e)}")
    raise

explanation_chain = LLMChain(
    llm=llm,
    prompt=PromptTemplate.from_template(prompt_template)
)

def analyze_text(text):
    try:
        # Classification
        if not text or len(text.strip()) == 0:
            return {
                "spam_score": 0,
                "label": "safe",
                "explanation": "No text provided for analysis"
            }
            
        # Truncate text to avoid token limits
        truncated_text = text[:512]
        
        # Run classification
        classification = scam_classifier(truncated_text)[0]
        logger.info(f"Classification result: {classification}")
        
        # Generate explanation using the newer invoke method
        explanation = explanation_chain.invoke({
            "text": truncated_text,
            "label": classification['label'],
            "score": classification['score']*100
        })
        
        # Extract the text from the explanation result
        explanation_text = explanation.get('text', 'No explanation available')
        
        return {
            "spam_score": classification['score']*100,
            "label": classification['label'],
            "explanation": explanation_text
        }
    except Exception as e:
        logger.error(f"Error in analyze_text: {str(e)}")
        return {
            "spam_score": 0,
            "label": "error",
            "explanation": f"Error analyzing text: {str(e)}"
        }