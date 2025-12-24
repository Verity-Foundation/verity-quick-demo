# Verity Protocol: DID Document Specification

1. Overview & Context

The Verity Protocol is designed to combat AI-generated misinformation in democratic processes (e.g., elections) by establishing cryptographic provenance for digital content. At its core is a Decentralized Identifier (DID) system (did:verity) that enables institutions like election commissions to make verifiable claims.

A Verity DID Document is a JSON document that describes an entity (an organization). It is stored on IPFS, and its hash is anchored to a permissioned blockchain (Hyperledger Besu) via a smart contract. This creates an immutable link between a human-readable DID and the cryptographic keys authorized to speak for that entity.

2. DID Document Structure & Field Definitions

The DID Document follows a JSON structure with specific fields. Below is the breakdown of each field and its critical role in the verification ecosystem.

@context (Array of strings)

- Purpose: Defines the data vocabulary. It ensures the document can be processed as Linked Data.
- Verity Role: It declares that the document conforms to the W3C DID Core specification and any Verity-specific extensions.
- Example: ["https://www.w3.org/ns/did/v1", "https://verity.foundation/contexts/v1"]

id (String)

- Purpose: The full DID string that uniquely identifies the subject of the document.
- Verity Role: The primary lookup key. Resolvers use this string to query the smart contract for the corresponding IPFS hash.
- Format: did:verity:<namespace>:<entity-identifier> (e.g., did:verity:gov:ghana-election-commission)
- Namespaces: gov (government), org (corporation/NGO), media (news), edu (education), ind (verified individual).

authentication (Array of strings or objects)

- Purpose: Specifies the verification methods that can be used to authenticate the DID subject (e.g., prove control of the DID).
- Verity Role: Lists the key IDs (like #super-user) that are allowed for general authentication. This is typically where the Super User Key is declared for infrequent, critical operations.

verificationMethod (Array of objects)

- Purpose: Defines all public keys and other verification methods available.
- Verity Role: This array contains the detailed definitions of all keys, especially the Master Keys used for governance and daily signing.
- Key Object Fields:
  - id: A fragment identifier (e.g., #master-1).
  - type: The cryptographic suite (e.g., Ed25519VerificationKey2020).
  - controller: The DID that controls this key (e.g., the organization's own DID).
  - publicKeyMultibase: The encoded public key material.
  - keyUsage: Verity Extension. Indicates the key's role: super-user, master-key, or delegated-key.(Not yet)
  - keyStatus: Tracks if the key is active, revoked, or suspended.(Not yet)

service (Array of objects)

- Purpose: Defines service endpoints for interacting with the DID subject.
- Verity Role: Points verifiers to where they can find signed claims (VerityClaimsEndpoint) or check revocation lists (RevocationList2023).
- Example Endpoint:
  ```json
  {
    "id": "#verity-claims",
    "type": "VerityClaimsEndpoint",
    "serviceEndpoint": "https://api.verity.foundation/claims/election-commission"
  }
  ```

metadata (Object)

- Purpose: A container for Verity-specific organizational details and status.
- Verity Role: Provides context for verifiers and drives the tiered verification model.
- Key Sub-fields:
  - organizationName: Human-readable name.
  - jurisdiction: Legal jurisdiction (e.g., "GH").
  - tier: Core Verification Field. Can be "S" (Cryptographic), "1" (Platform-Verified), or "2" (Evidence-Based). Only Tier S entities use this full DID document specification.
  - verifiedAt: Timestamp of foundation verification.
  - masterKeyThreshold: The "M" in the M-of-N threshold required for Master Key governance actions (e.g., 3).

3. The Three-Tier Key Hierarchy (Super, Master, Slave)

This system, managed partly on-chain and reflected in the DIDDoc, is designed for real-world organizational security.

- Super User Key
  - Defined In: authentication array.
  - Purpose: The "root of trust." Used exclusively for the most critical operation: updating the DID Document itself (e.g., changing the list of Master Keys). It is kept offline and used 1-3 times per year.
- Master Keys
  - Defined In: verificationMethod array
  - Purpose: Form the organization's governance layer. They can:
    1. Sign Claims: Authorize official content (most frequent use).
    2. Delegate Authority: Create Slave Keys via smart contract.
    3. Initiate Recovery: Start the timelocked process to recover a lost Super User key (requires meeting the masterKeyThreshold).
- Slave Keys (Delegated Keys)
  - Origin: Created dynamically via on-chain delegation by a Master Key. They are not listed in the static DID Document.
  - Purpose: Operational keys for daily use by employees or systems. They can sign claims on behalf of the organization but have permissions (like expiry, depth limits) set by the delegating Master Key. They can be revoked instantly on-chain without touching the DIDDoc.

4. Verification Process Flow

Verification is a multi-step process that checks the content, the signature, the issuer's identity, and the issuer's authority.

1. Content & Claim Discovery: A verifier encounters a piece of content (e.g., an image of an election result) with an associated Verity Claim containing a signature and the issuer's DID.
2. DID Resolution:
   - The resolver extracts the issuer's DID (e.g., did:verity:gov:ghana-election-commission).
   - It calls the DIDRegistry smart contract to resolve the DID to the latest IPFS Content Identifier (CID) hash of the DID Document.
   - It fetches the DID Document JSON from IPFS using the CID.
3. Signature & Authority Verification:
   - The verifier checks that the signature on the claim validly corresponds to a public key listed in the DID Document's verificationMethod array.
   - It checks the keyUsage and keyStatus of that key to ensure it is a currently active master-key or delegated-key authorized for signing.
   - For Slave Keys, it also checks the on-chain delegation record for validity and expiration.
4. Trust Assessment (Tier Evaluation):
   - The verifier examines the metadata.tier field.
   - Tier S (Cryptographic): Full trust is established through the cryptographic checks above. The content is displayed with the highest verification badge.
   - Tier 1/2: The verifier falls back to platform verification or forensic analysis, as the DID is not foundation-verified.

5. Example DID Document Snippet

```json
{
  "@context": [
    "https://www.w3.org/ns/did/v1",
    "https://verity.foundation/contexts/v1"
  ],
  "id": "did:verity:gov:demo-commission",
  "authentication": ["#super-user-2025"],
  "verificationMethod": [
    {
      "id": "#super-user-2025",
      "type": "Ed25519VerificationKey2020",
      "controller": "did:verity:gov:demo-commission",
      "publicKeyMultibase": "z6Mkq...",
    },
    {
      "id": "#master-key-1",
      "type": "Ed25519VerificationKey2020",
      "controller": "did:verity:gov:demo-commission",
      "publicKeyMultibase": "z6Mkm...",
    }
  ],
  "service": [...],
  "metadata": {
    "organizationName": "Demo Election Commission",
    "tier": "S",
    "masterKeyThreshold": 2,
    "verifiedAt": "2025-12-01T00:00:00Z"
  }
}
```