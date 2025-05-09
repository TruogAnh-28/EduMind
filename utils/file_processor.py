import shutil
import os
import logging
from fastapi import UploadFile
from core.utils.file import upload_to_s3
from .text_extractor import TextExtractor
from machine.controllers import DocumentsController, ExtractedTextController
from machine.models import Documents
from fastapi import Depends
from machine.providers import InternalProvider
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def sanitize_text(extracted_content):
    """Sanitize text to ensure it's valid UTF-8 without null bytes."""
    if extracted_content is None:
        return None
        
    # Handle different data types
    if isinstance(extracted_content, str):
        # Remove null bytes
        sanitized = extracted_content.replace('\x00', '')
        # Replace other invalid characters with space
        return ''.join(ch if ord(ch) < 0x10000 else ' ' for ch in sanitized)
    elif isinstance(extracted_content, list) or isinstance(extracted_content, dict):
        # For list/dict content, convert to JSON string and sanitize
        import json
        try:
            content_str = json.dumps(extracted_content)
            return sanitize_text(content_str)
        except:
            # If JSON conversion fails, try string conversion
            return sanitize_text(str(extracted_content))
    else:
        # Try string conversion for other types
        return sanitize_text(str(extracted_content))
async def process_document(file: UploadFile, lesson_id: str, description: str, document_controller: DocumentsController = Depends(InternalProvider().get_documents_controller), extracted_text_controller: ExtractedTextController = Depends(InternalProvider().get_extracted_text_controller)) -> dict:
    """
    Handle document processing: extract text, upload to S3, update database
    """
    logger.info("Processing started for file: %s", file.filename)
    
    document_data = {
        "lesson_id": lesson_id,
        "name": file.filename,
        "type": file.content_type,
        "description": description,
        "document_url": "",
        "status": "processing",
        "progress_upload": 0  # 0% progress
    }
    document_record = await document_controller.documents_repository.create(document_data, commit=True)
    try:
        # Copy file to temp path
        temp_path = f"temp_{file.filename}"
        logger.debug("Saving file to temp path: %s", temp_path)
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Update progress 30% (Uploaded)
        update_response = {
            "progress_upload": 30
        }
        logger.info("Updating document progress to 30%% (Uploaded)")
        await document_controller.documents_repository.update(where_=[Documents.id == document_record.id], attributes=update_response, commit=True)

        # Extract text from file, based on content type
        extracted_text = None
        if file.content_type == "application/pdf":
            extracted_text = TextExtractor.extract_pdf(temp_path)
            logger.info("Extracted text from PDF.")
        elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            extracted_text = TextExtractor.extract_docx(temp_path)
            logger.info("Extracted text from DOCX.")
        elif file.content_type == "application/vnd.openxmlformats-officedocument.presentationml.presentation":
            extracted_text = TextExtractor.extract_pptx(temp_path)
            logger.info("Extracted text from PPTX.")

        # Delete temp file
        os.remove(temp_path)
        logger.debug("Temporary file removed: %s", temp_path)

        if not extracted_text:
            update_response = {
                "status": "failed",
                "progress_upload": 100
            }
            logger.error("Text extraction failed for file: %s", file.filename)
            await document_controller.documents_repository.update(where_=[Documents.id == document_record.id], attributes=update_response, commit=True)
            return {"filename": file.filename, "error": "Extraction failed"}

        # Sanitize the extracted text to ensure valid UTF-8
        sanitized_text = sanitize_text(extracted_text)
        
        # Update progress 50% (Extracted)
        update_response = {
            "progress_upload": 50
        }
        logger.info("Updating document progress to 50%% (Text extracted)")
        await document_controller.documents_repository.update(where_=[Documents.id == document_record.id], attributes=update_response, commit=True)

        # Upload to S3
        content = await file.read()
        logger.info("Uploading file to S3: %s", file.filename)
        s3_url = await upload_to_s3(content, file.filename)

        # Update progress 80% (Uploaded to S3)
        update_response = {
            "progress_upload": 80
        }
        logger.info("Updating document progress to 80%% (Uploaded to S3)")
        await document_controller.documents_repository.update(where_=[Documents.id == document_record.id], attributes=update_response, commit=True)

        # Final update (completed)
        update_response = {
            "document_url": s3_url,
            "status": "completed",
            "progress_upload": 100,
            "created_at": datetime.now()
        }
        
        create_response = {
            "document_id": document_record.id,
            "extracted_content": sanitized_text,
            "processing_status": "completed"
        }

        try:
            await extracted_text_controller.extracted_text_repository.create(attributes=create_response, commit=True)
            logger.info("Inserted extracted content into database for document: %s", file.filename)
        except Exception as db_err:
            logger.error(f"Database insertion error for extracted text: {str(db_err)}")
            # Try with fallback minimal content if insertion fails
            create_response["extracted_content"] = f"Text extraction completed for {file.filename}"
            await extracted_text_controller.extracted_text_repository.create(attributes=create_response, commit=True)
        
        await document_controller.documents_repository.update(where_=[Documents.id == document_record.id], attributes=update_response, commit=True)

        return {
            "document_id": document_record.id,
            "filename": file.filename,
            "s3_url": s3_url,
            "status": "completed"
        }

    except Exception as e:
        logger.error("Error processing document %s: %s", file.filename, str(e))
        logger.error(traceback.format_exc())  # Add traceback for better debugging

        update_response = {
            "status": "failed",
            "progress_upload": 100
        }
        await document_controller.documents_repository.update(where_=[Documents.id == document_record.id], attributes=update_response, commit=True)
        return {"filename": file.filename, "error": str(e)}