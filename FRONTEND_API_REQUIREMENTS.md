# Frontend API Requirements Specification

Based on the frontend React implementation, the following REST APIs are required to power the different sections of the Bureaucracy Automation platform.

---

## 1. Authentication & Role Selection
**Frontend File:** `src/pages/Login.jsx`

### `POST /api/auth/login`
Authenticates the user and returns an access token along with their role layout context.

*   **Request Body (JSON):**
    ```json
    {
      "email": "user@example.com",
      "password": "password123",
      "role": "admin" // admin, company, or customer
    }
    ```
*   **Response (200 OK):**
    ```json
    {
      "token": "jwt_token_string",
      "user": {
        "id": "uuid",
        "email": "user@example.com",
        "role": "admin",
        "name": "John Doe"
      }
    }
    ```

---

## 2. Admin / Government Dashboard
**Frontend File:** `src/pages/Home.jsx`

### `GET /api/admin/metrics`
Fetches the key statistics for the top metrics section.

*   **Request Params:** `None` (Requires Bearer Token)
*   **Response (200 OK):**
    ```json
    {
      "totalComplaintsToday": 142,
      "totalComplaintsTrend": "+12%",
      "autoRoutedPercentage": 78,
      "autoRoutedCount": 110,
      "manualReviewPercentage": 22,
      "manualReviewCount": 32,
      "topCategory": "Public Works",
      "topCategoryCount": 45
    }
    ```

### `GET /api/admin/complaints`
Fetches the queue of incoming complaints.

*   **Query Params:** `?status=Needs Review&limit=50&page=1`
*   **Response (200 OK):**
    ```json
    {
      "complaints": [
        {
          "id": "C-8291",
          "text": "I was charged twice for my property tax...",
          "category": "Tax & Billing",
          "confidence": 92,
          "status": "Auto Routed",
          "timestamp": "10:24 AM",
          "fullDescription": "..."
        }
      ]
    }
    ```

### `PUT /api/admin/complaints/:id`
Updates the status, category, or routing of a specific complaint from the side panel.

*   **Request Body (JSON):**
    ```json
    {
      "action": "approve_routing", // approve_routing, change_category, mark_critical
      "newCategory": "Utilities", // Optional if change_category
      "status": "In Progress"
    }
    ```
*   **Response (200 OK):**
    ```json
    {
      "success": true,
      "message": "Complaint updated successfully",
      "complaint": { /* updated object */ }
    }
    ```

---

## 3. Company Dashboard
**Frontend Files:** `src/pages/CompanyDashboard.jsx`, `src/pages/CompanyOpening.jsx`, `src/pages/CompanyQueryChat.jsx`

### `GET /api/company/metrics`
Fetches the corporation-specific metrics (action required, pending review, resolved cases).

*   **Request Params:** `None`
*   **Response (200 OK):**
    ```json
    {
      "actionRequired": 2,
      "pendingReview": 1,
      "resolvedCases": 124,
      "resolutionRate": 96.5,
      "actionsRequiredList": 3 // For company opening page
    }
    ```

### `GET /api/company/queries`
Fetches queries assigned to the specific corporation.

*   **Query Params:** `?status=all&limit=20`
*   **Response (200 OK):**
    ```json
    {
      "queries": [
        {
          "id": "QRY-3042",
          "title": "Service Interruption Response",
          "status": "Action Required",
          "date": "2026-04-20",
          "priority": "High",
          "customer": "John Doe",
          "description": "Customer reports complete internet outage..."
        }
      ]
    }
    ```

### `GET /api/company/queries/:id/chat`
Fetches the query details and chat history for the "Resolution Chat Channel".

*   **Response (200 OK):**
    ```json
    {
      "queryDetails": {
         "id": "QRY-3042",
         "title": "Service Interruption Response",
         "priority": "High",
         "customer": "John Doe",
         "description": "..."
      },
      "messages": [
        {
          "sender": "bot",
          "text": "Automated Context: This is the internal resolution channel...",
          "time": "2026-04-20T09:00:00Z"
        }
      ]
    }
    ```

### `POST /api/company/queries/:id/chat`
Sends a resolution message from the company agent to the customer/bot.

*   **Request Body (JSON):**
    ```json
    {
      "text": "We are looking into this right now."
    }
    ```
*   **Response (200 OK):**
    ```json
    {
      "success": true,
      "message": {
        "sender": "agent",
        "text": "We are looking into this right now.",
        "time": "2026-04-20T09:05:00Z"
      },
      "botResponse": {
        "sender": "bot",
        "text": "System: Message securely recorded...",
        "time": "2026-04-20T09:05:01Z"
      }
    }
    ```

---

## 4. Customer Dashboard
**Frontend Files:** `src/pages/CustomerIntro.jsx`, `src/pages/CustomerDashboard.jsx`

### `POST /api/customer/complaints`
Files a new complaint from the "File a New Complaint" modal/page (implied from CustomerIntro.jsx actions).

*   **Request Body (JSON):**
    ```json
    {
      "title": "Streetlight out in neighborhood",
      "description": "The streetlight at 5th and Main has been out for 3 days.",
      "category": "Maintenance" // Optional
    }
    ```
*   **Response (201 Created):**
    ```json
    {
      "id": "QRY-1030",
      "status": "Pending",
      "message": "Complaint filed successfully."
    }
    ```

### `GET /api/customer/complaints`
Fetches the citizen's own raised queries history.

*   **Request Params:** `None`
*   **Response (200 OK):**
    ```json
    {
      "queries": [
        {
          "id": "QRY-1029",
          "title": "Pothole repair request on 5th Ave",
          "status": "In Progress",
          "date": "2026-04-18",
          "category": "Infrastructure"
        }
      ]
    }
    ```

### `POST /api/customer/chat`
Sends a message to the automated Support Assistant bot in the Customer Dashboard.

*   **Request Body (JSON):**
    ```json
    {
      "text": "I need help tracking my pothole request."
    }
    ```
*   **Response (200 OK):**
    ```json
    {
      "botResponse": "I've received your message. Our system is currently analyzing your request. Is there anything else you'd like to add?"
    }
    ```
