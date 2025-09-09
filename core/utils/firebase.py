from __future__ import annotations
from typing import Any, Dict, Optional
import json
import os

import firebase_admin
from firebase_admin import credentials, auth

from ..config import settings


_firebase_app: Optional[firebase_admin.App] = None


def _load_credentials():
    if settings.firebase_credentials_file:
        # Prefer file path
        cred_path = settings.firebase_credentials_file
        if os.path.exists(cred_path):
            return credentials.Certificate(cred_path)
        # If not a file path, try to treat it as JSON string
        try:
            data = json.loads(settings.firebase_credentials_file)
            return credentials.Certificate(data)
        except json.JSONDecodeError:
            raise RuntimeError("Invalid firebase_credentials_file: not a valid path or JSON")
    # Fallback: environment GOOGLE_APPLICATION_CREDENTIALS or default
    if os.getenv("GOOGLE_APPLICATION_CREDENTIALS"):
        return credentials.ApplicationDefault()
    raise RuntimeError("Firebase credentials not configured. Set firebase_credentials_file or GOOGLE_APPLICATION_CREDENTIALS")


def get_firebase_app() -> firebase_admin.App:
    global _firebase_app
    if _firebase_app is None:
        cred = _load_credentials()
        _firebase_app = firebase_admin.initialize_app(cred, {
            "projectId": settings.firebase_project_id,
        } if settings.firebase_project_id else None)
    return _firebase_app


def verify_id_token(id_token: str) -> Dict[str, Any]:
    app = get_firebase_app()
    decoded = auth.verify_id_token(id_token, app=app)
    return decoded


firebase_app = get_firebase_app


