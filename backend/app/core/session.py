"""In-memory session store for hackathon purposes.
Stores the request parameters and generated frames for a session.
"""

from typing import Dict, Any

# Structure: session_id -> { "request": GenerateRequest, "frames": [], "status": "pending" | "generating" | "complete" | "error", "error_msg": "" }
MOCK_REDIS_STORE: Dict[str, Dict[str, Any]] = {}
