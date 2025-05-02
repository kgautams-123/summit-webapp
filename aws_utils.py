import boto3
import streamlit as st
from typing import List
import tempfile
from PIL import Image
import io

class AWSManager:
    def __init__(self, region="us-east-1"):
        self.region = region
        self.bedrock_runtime = boto3.client("bedrock-runtime", region_name=region)
        self.s3_client = boto3.client("s3", region_name=region)

    def get_product_images_from_s3(self, bucket_name: str, prefix: str) -> List[dict]:
        """Fetch product images from S3 bucket"""
        try:
            response = self.s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
            products = []
            for obj in response.get('Contents', []):
                if obj['Key'].lower().endswith(('.png', '.jpg', '.jpeg')):
                    url = self.s3_client.generate_presigned_url('get_object',
                        Params={'Bucket': bucket_name, 'Key': obj['Key']},
                        ExpiresIn=3600)
                    
                    product_name = obj['Key'].split('/')[-1].split('.')[0].replace('_', ' ').title()
                    
                    products.append({
                        'name': product_name,
                        'image_url': url,
                        'key': obj['Key']
                    })
            return products
        except Exception as e:
            st.error(f"Error fetching products from S3: {str(e)}")
            return []

    def load_image_from_s3(self, bucket: str, key: str) -> bytes:
        """Load an image from S3 and return as bytes"""
        try:
            response = self.s3_client.get_object(Bucket=bucket, Key=key)
            image_content = response['Body'].read()
            
            # Verify the image can be opened
            Image.open(io.BytesIO(image_content))
            
            return image_content
        except Exception as e:
            st.error(f"Error loading image from S3: {str(e)}")
            return None

    def generate_presigned_url(self, s3_uri):
        s3_parts = s3_uri.replace("s3://", "").split("/", 1)
        bucket_name = s3_parts[0]
        object_key = s3_parts[1] + "/output.mp4"
        presigned_url = self.s3_client.generate_presigned_url(
            "get_object",
            Params={"Bucket": bucket_name, "Key": object_key},
            ExpiresIn=3600 * 24
        )
        return presigned_url
