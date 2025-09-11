gcloud artifacts repositories create email-automation-repo --repository-format=docker --location=us-central1 --description="Docker repo for email automation"

gcloud iam workload-identity-pools create github --project=neon-trilogy-468618-h8 --location="global" --display-name="GitHub Actions Pool"

gcloud iam workload-identity-pools providers create-oidc github-provider --project=neon-trilogy-468618-h8 --location="global" --workload-identity-pool="github" --display-name="GitHub Provider" --issuer-uri="https://token.actions.githubusercontent.com" --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository" --attribute-condition="attribute.repository=='sarojgharat/ai-email-processor'"

gcloud iam workload-identity-pools providers describe github-provider --project=neon-trilogy-468618-h8 --location="global" --workload-identity-pool="github" --format="value(name)"