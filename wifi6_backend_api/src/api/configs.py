from fastapi import APIRouter, HTTPException, Depends
from typing import List
from pydantic import BaseModel, Field
from src.api.users import get_current_user, User

router = APIRouter(
    prefix="/configs",
    tags=["configs"],
)

class Config(BaseModel):
    id: int = Field(..., description="Configuration unique identifier")
    device_id: int = Field(..., description="ID of the associated WiFi 6 device")
    ssid: str = Field(..., description="SSID of the WiFi network")
    password: str = Field(..., description="Password for the WiFi network")
    channel: int = Field(..., description="WiFi channel")
    wpa3_enabled: bool = Field(..., description="Is WPA3 enabled?")

class ConfigCreate(BaseModel):
    device_id: int = Field(..., description="ID of the associated device")
    ssid: str = Field(..., description="SSID of the WiFi network")
    password: str = Field(..., description="Password for the WiFi network")
    channel: int = Field(..., description="WiFi channel")
    wpa3_enabled: bool = Field(..., description="Is WPA3 enabled?")

dummy_configs = [
    Config(id=1, device_id=1, ssid="Network-A", password="pwA12345", channel=36, wpa3_enabled=True),
    Config(id=2, device_id=2, ssid="Network-B", password="pwB12345", channel=44, wpa3_enabled=False),
]

configs_db = {conf.id: conf for conf in dummy_configs}

# PUBLIC_INTERFACE
@router.get("/", response_model=List[Config], summary="List all configurations")
def list_configs(current_user: User = Depends(get_current_user)):
    """List all WiFi 6 configuration profiles."""
    return list(configs_db.values())

# PUBLIC_INTERFACE
@router.get("/{config_id}", response_model=Config, summary="Get a configuration by ID")
def get_config(config_id: int, current_user: User = Depends(get_current_user)):
    """Get a specific WiFi 6 configuration profile by ID."""
    conf = configs_db.get(config_id)
    if not conf:
        raise HTTPException(status_code=404, detail="Config not found")
    return conf

# PUBLIC_INTERFACE
@router.get("/device/{device_id}", response_model=List[Config], summary="List all configs for a device")
def get_device_configs(device_id: int, current_user: User = Depends(get_current_user)):
    """List all configs that are associated with a particular device."""
    return [c for c in configs_db.values() if c.device_id == device_id]

# PUBLIC_INTERFACE
@router.post("/", response_model=Config, status_code=201, summary="Create configuration")
def create_config(cfg: ConfigCreate, current_user: User = Depends(get_current_user)):
    """Create a WiFi 6 configuration for a device."""
    new_id = max(configs_db.keys(), default=0) + 1
    conf = Config(id=new_id, **cfg.model_dump())
    configs_db[new_id] = conf
    return conf

# PUBLIC_INTERFACE
@router.put("/{config_id}", response_model=Config, summary="Update configuration")
def update_config(config_id: int, cfg: ConfigCreate, current_user: User = Depends(get_current_user)):
    """Update a WiFi 6 configuration."""
    if config_id not in configs_db:
        raise HTTPException(status_code=404, detail="Config not found")
    conf = Config(id=config_id, **cfg.model_dump())
    configs_db[config_id] = conf
    return conf

# PUBLIC_INTERFACE
@router.delete("/{config_id}", status_code=204, summary="Delete configuration")
def delete_config(config_id: int, current_user: User = Depends(get_current_user)):
    """Delete a WiFi 6 configuration."""
    if config_id not in configs_db:
        raise HTTPException(status_code=404, detail="Config not found")
    del configs_db[config_id]
    return None
