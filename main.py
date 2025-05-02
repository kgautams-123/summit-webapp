import streamlit as st
import requests
import urllib.parse
import base64
import io
from PIL import Image
from styles import custom_css
from aws_utils import AWSManager
from helpers import prepare_reference_image, check_job_status, show_loading_animation

# AWS Configuration
AWS_REGION = "us-east-1"
OUTPUT_S3_BUCKET = "aws-summit-nova-reel"
OUTPUT_S3_PREFIX = "nova-reel-output/"
CATALOG_BUCKET = "aws-summit-product-catalog"
MODEL_ID = "amazon.nova-reel-v1:1"

# Product Categories
PRODUCT_CATEGORIES = {
    "Food & Beverages": "products/food/",
    "Electronics": "product-catalog/electronics/",
    "Fashion": "product-catalog/fashion/",
    "Home & Living": "product-catalog/home-living/",
    "Beauty & Personal Care": "product-catalog/beauty/"
}

# Initialize AWS Manager
aws_manager = AWSManager(AWS_REGION)

def create_video(key_suffix=""):
    """Helper function for video creation interface"""
    st.markdown("### ✨ Create Your Video")
    
    # Prompt input with unique key
    prompt = st.text_area(
        "Describe how you want your video to look",
        value=st.session_state.current_prompt or f"Create a cinematic video showcasing {st.session_state.selected_image_name} with dynamic camera movements and professional lighting.",
        height=100,
        key=f"prompt_input_{key_suffix}"  # Add unique key
    )
    
    # Generate Video Button
    if st.button("🚀 Generate Video", 
                 type="primary", 
                 use_container_width=True,
                 key=f"generate_btn_{key_suffix}"):  # Add unique key for button
        if not prompt.strip():
            st.error("Please enter a prompt before generating the video.")
            return

        try:
            base64_image = prepare_reference_image(st.session_state.selected_image)
            model_input = {
                "taskType": "TEXT_VIDEO",
                "textToVideoParams": {
                    "text": prompt,
                    "images": [{"format": "jpeg", "source": {"bytes": base64_image}}]
                },
                "videoGenerationConfig": {
                    "durationSeconds": 6,
                    "fps": 24,
                    "dimension": "1280x720"
                }
            }

            output_config = {
                "s3OutputDataConfig": {
                    "s3Uri": f"s3://{OUTPUT_S3_BUCKET}/{OUTPUT_S3_PREFIX}"
                }
            }
            
            with st.spinner("🎥 Creating your video..."):
                response = aws_manager.bedrock_runtime.start_async_invoke(
                    modelId=MODEL_ID,
                    modelInput=model_input,
                    outputDataConfig=output_config
                )

            s3_uri = check_job_status(aws_manager.bedrock_runtime, response["invocationArn"])

            if s3_uri:
                presigned_url = aws_manager.generate_presigned_url(s3_uri)
                st.video(presigned_url)
                
                col1, col2 = st.columns(2)
                with col1:
                    video_content = requests.get(presigned_url).content
                    b64_video = base64.b64encode(video_content).decode()
                    st.markdown(f"""
                        <a href="data:video/mp4;base64,{b64_video}" 
                           download="generated_video.mp4" 
                           class="download-button">
                           📥 Download Video
                        </a>
                    """, unsafe_allow_html=True)
                
                with col2:
                    linkedin_text = f"""🌟 Check out this AI-generated video created using Amazon Bedrock and Nova Reel! #AI #Marketing #GenerativeAI"""
                    linkedin_url = f"https://www.linkedin.com/feed/?shareActive=true&text={urllib.parse.quote(linkedin_text)}"
                    st.markdown(f"""
                        <a href="{linkedin_url}" 
                           target="_blank" 
                           class="download-button linkedin">
                           📤 Share on LinkedIn
                        </a>
                    """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"❌ Error: {e}")


