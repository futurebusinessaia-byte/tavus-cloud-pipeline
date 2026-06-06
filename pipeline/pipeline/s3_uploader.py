import os
import logging
import requests
import boto3
from botocore.exceptions import ClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def stream_video_to_s3(video_url: str, session_id: str) -> dict:
    """
    Streams a video file directly from Tavus to a secure AWS S3 bucket 
    without saving it to local server disk memory.
    """
    bucket_name = os.getenv("SECURE_S3_BUCKET")
    s3_key = f"interviews/{session_id}.mp4"
    
    if not bucket_name:
        raise ValueError("SECURE_S3_BUCKET environment variable is missing.")

    s3_client = boto3.client('s3')
    logger.info(f"Initiating stream transfer for Tavus Session: {session_id}")
    
    try:
        with requests.get(video_url, stream=True) as response:
            response.raise_for_status()
            
            s3_client.upload_fileobj(
                Fileobj=response.raw, 
                Bucket=bucket_name, 
                Key=s3_key,
                ExtraArgs={
                    "ServerSideEncryption": "aws:kms"
                }
            )
            
        logger.info(f"Successfully secured session {session_id} to S3.")
        return {"status": "success", "s3_path": f"s3://{bucket_name}/{s3_key}"}

    except ClientError as e:
        logger.error(f"AWS S3 Upload Error: {e}")
        return {"status": "error", "message": "Failed to upload to cloud storage."}
    except requests.RequestException as e:
        logger.error(f"Tavus Video Stream Fetch Error: {e}")
        return {"status": "error", "message": "Failed to stream video from Tavus API."}
