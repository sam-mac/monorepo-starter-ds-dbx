# Terraform (recommended) — Unity Catalog grants + identities

Use IaC to manage:
- Unity Catalog catalogs/schemas/tables grants
- Service principals for prod run-as identities
- Cluster policies (optional)

Why: permissions drift is a common failure mode for DS delivery.

Suggested approach:
- Deploy workflows with a GitHub Actions service principal (deploy identity)
- Run production jobs as a runtime service principal (least privilege)

See the Databricks Terraform provider `grants` resource docs for defining UC privileges.
