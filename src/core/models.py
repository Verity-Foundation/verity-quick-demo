"""
# models.py
# Models used across multiple services for consistency
"""
from datetime import datetime
from typing import Optional, Dict, Any, List, cast
import inspect
import sys
from pydantic import BaseModel, ConfigDict, Field
from .crypto import hexhash
from .constants import ContentType

current_module = sys.modules[__name__]
__all__ = [
    name for name, obj in inspect.getmembers(current_module)
    if inspect.isclass(obj) and issubclass(obj, BaseModel)
]

# ---------- DID Registry Service Models ----------
class DIDRegistryRegisterRequest(BaseModel):
    """Request to register/update a DID -> IPFS CID mapping"""
    did: str = Field(..., description="Full DID string (e.g., did:verity:demo:election-commission)")
    doc_cid: str = Field(..., description="IPFS CID of the DID Document")
    # Optional signature for demo purposes
    signature: Optional[str] = Field(None, description="Signature of "
    "(did + doc_cid by the DID's admin key")

class DIDRegistryRegisterResponse(BaseModel):
    """Response after registering a DID"""
    status: str = Field(..., description="'success' or 'error'")
    did: str
    doc_cid: str
    timestamp: datetime = Field(default_factory=datetime.now)
    message: Optional[str] = None

class DIDRegistryResolveRequest(BaseModel):
    """Request to resolve a DID to its current IPFS CID"""
    did: str

class DIDRegistryResolveResponse(BaseModel):
    """Response with resolved CID and status"""
    did: str
    doc_cid: Optional[str] = None  # None if not found
    status: str  # 'found', 'not_found', 'revoked'
    last_updated: Optional[datetime] = None

# ---------- IPFS Gateway Service Models ----------
class IPFSStoreRequest(BaseModel):
    """Request to store a DID Document on the mock IPFS"""
    # The entire DID Document as JSON
    document: Dict[str, Any]
    # Optional: specify content type for demo extensibility
    content_type: str = Field(default="application/did+json")

class IPFSStoreResponse(BaseModel):
    """Response with the generated mock CID"""
    cid: str
    size_bytes: int
    stored_at: datetime = Field(default_factory=datetime.now)

class IPFSRetrieveRequest(BaseModel):
    """Request to retrieve a document by CID"""
    cid: str

class IPFSRetrieveResponse(BaseModel):
    """Response with the retrieved document"""
    cid: str
    document: Dict[str, Any]
    retrieved_at: datetime = Field(default_factory=datetime.now)
    exists: bool = True  # False if CID not found

# ---------- DID Resolver Service Models ----------
class DIDResolveRequest(BaseModel):
    """Main request to resolve a DID"""
    did: str
    # Optional flags for demo
    include_proof: bool = Field(default=False, description="Include resolution proof chain")
    cache_override: bool = Field(default=False, description="Ignore cache and " \
    "force fresh resolution")

class DIDResolveResponse(BaseModel):
    """Complete resolution result"""
    did: str
    status: str  # 'resolved', 'not_found', 'invalid_did', 'error'
    did_document: Optional[Dict[str, Any]] = None
    resolution_metadata: Dict[str, Any] = Field(default_factory=dict)
    # Metadata about the resolution process
    resolved_at: datetime = Field(default_factory=datetime.now)
    retrieval_path: List[str] = Field(default_factory=list)  # e.g., ['registry', 'ipfs']
    # If include_proof was True
    proof_chain: Optional[List[Dict[str, Any]]] = None
    error_message: Optional[str] = None

# ---------- DID Document Structure ----------
class VerificationMethod(BaseModel):
    """Simplified verification method for demo"""
    id: str
    type: str = "Ed25519VerificationKey2020"
    controller: str
    public_key_multibase: str

class ServiceEndpoint(BaseModel):
    """Service endpoint in DID Document"""
    id: str
    type: str
    service_endpoint: str

# -------- Demo ------
class DemoDIDDocument(BaseModel):
    """Simplified DID Document structure for the demo"""
    # Core DID Document fields
    id: str
    verification_method: List[VerificationMethod] = Field(default_factory=list)
    authentication: List[str] = Field(default_factory=list)
    service: List[ServiceEndpoint] = Field(default_factory=list)

    # Demo-specific extensions
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created: datetime = Field(default_factory=datetime.now)
    updated: datetime = Field(default_factory=datetime.now)
    model_config = ConfigDict(
        use_enum_values=True
    )
    proof:Dict[str, Any] = Field(default_factory=dict)

