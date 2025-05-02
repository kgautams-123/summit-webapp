import streamlit as st
from PIL import Image
import io
import base64
import time

def show_loading_animation():
    return st.markdown("""
        <div class="loading-animation">
            <div></div>
            <div></div>
            <div></div>
        </div>
    """, unsafe_allow_html=True)

def prepare_reference_image(image_data):
    """Prepare image for API submission"""
    with st.spinner("Processing image..."):
        if isinstance(image_data, bytes):
            img = Image.open(io.BytesIO(image_data))
        else:
            img = Image.open(image_data)
        
        if img.size != (1280, 720):
            st.info(f"📐 Optimizing image resolution from {img.size} to 1280x720")
            img = img.resize((1280, 720), Image.LANCZOS)
        
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            st.info("🎨 Converting image format for compatibility")
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'RGBA':
                background.paste(img, mask=img.split()[3])
            else:
                background.paste(img, mask=img.convert('RGBA').split()[3])
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG', quality=95)
        img_byte_arr.seek(0)
        return base64.b64encode(img_byte_arr.getvalue()).decode('utf-8')

def check_job_status(bedrock_runtime, job_arn):
    progress_bar = st.progress(0)
    status_text = st.empty()
    loading_placeholder = st.empty()
    
    start_time = time.time()
    expected_duration = 300
    
    while True:
        try:
            response = bedrock_runtime.get_async_invoke(invocationArn=job_arn)
            status = response["status"]
            
            elapsed_time = time.time() - start_time
            progress = min(elapsed_time / expected_duration, 0.99)
            progress_bar.progress(progress)
            
            if status == "Completed":
                progress_bar.progress(1.0)
                status_text.success("🎉 Video generation completed!")
                loading_placeholder.empty()
                return response["outputDataConfig"]["s3OutputDataConfig"]["s3Uri"]
            elif status == "Failed":
                error_message = response.get("failureMessage", "Unknown error")
                if "content filters" in error_message.lower():
                    status_text.error("🚫 Content blocked by AWS filters. Please adjust your prompt or image.")
                else:
                    status_text.error(f"❌ Generation failed: {error_message}")
                loading_placeholder.empty()
                return None
            else:
                status_text.info("🎥 Creating your video... (3-5 minutes)")
                time.sleep(15)
        except Exception as e:
            status_text.error(f"❌ Error: {e}")
            loading_placeholder.empty()
            return None
