# **Trust-It**

### **Collaborative AI-Powered Fraud Detection and Reporting Platform**

A platform designed to help users and organizations identify and prevent scams using AI and community-driven reporting.

---

### **Core Features (MVP)**

**1. Spam Screenshot Detection (OCR + AI)**
✅ Users upload screenshots of suspicious messages.  
✅ Google Vision API (OCR) extracts text.  
✅ Google Gemini AI / Vertex AI analyzes message for fraud patterns.  
✅ AI assigns a Spam Score (0-100%) with an explanation.  

 **2. Collaborative Spam Reporting**
✅ Users & verified organizations report new scams (text, URLs, call scripts).  
✅ Stored in a public spam database (Supabase/PostgreSQL).  
✅ AI learns from new reports and adapts fraud detection.  

**3. AI Model Updates with Community Input**
✅ AI analyzes newly reported scams and refines detection rules.  
✅ Uses Google Vertex AI AutoML to retrain model over time.  
✅ Spam detection improves as database grows.  

**4. Scam Awareness Hub**
✅ Publicly accessible list of latest scams (trending frauds, patterns, etc.).  
✅ Verified users (Govt/Companies) can tag scams as Critical.  
✅ AI-generated scam summaries using Google Gemini AI.  

---

## **Low-Level Design (LLD)**

### **System Architecture Overview**

- **Frontend**: Next.js - User interface for uploading screenshots & reporting scams.  
- **Backend**: Node.js + Express - API to handle OCR, AI analysis, and scam reporting.  
- **Database**: MongoDB - Store reported scams, user data, and AI model updates.  
- **AI Processing**: Python (**Google Gemini AI** & **Vertex AI** for spam detection, **Google Cloud Vision** for OCR, **Google Safe Browsing API** → Detect phishing URLs).  
- **AI API Handling**: FastAPI - API routes for AI-related tasks.  
- **Hosting & Deployment**: Vercel, Google Cloud Run (Backend & AI API).  

---

### **Database Schema (MongoDB)**

#### **Users Collection**
```json
{
    "_id": ObjectId,
    "name": "string",
    "email": "string",
    "password_hash": "string",
    "role": "user" | "verified_org" | "admin",
    "created_at": "timestamp"
}
```

#### **Scam Reports Collection**
```json
{
    "_id": ObjectId,
    "user_id": ObjectId,
    "scam_type": "SMS" | "Call" | "Email" | "Other",
    "scam_text": "string",
    "scam_url": "string",
    "scam_source": "string",
    "status": "pending" | "verified" | "rejected",
    "created_at": "timestamp"
}
```

#### **AI Model Feedback Collection**
```json
{
    "_id": ObjectId,
    "report_id": ObjectId,
    "spam_score": "float",
    "ai_analysis": "string",
    "user_feedback": "fraud" | "safe" | "unsure",
    "created_at": "timestamp"
}
```

---

### **API Design**

#### **1. User Authentication APIs (Express)**
- **User Registration**: `POST /api/auth/register`  
- **User Login**: `POST /api/auth/login`  
- **Get User Profile**: `GET /api/auth/profile`  

#### **2. Scam Detection APIs (FastAPI for AI tasks, Express for standard APIs)**
- **Upload Screenshot for OCR** (Express): `POST /api/scam/upload`  
  - Extracts text using Google Vision API.  
  - Returns extracted text for fraud analysis.  
- **Analyze Text for Scam** (FastAPI): `POST /api/ai/analyze`  
  - Uses Google Gemini AI to classify as spam/safe.  
  - Returns fraud likelihood score (0-100%).  

#### **3. Scam Reporting APIs (Express)**
- **Report New Scam**: `POST /api/scam/report`  
  - Allows users/organizations to submit new scam messages.  
- **Get Reported Scams (Public List)**: `GET /api/scam/reports`  
  - Fetches latest scams from verified sources.  
- **Verify Scam Report (Admin Only)**: `PATCH /api/scam/verify/:report_id`  
  - Admins/verified orgs can approve/reject scam reports.  

#### **4. AI Model Training APIs (FastAPI)**
- **Retrain AI Model with New Scam Data**: `POST /api/ai/retrain`  
  - Uses Google Vertex AI to update fraud detection model.  

#### **5. Feedback & Community APIs (Express)**
- **Submit User Feedback on AI Detection**: `POST /api/scam/feedback`  
- **Get Scam Awareness Articles**: `GET /api/scam/awareness`  

---

### **Data Flow**

1. User uploads a screenshot → OCR extracts text.  
2. Text is analyzed by AI (Google Gemini + Vertex AI via FastAPI).  
3. Fraud Score & Explanation is returned.  
4. Users/Govt can report new scams (stored in MongoDB & used for AI retraining).  
5. AI model updates dynamically with new scam patterns over time.  

---

## **Frontend Pages**

### **1. Home & Dashboard Page**
- Overview of the platform.  
- Quick access to scam detection, reports, and educational content.  
- Shows user statistics (e.g., number of scams detected, recent reports).  

### **2. Upload & Detect Scam Page**
- Users upload screenshots of messages.  
- AI analyzes and returns fraud likelihood score.  
- Explanation of why a message may be fraudulent.  

### **3. Report a Scam Page**
- Users manually submit scam messages/calls they encountered.  
- Form to submit scam details (type, text, source).  
- Option for government/private organizations to verify scams.  

### **4. Browse Reported Scams Page**
- Displays a list of user/government-reported scams.  
- Search & filter by scam type (SMS, Call, Email).  
- Users can comment/validate reported scams.  

---

## **MVP Roadmap**

### **📌 Phase 1: Core AI Spam Detection**
✅ Implement OCR (Google Vision API) to extract text.  
✅ Use Google Gemini AI to classify messages as Spam/Not Spam.  
✅ Display Spam Score with reasons.  

### **📌 Phase 2: User-Reported Scam Database**
✅ Build a form for users to submit new scam messages.  
✅ Store scams in Supabase/PostgreSQL.  
✅ Expose reported scams in a public scam list.  

### **📌 Phase 3: AI Model Updates**
✅ Train Google Vertex AI AutoML on reported scams.  
✅ Integrate AutoML model into detection pipeline.  
✅ Automatically improve detection accuracy as more data comes in.  

### **📌 Phase 4: Scam Awareness & Community**
✅ Add scam trends & AI-generated scam summaries.  
✅ Allow verified organizations to tag & approve scam reports.  
✅ Notify users of emerging fraud threats.  

---

## **Future Enhancements**
✅ Real-time call monitoring using VoIP analysis (for fraud call detection).  
✅ AI-generated scam alerts (push notifications for trending scams).  
✅ Blockchain-based scam verification for immutable records.  

