from typing import Literal
from pydantic import BaseModel

class OrgConfig(BaseModel):
    provider: Literal["github", "gitlab"]
    org_name: str
    target_agent: Literal["claude-code", "cursor", "generic"] = "claude-code"
    default_branch: str = "main"

class DetectedDep(BaseModel):
    name: str
    source: str

class Connection(BaseModel):
    from_project: str
    to_project: str
    type: Literal["http", "grpc", "library", "event"]
    evidence: str

class Enrichment(BaseModel):
    owner: str | None = None
    description: str | None = None
    notes: str | None = None
    slack_channel: str | None = None
    tags: list[str] = []  

class Project(BaseModel):
    name: str
    repo_url: str
    language: str | None = None
    framework: str | None = None
    type: Literal["service", "app", "library", "infrastructure", "unknown"] = "unknown"
    depends_on: list[DetectedDep] = []
    enrichment: Enrichment | None = None