# Page configuration
st.set_page_config(
    page_title="AI Motion Ad Creator",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Inject custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

# Modern animated header
st.markdown("""
    <div class="header-container">
        <h1 style='font-size: 2.5rem; font-weight: 700; margin-bottom: 0.5rem;'>🎬 AI Motion Ad Creator</h1>
        <p style='font-size: 1.2rem; opacity: 0.9;'>Transform your product images into stunning video content with AI</p>
    </div>
""", unsafe_allow_html=True)

# Initialize session state
if 'selected_image' not in st.session_state:
    st.session_state.selected_image = None
if 'selected_image_name' not in st.session_state:
    st.session_state.selected_image_name = None
if 'current_prompt' not in st.session_state:
    st.session_state.current_prompt = ""

# Sidebar with Creative Prompts
with st.sidebar:
    st.markdown("### 💡 Creative Inspiration")
    
    showcase_prompts = {
        "Cinematic": [
            "Cinematic dolly shot with beautiful lighting and focus transitions",
            "Epic reveal with dramatic lighting and depth of field",
            "Luxury showcase with golden hour lighting"
        ],
        "Dynamic": [
            "360-degree pan around the product with particle effects",
            "Dynamic camera movement with smooth transitions",
            "Top-down to eye-level dramatic reveal"
        ],
        "Modern": [
            "Modern tech-style presentation with floating elements",
            "Clean minimal showcase with subtle motion",
            "Professional feature highlight with sleek transitions"
        ]
    }
    
    selected_style = st.selectbox("Select Style", list(showcase_prompts.keys()))
    
    for prompt in showcase_prompts[selected_style]:
        if st.button(prompt, key=f"prompt_{prompt}", use_container_width=True):
            st.session_state.current_prompt = prompt
            st.rerun()

# Main content area
tab1, tab2 = st.tabs(["📑 Product Catalog", "⬆️ Custom Upload"])

# Product Catalog Tab
with tab1:
    col1, col2 = st.columns([0.4, 0.6])
    
    # In the Product Catalog Tab section:
    with col1:
        st.markdown("### Select Product")
        selected_category = st.selectbox(
            "Product Category",
            options=list(PRODUCT_CATEGORIES.keys()),
            key="category_selector"
        )
        
        products = aws_manager.get_product_images_from_s3(
            CATALOG_BUCKET, 
            PRODUCT_CATEGORIES[selected_category]
        )
        
        if not products:
            st.warning(f"No products found in {selected_category} category.")
        else:
            st.markdown("#### Available Products")
            
            # Display products in a grid
            cols = st.columns(3)
            for idx, product in enumerate(products):
                with cols[idx % 3]:
                    st.image(product['image_url'], 
                            caption=product['name'],
                            use_container_width=True)
                    
                    if st.button("Select", key=f"btn_{product['name']}", use_container_width=True):
                        selected_image_bytes = aws_manager.load_image_from_s3(
                            CATALOG_BUCKET, 
                            product['key']
                        )
                        if selected_image_bytes:
                            # Store the binary data in session state
                            st.session_state.selected_image = selected_image_bytes
                            st.session_state.selected_image_name = product['name']
                            st.rerun()

    # Update the image display section:
    if st.session_state.selected_image:
        st.markdown('<div class="selected-image-container">', unsafe_allow_html=True)
        
        # Display selected image
        col_img, col_btn = st.columns([0.6, 0.4])
        with col_img:
            st.markdown(f"#### Selected: {st.session_state.selected_image_name}")
            # Create PIL Image from bytes
            image = Image.open(io.BytesIO(st.session_state.selected_image))
            st.image(image)
                
            with col_btn:
                if st.button("🔄 Change"):
                    st.session_state.selected_image = None
                    st.session_state.selected_image_name = None
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Video creation interface
            create_video(key_suffix="catalog") 

# Custom Upload Tab
# In the Custom Upload Tab section, replace with:
with tab2:
    col1, col2 = st.columns([0.4, 0.6])
    
    with col1:
        st.markdown("### Upload Your Image")
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=["png", "jpg", "jpeg"],
            help="For best results, use a 1280x720 resolution image"
        )
        
        if uploaded_file:
            # Read the file content
            image_bytes = uploaded_file.read()
            st.image(image_bytes, caption="Preview", use_container_width=True)
            if st.button("Use This Image", use_container_width=True):
                st.session_state.selected_image = image_bytes
                st.session_state.selected_image_name = "Custom Image"
                st.rerun()
    
    with col2:
        if st.session_state.selected_image:
            st.markdown('<div class="selected-image-container">', unsafe_allow_html=True)
            
            # Display selected image
            col_img, col_btn = st.columns([0.8, 0.2])
            with col_img:
                st.markdown(f"#### Selected: {st.session_state.selected_image_name}")
                # Create PIL Image from bytes
                image = Image.open(io.BytesIO(st.session_state.selected_image))
                st.image(image, use_container_width=True)
            
            with col_btn:
                if st.button("🔄 Change", key="change_custom"):
                    st.session_state.selected_image = None
                    st.session_state.selected_image_name = None
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Video creation interface
            create_video(key_suffix="custom")


# Footer
st.markdown("""
    <div style='text-align: center; padding: 2rem 0; color: var(--text-secondary); margin-top: 2rem;'>
        <p style='margin-bottom: 0.5rem;'>Created with ❤️ using Amazon Bedrock and Nova Reel 1.1</p>
    </div>
""", unsafe_allow_html=True)
