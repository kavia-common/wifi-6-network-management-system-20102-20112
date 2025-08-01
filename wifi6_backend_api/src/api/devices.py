from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
from src.api.users import get_current_user, User

router = APIRouter(
    prefix="/devices",
    tags=["devices"],
)

# Dummy device data for demonstration
class Device(BaseModel):
    id: int = Field(..., description="Device unique identifier")
    name: str = Field(..., description="Device name")
    mac: str = Field(..., description="MAC address")
    ip: Optional[str] = Field(None, description="Device IP address")
    device_status: str = Field(..., description="Device online/offline status")

class DeviceCreate(BaseModel):
    name: str = Field(..., description="Device name")
    mac: str = Field(..., description="MAC address")
    ip: Optional[str] = Field(None, description="Device IP address")

dummy_devices = [
    Device(id=1, name="WiFi6 Router 1", mac="AA:BB:CC:DD:EE:01", ip="192.168.0.2", device_status="online"),
    Device(id=2, name="WiFi6 AP 2", mac="AA:BB:CC:DD:EE:02", ip="192.168.0.3", device_status="offline"),
]

# In-memory devices list for demo (not persistent!)
devices_db = {dev.id: dev for dev in dummy_devices}

# PUBLIC_INTERFACE
@router.get("/", response_model=List[Device], summary="List all WiFi 6 devices")
def list_devices(current_user: User = Depends(get_current_user)):
    """Return a list of all WiFi 6 devices."""
    return list(devices_db.values())

# PUBLIC_INTERFACE
@router.get("/{device_id}", response_model=Device, summary="Get info for a single device")
def get_device(device_id: int, current_user: User = Depends(get_current_user)):
    """Get details for a specific WiFi 6 device by its ID."""
    device = devices_db.get(device_id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")
    return device

# PUBLIC_INTERFACE
@router.post("/", response_model=Device, status_code=201, summary="Add WiFi 6 device")
def add_device(device: DeviceCreate, current_user: User = Depends(get_current_user)):
    """Add a new WiFi 6 device."""
    new_id = max(devices_db.keys(), default=0) + 1
    dev_obj = Device(id=new_id, **device.model_dump(), device_status="online")
    devices_db[new_id] = dev_obj
    return dev_obj

# PUBLIC_INTERFACE
@router.put("/{device_id}", response_model=Device, summary="Update WiFi 6 device")
def update_device(device_id: int, device: DeviceCreate, current_user: User = Depends(get_current_user)):
    """Update device info for an existing WiFi 6 device."""
    if device_id not in devices_db:
        raise HTTPException(status_code=404, detail="Device not found")
    updated_device = Device(id=device_id, **device.model_dump(), device_status=devices_db[device_id].device_status)
    devices_db[device_id] = updated_device
    return updated_device

# PUBLIC_INTERFACE
@router.delete("/{device_id}", status_code=204, summary="Delete WiFi 6 device")
def delete_device(device_id: int, current_user: User = Depends(get_current_user)):
    """Delete a WiFi 6 device."""
    if device_id not in devices_db:
        raise HTTPException(status_code=404, detail="Device not found")
    del devices_db[device_id]
    return None
