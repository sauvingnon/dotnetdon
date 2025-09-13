from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field
from enum import StrEnum

class UserActiveInboundsDto(BaseModel):
    uuid: UUID
    tag: str
    type: str
    network: Optional[str] = None
    security: Optional[str] = None

class ActiveInternalSquadDto(BaseModel):
    uuid: UUID
    name: str

class UserLastConnectedNodeDto(BaseModel):
    connected_at: datetime = Field(alias="connectedAt")
    node_name: str = Field(alias="nodeName")

class HappCrypto(BaseModel):
    cryptoLink: str

class UserStatus(StrEnum):
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"
    LIMITED = "LIMITED"
    EXPIRED = "EXPIRED"


class TrafficLimitStrategy(StrEnum):
    NO_RESET = "NO_RESET"
    DAY = "DAY"
    WEEK = "WEEK"
    MONTH = "MONTH"

class UserResponseDto(BaseModel):
    uuid: UUID
    subscription_uuid: Optional[UUID] = Field(None, alias="subscriptionUuid")
    short_uuid: str = Field(alias="shortUuid")
    username: str
    status: Optional[UserStatus] = None
    used_traffic_bytes: float = Field(alias="usedTrafficBytes")
    lifetime_used_traffic_bytes: float = Field(alias="lifetimeUsedTrafficBytes")
    traffic_limit_bytes: Optional[int] = Field(None, alias="trafficLimitBytes")
    traffic_limit_strategy: Optional[str] = Field(None, alias="trafficLimitStrategy")
    sub_last_user_agent: Optional[str] = Field(None, alias="subLastUserAgent")
    sub_last_opened_at: Optional[datetime] = Field(None, alias="subLastOpenedAt")
    expire_at: Optional[datetime] = Field(None, alias="expireAt")
    online_at: Optional[datetime] = Field(None, alias="onlineAt")
    sub_revoked_at: Optional[datetime] = Field(None, alias="subRevokedAt")
    last_traffic_reset_at: Optional[datetime] = Field(None, alias="lastTrafficResetAt")
    trojan_password: str = Field(alias="trojanPassword")
    vless_uuid: UUID = Field(alias="vlessUuid")
    ss_password: str = Field(alias="ssPassword")
    description: Optional[str] = None
    telegram_id: Optional[int] = Field(None, alias="telegramId")
    email: Optional[str] = None
    hwidDeviceLimit: Optional[int] = Field(None, alias="hwidDeviceLimit", ge=0)
    active_user_inbounds: Optional[List[UserActiveInboundsDto]] = Field(
        None, alias="activeUserInbounds"
    )
    active_internal_squads: Optional[List["ActiveInternalSquadDto"]] = Field(
        None, alias="activeInternalSquads"
    )
    subscription_url: str = Field(alias="subscriptionUrl")
    first_connected: Optional[datetime] = Field(None, alias="firstConnectedAt")
    last_trigger_threshold: Optional[int] = Field(None, alias="lastTriggeredThreshold")
    last_connected_node: Optional[UserLastConnectedNodeDto] = Field(
        None, alias="lastConnectedNode"
    )
    happ: Optional[HappCrypto] = Field(None, alias="happ")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True