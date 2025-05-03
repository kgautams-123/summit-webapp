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
OUTPUT_S3_BUCKET = "aws-summit-nova-reel-2"
OUTPUT_S3_PREFIX = "nova-reel-output/"
CATALOG_BUCKET = "aws-summit-product-catalog-2"
MODEL_ID = "amazon.nova-reel-v1:1"

# Product Categories
PRODUCT_CATEGORIES = {
    "Food & Beverages": "products/food/",
    "Electronics": "products/electronics/",
    "Home & Living": "products/home-living/"
}

# Initialize AWS Manager
aws_manager = AWSManager(AWS_REGION)

def create_video(key_suffix=""):
    st.markdown("### ✨ Create Your Video")
    prompt = st.text_area(
        "Describe how you want your video to look",
        value=st.session_state.current_prompt or (
            f"Create a cinematic video showcasing {st.session_state.selected_image_name} with dynamic camera movements and professional lighting."
            if st.session_state.selected_image_name else
            "Create a cinematic video with dynamic camera movements and professional lighting."
        ),
        height=100,
        key=f"prompt_input_{key_suffix}"
    )

    if st.button("🚀 Generate Video", type="primary", use_container_width=True, key=f"generate_btn_{key_suffix}"):
        if not prompt.strip():
            st.error("Please enter a prompt before generating the video.")
            return

        try:
            text_to_video_params = {"text": prompt}
            if st.session_state.selected_image:
                base64_image = prepare_reference_image(st.session_state.selected_image)
                text_to_video_params["images"] = [{"format": "jpeg", "source": {"bytes": base64_image}}]
            model_input = {
                "taskType": "TEXT_VIDEO",
                "textToVideoParams": text_to_video_params,
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
                    linkedin_text = "🌟 Check out this AI-generated video created using Amazon Bedrock and Nova Reel! #AI #AWS #AWSSummitBengaluru"
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

def create_video_from_prompt():
    st.markdown("### ✨ Generate Video with Custom Prompt")
    st.markdown("Create a video using just your prompt without requiring an image.")
    prompt = st.text_area(
        "Enter your detailed video prompt",
        value="Create a cinematic video with dynamic camera movements and professional lighting.",
        height=150,
        key="custom_prompt_only"
    )
    if st.button("🚀 Generate Video", type="primary", use_container_width=True, key="generate_custom_prompt"):
        if not prompt.strip():
            st.error("Please enter a prompt before generating the video.")
            return
        try:
            text_to_video_params = {"text": prompt}
            model_input = {
                "taskType": "TEXT_VIDEO",
                "textToVideoParams": text_to_video_params,
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
                    linkedin_text = "🌟 Check out this AI-generated video created using Amazon Bedrock and Nova Reel! #AI #AWS #AWSSummitBengaluru"
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
if 'current_product_key' not in st.session_state:
    st.session_state.current_product_key = None

with st.sidebar:
    # --- LinkedIn Post Card ---
    linkedin_text = (
        "🌟 Check out this AI-generated video created using Amazon Bedrock and Nova Reel! "
        "#AI #AWS #AWSSummitBengaluru"
    )
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(90deg, #0077b5 0%, #00a0dc 100%);
            padding: 1.1em 1em 1em 1em;
            border-radius: 14px;
            margin-bottom: 1.5em;
            box-shadow: 0 2px 8px rgba(0,0,0,0.07);
            color: white;
        ">
            <div style="display: flex; align-items: center;">
                <img src="https://cdn-icons-png.flaticon.com/512/174/174857.png" width="28" style="margin-right: 0.7em; border-radius: 6px; box-shadow: 0 2px 6px rgba(0,0,0,0.07);" />
                <span style="font-weight: 600; font-size: 1.09em;">Share on LinkedIn</span>
            </div>
            <div style="margin-top: 1em; background: rgba(255,255,255,0.13); border-radius: 8px; padding: 0.8em; color: #fff;">
                {linkedin_text}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.code(linkedin_text, language="markdown")  # Built-in copy button[2][6]

    # --- Creative Prompts ---
    st.markdown("### 💡 Creative Prompts")
    creative_prompts = [
        "Cinematic dolly shot with beautiful lighting and focus transitions",
        "360-degree pan around the product with particle effects",
        "Modern tech-style presentation with floating elements"
    ]
    for prompt in creative_prompts:
        if st.button(prompt, key=f"prompt_{prompt}", use_container_width=True):
            st.session_state.current_prompt = prompt
            st.rerun()



# Main content area
tab1, tab2, tab3 = st.tabs(["📑 Product Catalog", "⬆️ Custom Upload", "✏️ Prompt Only"])

# Product Catalog Tab
with tab1:
    col1, col2 = st.columns([0.4, 0.6])
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
            # If a product is selected, show only that product
            if st.session_state.selected_image and st.session_state.current_product_key:
                selected_product = next((p for p in products if p['key'] == st.session_state.current_product_key), None)
                if selected_product:
                    st.image(selected_product['image_url'], caption=selected_product['name'], use_container_width=True)
                    if st.button("View All Products", key="view_all", use_container_width=True):
                        st.session_state.selected_image = None
                        st.session_state.selected_image_name = None
                        st.session_state.current_product_key = None
                        st.rerun()
            else:
                cols = st.columns(3)
                for idx, product in enumerate(products):
                    with cols[idx % 3]:
                        st.image(product['image_url'], caption=product['name'], use_container_width=True)
                        if st.button("Select", key=f"btn_{product['name']}", use_container_width=True):
                            selected_image_bytes = aws_manager.load_image_from_s3(
                                CATALOG_BUCKET, 
                                product['key']
                            )
                            if selected_image_bytes:
                                st.session_state.selected_image = selected_image_bytes
                                st.session_state.selected_image_name = product['name']
                                st.session_state.current_product_key = product['key']
                                st.rerun()
    if st.session_state.selected_image:
        st.markdown('<div class="selected-image-container">', unsafe_allow_html=True)
        col_img, col_btn = st.columns([0.6, 0.4])
        with col_img:
            st.markdown(f"#### Selected: {st.session_state.selected_image_name}")
            image = Image.open(io.BytesIO(st.session_state.selected_image))
            st.image(image)
        with col_btn:
            if st.button("🔄 Change"):
                st.session_state.selected_image = None
                st.session_state.selected_image_name = None
                st.session_state.current_product_key = None
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        create_video(key_suffix="catalog")

# Custom Upload Tab
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
            image_bytes = uploaded_file.read()
            st.image(image_bytes, caption="Preview", use_container_width=True)
            if st.button("Use This Image", use_container_width=True):
                st.session_state.selected_image = image_bytes
                st.session_state.selected_image_name = "Custom Image"
                st.session_state.current_product_key = None
                st.rerun()
    with col2:
        if st.session_state.selected_image:
            st.markdown('<div class="selected-image-container">', unsafe_allow_html=True)
            col_img, col_btn = st.columns([0.8, 0.2])
            with col_img:
                st.markdown(f"#### Selected: {st.session_state.selected_image_name}")
                image = Image.open(io.BytesIO(st.session_state.selected_image))
                st.image(image, use_container_width=True)
            with col_btn:
                if st.button("🔄 Change", key="change_custom"):
                    st.session_state.selected_image = None
                    st.session_state.selected_image_name = None
                    st.session_state.current_product_key = None
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
            create_video(key_suffix="custom")

# Custom Prompt Tab (NEW)
with tab3:
    create_video_from_prompt()

# Footer
st.markdown("""
    <div style='text-align: center; padding: 2rem 0; color: var(--text-secondary); margin-top: 2rem;'>
        <p style='margin-bottom: 0.5rem;'>Created with ❤️ using Amazon Bedrock and Nova Reel 1.1</p>
    </div>
""", unsafe_allow_html=True)
