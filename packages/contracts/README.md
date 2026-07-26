# Contracts

JSON-schema definitions for payloads that cross the `website/backend` <->
`ai-engine/service` boundary. Any change to a Pydantic schema shared across
services must update the matching schema here in the same PR (enforced by
`infra/ci/backend-ci.yml` and `infra/ci/ai-engine-ci.yml`).
