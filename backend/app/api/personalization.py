"""Personalization endpoints: API keys, workspaces, templates, notifications"""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional
from datetime import datetime, timedelta
import uuid

from app.core.auth import get_current_user, APIKeyManager
from app.schemas.user import (
    APIKeyCreate,
    APIKeyResponse,
    APIKeyUpdate,
    WorkspaceCreate,
    WorkspaceResponse,
    WorkspaceMemberAdd,
    ExperimentTemplateCreate,
    ExperimentTemplateResponse,
    NotificationResponse
)

router = APIRouter(prefix="/personalization", tags=["personalization"])

# Mock databases
API_KEYS_DB = {}
WORKSPACES_DB = {}
TEMPLATES_DB = {}
NOTIFICATIONS_DB = {}


# ==================== API Keys ====================

@router.post("/api-keys", response_model=APIKeyResponse, status_code=status.HTTP_201_CREATED)
async def create_api_key(
    key_data: APIKeyCreate,
    current_user_id: str = Depends(get_current_user)
) -> APIKeyResponse:
    """Create a new API key for user"""
    
    key_id = str(uuid.uuid4())
    raw_key = APIKeyManager.generate_api_key()
    hashed_key = APIKeyManager.hash_api_key(raw_key)
    
    expires_at = None
    if key_data.expires_in_days:
        expires_at = datetime.utcnow() + timedelta(days=key_data.expires_in_days)
    
    API_KEYS_DB[key_id] = {
        "id": key_id,
        "user_id": current_user_id,
        "key": hashed_key,
        "name": key_data.name,
        "description": key_data.description,
        "scopes": key_data.scopes,
        "is_active": True,
        "rate_limit": 1000,
        "last_used": None,
        "ip_whitelist": key_data.ip_whitelist,
        "created_at": datetime.utcnow(),
        "expires_at": expires_at
    }
    
    response = APIKeyResponse(**API_KEYS_DB[key_id])
    response.key = raw_key  # Only return raw key on creation
    return response


@router.get("/api-keys", response_model=List[APIKeyResponse])
async def list_api_keys(current_user_id: str = Depends(get_current_user)) -> List[APIKeyResponse]:
    """List all API keys for current user"""
    
    user_keys = [
        key for key in API_KEYS_DB.values()
        if key["user_id"] == current_user_id
    ]
    
    return [APIKeyResponse(**key) for key in user_keys]


@router.get("/api-keys/{key_id}", response_model=APIKeyResponse)
async def get_api_key(
    key_id: str,
    current_user_id: str = Depends(get_current_user)
) -> APIKeyResponse:
    """Get specific API key (hashed, for security)"""
    
    if key_id not in API_KEYS_DB:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    
    key = API_KEYS_DB[key_id]
    if key["user_id"] != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this key"
        )
    
    return APIKeyResponse(**key)


@router.put("/api-keys/{key_id}", response_model=APIKeyResponse)
async def update_api_key(
    key_id: str,
    key_update: APIKeyUpdate,
    current_user_id: str = Depends(get_current_user)
) -> APIKeyResponse:
    """Update API key settings"""
    
    if key_id not in API_KEYS_DB:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    
    key = API_KEYS_DB[key_id]
    if key["user_id"] != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this key"
        )
    
    update_data = key_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            key[field] = value
    
    return APIKeyResponse(**key)


@router.delete("/api-keys/{key_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_api_key(
    key_id: str,
    current_user_id: str = Depends(get_current_user)
):
    """Delete an API key"""
    
    if key_id not in API_KEYS_DB:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    
    key = API_KEYS_DB[key_id]
    if key["user_id"] != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this key"
        )
    
    del API_KEYS_DB[key_id]
    return None


# ==================== Workspaces ====================

@router.post("/workspaces", response_model=WorkspaceResponse, status_code=status.HTTP_201_CREATED)
async def create_workspace(
    workspace_data: WorkspaceCreate,
    current_user_id: str = Depends(get_current_user)
) -> WorkspaceResponse:
    """Create a new workspace"""
    
    workspace_id = str(uuid.uuid4())
    slug = workspace_data.name.lower().replace(" ", "-") + f"-{workspace_id[:8]}"
    
    WORKSPACES_DB[workspace_id] = {
        "id": workspace_id,
        "owner_id": current_user_id,
        "name": workspace_data.name,
        "description": workspace_data.description,
        "slug": slug,
        "logo_url": None,
        "color_scheme": "indigo",
        "is_private": workspace_data.is_private,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "members": [current_user_id]
    }
    
    return WorkspaceResponse(**WORKSPACES_DB[workspace_id])


@router.get("/workspaces", response_model=List[WorkspaceResponse])
async def list_workspaces(
    current_user_id: str = Depends(get_current_user)
) -> List[WorkspaceResponse]:
    """List all workspaces for current user"""
    
    user_workspaces = [
        ws for ws in WORKSPACES_DB.values()
        if ws["owner_id"] == current_user_id or current_user_id in ws.get("members", [])
    ]
    
    return [WorkspaceResponse(**ws) for ws in user_workspaces]


