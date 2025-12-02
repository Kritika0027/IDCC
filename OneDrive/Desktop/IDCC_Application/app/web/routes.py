"""
Web UI routes for forms and views.
"""
from fastapi import APIRouter, Request, Depends, Form, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional
from datetime import datetime
from app.core.database import get_db
from app.services.requirement_service import RequirementService
from app.services.document_parser import DocumentParser
from app.services.image_processor import ImageProcessor
from app.schemas.requirement import RequirementCreate, SubRequirementCreate, ChecklistItemCreate
from app.models.requirement import Priority

web_router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@web_router.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    """Home page with list of requirements."""
    requirements = RequirementService.get_all_requirements(db, skip=0, limit=50)
    return templates.TemplateResponse("home.html", {"request": request, "requirements": requirements})


@web_router.get("/requirements/new", response_class=HTMLResponse)
async def new_requirement_form(request: Request):
    """Form to create a new requirement."""
    return templates.TemplateResponse("requirement_form.html", {
        "request": request,
        "requirement": None,
        "priorities": [p.value for p in Priority]
    })


@web_router.post("/requirements/new", response_class=HTMLResponse)
async def create_requirement(
    request: Request,
    project_name: str = Form(...),
    business_owner: str = Form(...),
    business_unit: Optional[str] = Form(None),
    title: str = Form(...),
    description: str = Form(...),
    priority: str = Form(...),
    expected_outcome: Optional[str] = Form(None),
    success_criteria: Optional[str] = Form(None),
    constraints: Optional[str] = Form(None),
    dependencies: Optional[str] = Form(None),
    desired_deadline: Optional[str] = Form(None),
    category: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    """Create a new requirement from form submission."""
    deadline = None
    if desired_deadline:
        try:
            deadline = datetime.fromisoformat(desired_deadline.replace("Z", "+00:00"))
        except:
            pass
    
    requirement_data = RequirementCreate(
        project_name=project_name,
        business_owner=business_owner,
        business_unit=business_unit,
        title=title,
        description=description,
        priority=Priority(priority),
        expected_outcome=expected_outcome,
        success_criteria=success_criteria,
        constraints=constraints,
        dependencies=dependencies,
        desired_deadline=deadline,
        category=category
    )
    
    requirement = RequirementService.create_requirement(db, requirement_data)
    
    # Redirect to requirement detail page
    return RedirectResponse(url=f"/requirements/{requirement.id}", status_code=303)


@web_router.get("/requirements/{requirement_id}", response_class=HTMLResponse)
async def view_requirement(request: Request, requirement_id: int, db: Session = Depends(get_db)):
    """View a requirement detail page."""
    requirement = RequirementService.get_requirement(db, requirement_id)
    if not requirement:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "Requirement not found"
        }, status_code=404)
    
    sub_requirements = RequirementService.get_sub_requirements(db, requirement_id)
    checklist_items = RequirementService.get_checklist_items(db, requirement_id=requirement_id)
    
    return templates.TemplateResponse("requirement_detail.html", {
        "request": request,
        "requirement": requirement,
        "sub_requirements": sub_requirements,
        "checklist_items": checklist_items
    })


@web_router.get("/requirements/{requirement_id}/sub-requirements/new", response_class=HTMLResponse)
async def new_sub_requirement_form(request: Request, requirement_id: int, db: Session = Depends(get_db)):
    """Form to create a new sub-requirement."""
    requirement = RequirementService.get_requirement(db, requirement_id)
    if not requirement:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "Requirement not found"
        }, status_code=404)
    
    return templates.TemplateResponse("sub_requirement_form.html", {
        "request": request,
        "requirement": requirement,
        "priorities": [p.value for p in Priority]
    })


@web_router.post("/requirements/{requirement_id}/sub-requirements/new", response_class=HTMLResponse)
async def create_sub_requirement(
    request: Request,
    requirement_id: int,
    title: str = Form(...),
    description: Optional[str] = Form(None),
    priority: str = Form(...),
    order: int = Form(0),
    db: Session = Depends(get_db)
):
    """Create a new sub-requirement from form."""
    sub_req_data = SubRequirementCreate(
        title=title,
        description=description,
        priority=Priority(priority),
        order=order
    )
    
    result = RequirementService.create_sub_requirement(db, requirement_id, sub_req_data)
    if not result:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "Failed to create sub-requirement"
        }, status_code=400)
    
    return RedirectResponse(url=f"/requirements/{requirement_id}", status_code=303)


@web_router.post("/requirements/{requirement_id}/checklist/new", response_class=HTMLResponse)
async def create_checklist_item(
    request: Request,
    requirement_id: int,
    title: str = Form(...),
    description: Optional[str] = Form(None),
    order: int = Form(0),
    db: Session = Depends(get_db)
):
    """Create a new checklist item."""
    checklist_data = ChecklistItemCreate(
        title=title,
        description=description,
        order=order
    )
    
    result = RequirementService.create_checklist_item(db, requirement_id, checklist_data)
    if not result:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "Failed to create checklist item"
        }, status_code=400)
    
    return RedirectResponse(url=f"/requirements/{requirement_id}", status_code=303)


@web_router.post("/checklist/{checklist_item_id}/toggle", response_class=HTMLResponse)
async def toggle_checklist_item(
    request: Request,
    checklist_item_id: int,
    db: Session = Depends(get_db)
):
    """Toggle checklist item completion status."""
    from app.repositories.requirement_repository import ChecklistItemRepository
    item = ChecklistItemRepository.get(db, checklist_item_id)
    if not item:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "Checklist item not found"
        }, status_code=404)
    
    ChecklistItemRepository.update(db, checklist_item_id, {"is_completed": not item.is_completed})
    
    requirement_id = item.requirement_id or (item.sub_requirement.requirement_id if item.sub_requirement else None)
    if requirement_id:
        return RedirectResponse(url=f"/requirements/{requirement_id}", status_code=303)
    return RedirectResponse(url="/", status_code=303)


@web_router.get("/upload", response_class=HTMLResponse)
async def upload_form(request: Request):
    """Form to upload documents or images."""
    return templates.TemplateResponse("upload_form.html", {"request": request})


@web_router.get("/analytics", response_class=HTMLResponse)
async def analytics_dashboard(request: Request, db: Session = Depends(get_db)):
    """Analytics dashboard."""
    from app.services.analytics_engine import AnalyticsEngine
    stats = AnalyticsEngine.get_summary_stats(db)
    return templates.TemplateResponse("analytics.html", {
        "request": request,
        "stats": stats
    })


