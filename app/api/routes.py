from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.history import HistoryCreate, HistoryResponse, HistoryUpdate
from app.schemas.integration import IntegrationCreate, IntegrationResponse, IntegrationUpdate
from app.schemas.output_format import OutputFormatCreate, OutputFormatResponse, OutputFormatUpdate
from app.schemas.skill import SkillCreate, SkillResponse, SkillUpdate
from app.services.history_service import HistoryService
from app.services.integration_service import IntegrationService
from app.services.output_format_service import OutputFormatService
from app.services.skill_service import SkillService

router = APIRouter()

# ── Integrations ──────────────────────────────────────────────────────────────

integration_router = APIRouter(prefix="/integrations", tags=["integrations"])


@integration_router.get("", response_model=list[IntegrationResponse])
async def list_integrations(db: Session = Depends(get_db)):
    service = IntegrationService(db)
    return service.list_all()


@integration_router.get("/{integration_id}", response_model=IntegrationResponse)
async def get_integration(integration_id: int, db: Session = Depends(get_db)):
    service = IntegrationService(db)
    integration = service.get(integration_id)
    if not integration:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Integration not found")
    return integration


@integration_router.post(
    "", response_model=IntegrationResponse, status_code=status.HTTP_201_CREATED
)
async def create_integration(data: IntegrationCreate, db: Session = Depends(get_db)):
    service = IntegrationService(db)
    return service.create(data)


@integration_router.put("/{integration_id}", response_model=IntegrationResponse)
async def update_integration(
    integration_id: int, data: IntegrationUpdate, db: Session = Depends(get_db)
):
    service = IntegrationService(db)
    integration = service.update(integration_id, data)
    if not integration:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Integration not found")
    return integration


@integration_router.delete("/{integration_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_integration(integration_id: int, db: Session = Depends(get_db)):
    service = IntegrationService(db)
    deleted = service.delete(integration_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Integration not found")


# ── Skills ────────────────────────────────────────────────────────────────────

skill_router = APIRouter(prefix="/skills", tags=["skills"])


@skill_router.get("", response_model=list[SkillResponse])
async def list_skills(db: Session = Depends(get_db)):
    service = SkillService(db)
    return service.list_all()


@skill_router.get("/{skill_id}", response_model=SkillResponse)
async def get_skill(skill_id: str, db: Session = Depends(get_db)):
    service = SkillService(db)
    skill = service.get(skill_id)
    if not skill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found")
    return skill


@skill_router.post("", response_model=SkillResponse, status_code=status.HTTP_201_CREATED)
async def create_skill(data: SkillCreate, db: Session = Depends(get_db)):
    service = SkillService(db)
    return service.create(data)


@skill_router.put("/{skill_id}", response_model=SkillResponse)
async def update_skill(skill_id: str, data: SkillUpdate, db: Session = Depends(get_db)):
    service = SkillService(db)
    skill = service.update(skill_id, data)
    if not skill:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found")
    return skill


@skill_router.delete("/{skill_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_skill(skill_id: str, db: Session = Depends(get_db)):
    service = SkillService(db)
    deleted = service.delete(skill_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found")


# ── Output Formats ────────────────────────────────────────────────────────────

output_format_router = APIRouter(prefix="/output-formats", tags=["output-formats"])


@output_format_router.get("", response_model=list[OutputFormatResponse])
async def list_output_formats(db: Session = Depends(get_db)):
    service = OutputFormatService(db)
    return service.list_all()


@output_format_router.get("/{format_id}", response_model=OutputFormatResponse)
async def get_output_format(format_id: int, db: Session = Depends(get_db)):
    service = OutputFormatService(db)
    fmt = service.get(format_id)
    if not fmt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Output format not found")
    return fmt


@output_format_router.post(
    "", response_model=OutputFormatResponse, status_code=status.HTTP_201_CREATED
)
async def create_output_format(data: OutputFormatCreate, db: Session = Depends(get_db)):
    service = OutputFormatService(db)
    return service.create(data)


@output_format_router.put("/{format_id}", response_model=OutputFormatResponse)
async def update_output_format(
    format_id: int, data: OutputFormatUpdate, db: Session = Depends(get_db)
):
    service = OutputFormatService(db)
    fmt = service.update(format_id, data)
    if not fmt:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Output format not found")
    return fmt


@output_format_router.delete("/{format_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_output_format(format_id: int, db: Session = Depends(get_db)):
    service = OutputFormatService(db)
    deleted = service.delete(format_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Output format not found")


# ── History ───────────────────────────────────────────────────────────────────

history_router = APIRouter(prefix="/history", tags=["history"])


@history_router.get("", response_model=list[HistoryResponse])
async def list_history(db: Session = Depends(get_db)):
    service = HistoryService(db)
    return service.list_all()


@history_router.get("/{history_id}", response_model=HistoryResponse)
async def get_history(history_id: int, db: Session = Depends(get_db)):
    service = HistoryService(db)
    entry = service.get(history_id)
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="History entry not found")
    return entry


@history_router.post("", response_model=HistoryResponse, status_code=status.HTTP_201_CREATED)
async def create_history(data: HistoryCreate, db: Session = Depends(get_db)):
    service = HistoryService(db)
    return service.create(data)


@history_router.put("/{history_id}", response_model=HistoryResponse)
async def update_history(history_id: int, data: HistoryUpdate, db: Session = Depends(get_db)):
    service = HistoryService(db)
    entry = service.update(history_id, data)
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="History entry not found")
    return entry


@history_router.delete("/{history_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_history(history_id: int, db: Session = Depends(get_db)):
    service = HistoryService(db)
    deleted = service.delete(history_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="History entry not found")


router.include_router(integration_router)
router.include_router(skill_router)
router.include_router(output_format_router)
router.include_router(history_router)