@router.get("/workspaces/{workspace_id}", response_model=WorkspaceResponse)
async def get_workspace(
    workspace_id: str,
    current_user_id: str = Depends(get_current_user)
) -> WorkspaceResponse:
    """Get workspace details"""
    
    if workspace_id not in WORKSPACES_DB:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found"
        )
    
    workspace = WORKSPACES_DB[workspace_id]
    
    # Check access
    is_owner = workspace["owner_id"] == current_user_id
    is_member = current_user_id in workspace.get("members", [])
    
    if not is_owner and not is_member:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this workspace"
        )
    
    return WorkspaceResponse(**workspace)


@router.put("/workspaces/{workspace_id}", response_model=WorkspaceResponse)
async def update_workspace(
    workspace_id: str,
    workspace_update: WorkspaceCreate,
    current_user_id: str = Depends(get_current_user)
) -> WorkspaceResponse:
    """Update workspace"""
    
    if workspace_id not in WORKSPACES_DB:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Workspace not found"
        )
    
    workspace = WORKSPACES_DB[workspace_id]
    
    if workspace["owner_id"] != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only workspace owner can update"
        )
    
    workspace["name"] = workspace_update.name
    workspace["description"] = workspace_update.description
    workspace["is_private"] = workspace_update.is_private
    workspace["updated_at"] = datetime.utcnow()
    
    return WorkspaceResponse(**workspace)


# ==================== Experiment Templates ====================

@router.post("/templates", response_model=ExperimentTemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_template(
    template_data: ExperimentTemplateCreate,
    current_user_id: str = Depends(get_current_user)
) -> ExperimentTemplateResponse:
    """Create experiment template"""
    
    template_id = str(uuid.uuid4())
    
    TEMPLATES_DB[template_id] = {
        "id": template_id,
        "creator_id": current_user_id,
        "name": template_data.name,
        "description": template_data.description,
        "category": template_data.category,
        "default_approach": template_data.default_approach,
        "analysis_steps": template_data.analysis_steps,
        "recommended_techniques": template_data.recommended_techniques,
        "is_public": template_data.is_public,
        "usage_count": 0,
        "rating": 0.0,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    return ExperimentTemplateResponse(**TEMPLATES_DB[template_id])


@router.get("/templates", response_model=List[ExperimentTemplateResponse])
async def list_templates(
    category: Optional[str] = None,
    current_user_id: str = Depends(get_current_user)
) -> List[ExperimentTemplateResponse]:
    """List experiment templates (public + user's own)"""
    
    templates = [
        t for t in TEMPLATES_DB.values()
        if t["is_public"] or t["creator_id"] == current_user_id
    ]
    
    if category:
        templates = [t for t in templates if t["category"] == category]
    
    return [ExperimentTemplateResponse(**t) for t in templates]


@router.get("/templates/{template_id}", response_model=ExperimentTemplateResponse)
async def get_template(
    template_id: str,
    current_user_id: str = Depends(get_current_user)
) -> ExperimentTemplateResponse:
    """Get template details"""
    
    if template_id not in TEMPLATES_DB:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Template not found"
        )
    
    template = TEMPLATES_DB[template_id]
    
    if not template["is_public"] and template["creator_id"] != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this template"
        )
    
    return ExperimentTemplateResponse(**template)


# ==================== Notifications ====================

@router.get("/notifications", response_model=List[NotificationResponse])
async def list_notifications(
    unread_only: bool = False,
    current_user_id: str = Depends(get_current_user)
) -> List[NotificationResponse]:
    """List user notifications"""
    
    notifications = [
        n for n in NOTIFICATIONS_DB.values()
        if n["user_id"] == current_user_id
    ]
    
    if unread_only:
        notifications = [n for n in notifications if not n["is_read"]]
    
    # Sort by creation date (newest first)
    notifications.sort(key=lambda x: x["created_at"], reverse=True)
    
    return [NotificationResponse(**n) for n in notifications]


@router.put("/notifications/{notification_id}/read", response_model=NotificationResponse)
async def mark_notification_read(
    notification_id: str,
    current_user_id: str = Depends(get_current_user)
) -> NotificationResponse:
    """Mark notification as read"""
    
    if notification_id not in NOTIFICATIONS_DB:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    notification = NOTIFICATIONS_DB[notification_id]
    
    if notification["user_id"] != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    notification["is_read"] = True
    notification["read_at"] = datetime.utcnow()
    
    return NotificationResponse(**notification)


@router.put("/notifications/mark-all-read")
async def mark_all_notifications_read(
    current_user_id: str = Depends(get_current_user)
):
    """Mark all notifications as read"""
    
    for notification in NOTIFICATIONS_DB.values():
        if notification["user_id"] == current_user_id:
            notification["is_read"] = True
            notification["read_at"] = datetime.utcnow()
    
    return {"message": "All notifications marked as read"}


@router.delete("/notifications/{notification_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_notification(
    notification_id: str,
    current_user_id: str = Depends(get_current_user)
):
    """Delete notification"""
    
    if notification_id not in NOTIFICATIONS_DB:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )
    
    notification = NOTIFICATIONS_DB[notification_id]
    
    if notification["user_id"] != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )
    
    del NOTIFICATIONS_DB[notification_id]
    return None
