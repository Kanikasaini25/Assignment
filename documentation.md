### System Overview

The system processes CSV files with image URLs, compresses images, and notifies users. Key components:

1. **API Layer**:
   - **Upload API**: Accepts CSV, validates, generates `request_id`, and enqueues tasks.
   - **Status API**: Returns status and output image URLs for a given `request_id`.

2. **Validation Service**: Checks CSV format, headers, and URL validity.

3. **Image Processing Service**: Downloads, compresses (50%), and uploads images to cloud storage (e.g., AWS S3).

4. **Database**:
   - **Requests Table**: Tracks `request_id`, status, and timestamps.
   - **Products Table**: Stores product details and image URLs.

5. **Worker Queue**: Manages async tasks (e.g., image processing) using tools like RabbitMQ or AWS SQS.

6. **Webhook Service**: Notifies users via callback when processing is complete.

7. **Storage Service**: Stores processed images and generates public URLs.

---

### Workflow

1. User uploads CSV → system validates, generates `request_id`, and enqueues task.
2. Workers process images → compress, upload, and store output URLs in the database.
3. User checks status via `request_id` → system returns status and output URLs.
4. On completion, webhook sends a notification with results.

---

### API Docs

#### **Upload API**
- **Endpoint**: `POST /upload`
- **Request**: CSV file.
- **Response**: `request_id`.

#### **Status API**
- **Endpoint**: `GET /status?request_id=<request_id>`
- **Response**: Status and output image URLs (if done).