DEMO = DemoDIDDocument(
    id = "did:verity:demo:election-commission",
    verification_method=[VerificationMethod(id="did:verity:demo:election-commission#key-1",
                                            type="Ed25519VerificationKey2020",
                                            controller="did:verity:demo:election-commission",
                                            public_key_multibase="z6MkqYqJ8Z4ZQZ4ZQZ4ZQZ4ZQ"),
                        ],
    authentication=["did:verity:demo:election-commission#key-1"],
    service = [ServiceEndpoint(id="did:verity:demo:election-commission#vcs",
                               type="VerifiableCredentialService",
                               service_endpoint="https://api.demo.verity/credentials"),
                ],
    metadata = {
                "organization": "Demo Election Commission",
                "jurisdiction": "DEMO",
                "tier": "S"
                },
)
"""
class ExampleDID():
    \"""An Example that showcase the format of a DIDDOC\"""
    json_schema_extra = {
        "example": {
            "id": "did:verity:demo:election-commission",
            "verification_method": [
                {
                    "id": "did:verity:demo:election-commission#key-1",
                    "type": "Ed25519VerificationKey2020",
                    "controller": "did:verity:demo:election-commission",
                    "public_key_multibase": "z6MkqYqJ8Z4ZQZ4ZQZ4ZQZ4ZQ"
                }
                ],
                "authentication": ["did:verity:demo:election-commission#key-1"],
                "service": [
                    {
                        "id": "did:verity:demo:election-commission#vcs",
                        "type": "VerifiableCredentialService",
                        "service_endpoint": "https://api.demo.verity/credentials"
                    }
                ],
                "metadata": {
                    "organization": "Demo Election Commission",
                    "jurisdiction": "DEMO",
                    "tier": "S"
                }
            }
        }
        """
# ---------- CLI / Signing Tool Models ----------
class SignedClaim(BaseModel):
    """A signed claim for the demo"""
    claim_id: str
    issuer_did: str
    claim_data: Dict[str, Any]
    signature: str
    signed_at: datetime = Field(default_factory=datetime.now)
    verification_url: Optional[str] = None  # Generated after registration

class DemoSetupRequest(BaseModel):
    """Request to set up a demo organization with a DID"""
    organization_name: str
    jurisdiction: str = "DEMO"
    tier: str = "S"
    # For key generation in demo
    key_algorithm: str = "ed25519"

class DemoSetupResponse(BaseModel):
    """Response with demo setup results"""
    status: str
    organization_name: str
    did: str
    did_document: Dict[str, Any]
    private_key_pem: Optional[str] = None  # For demo signing
    verification_url: str
    steps_completed: List[str]


class VerityClaim(BaseModel):
    """
    Core model representing a verifiable claim issued by an organization.
    This is the object that will be signed and anchored.
    """
    # --- Claim Identity & Metadata ---
    claim_id: str = Field(
        ...,
        description="Unique identifier for this claim (e.g., a UUID or hash)."
    )
    context: List[str] = Field(
        default=["https://verity.foundation/contexts/claim/v1"],
        description="JSON-LD contexts for semantic understanding."
    )
    type: List[str] = Field(
        default=["VerifiableCredential", "VerityClaim"],
        description="The type of this credential."
    )
    issuance_date: datetime = Field(
        default_factory=datetime.now,
        description="When the claim was issued."
    )
    expiration_date: Optional[datetime] = Field(
        None,
        description="Optional date after which the claim is no longer valid."
    )

    # --- Issuer (Who is making the claim) ---
    issuer: Dict[str, str] = Field(
        ...,
        description="The DID of the issuing organization and optional specific key.",
        examples=[{"id": "did:verity:gov:demo-commission", "signed_by": "#master-key-1"}]
    )

    # --- Credential Subject (The actual content being attested) ---
    credential_subject: Dict[str, Any] = Field(
        ...,
        description="The core content/statement of the claim.",
        examples=[{
            "id": "urn:uuid:target-content-123",
            "type": "ElectionResult",
            "title": "2024 Presidential Election - Final Tally",
            "summary": "The final certified results for the 2024 presidential election...",
            "content_url": "https://elections.demo/results.pdf",
            "authority": "National Electoral Commission"
        }]
    )

    # --- Content Integrity & Platform Verification ---
    content_hash: str = Field(
        ...,
        description="Cryptographic hash (e.g., SHA-256) of the original content file.",
        examples=["sha256:a1b2c3..."]
    )
    content_type: ContentType
    platform_hashes: Optional[Dict[str, Dict[str, str]]] = Field(
        None,
        description="Perceptual or format-specific hashes for different platforms.",
        examples=[{
            "twitter": {"perceptual_hash": "phash:1234abc", "format": "jpeg_medium"},
            "facebook": {"perceptual_hash": "phash:5678def", "format": "webp_high"}
        }]
    )

    # --- Proof & Anchoring (To be filled after signing/anchoring) ---
    proof: Optional[Dict[str, Any]] = Field(
        None,
        description="Cryptographic signature and anchoring proof. Added by the system.",
        examples=[{
            "type": "Ed25519Signature2020",
            "created": "2024-01-20T14:30:00Z",
            "verification_method": "did:verity:gov:demo-commission#master-key-1",
            "proof_value": "z4oey5q...",  # The actual signature
            "anchors": [
                {
                    "type": "VerityBatchMerkleAnchor",
                    "batch_id": 427,
                    "merkle_proof": ["0xabc...", "0xdef..."],
                    "transaction_receipt": "0x123..."  # Mock for demo
                }
            ]
        }]
    )

    # --- Verification Metadata (For the demo UI) ---
    verification_url: Optional[str] = Field(
        None,
        description="The direct URL to verify this claim. Generated by the system."
    )
    model_config = ConfigDict(
        use_enum_values=True
    )

    def generate_claim_id(self) -> str:
        """Helper to generate a unique ID based on content and issuer."""
        if isinstance(self.issuance_date, datetime):
            date = cast(datetime, self.issuance_date)
            data = f"{self.issuer['id']}{self.content_hash}{date.isoformat()}"
            return f"claim_{hexhash(data.encode())[:16]}"
        raise ValueError("issuance_date must be set to generate claim_id")
