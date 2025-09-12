gcloud artifacts repositories create email-automation-repo --repository-format=docker --location=us-central1 --description="Docker repo for email automation"

gcloud iam workload-identity-pools create github --project=neon-trilogy-468618-h8 --location="global" --display-name="GitHub Actions Pool"

gcloud iam workload-identity-pools providers create-oidc github-provider --project=neon-trilogy-468618-h8 --location="global" --workload-identity-pool="github" --display-name="GitHub Provider" --issuer-uri="https://token.actions.githubusercontent.com" --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository" --attribute-condition="attribute.repository=='sarojgharat/ai-email-processor'"

gcloud iam workload-identity-pools providers describe github-provider --project=neon-trilogy-468618-h8 --location="global" --workload-identity-pool="github" --format="value(name)"

----------------------------------------------------------------------------------------------------------------------


gcloud iam workload-identity-pools create "github-actions-pool" --project="neon-trilogy-468618-h8" --location="global" --display-name="GitHub Actions Pool"

gcloud iam workload-identity-pools providers create-oidc "github-actions-provider" --project="neon-trilogy-468618-h8" --location="global" --workload-identity-pool="github-actions-pool" --display-name="GitHub Actions provider" --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.aud=assertion.aud,attribute.repository=assertion.repository" --issuer-uri="https://token.actions.githubusercontent.com" --attribute-condition="attribute.repository=='sarojgharat/ai-email-processor'"


gcloud iam service-accounts add-iam-policy-binding "github-cicd@neon-trilogy-468618-h8.iam.gserviceaccount.com" --project="neon-trilogy-468618-h8" --role="roles/iam.workloadIdentityUser" --member="principalSet://iam.googleapis.com/projects/1031078077136/locations/global/workloadIdentityPools/github-actions-pool/attribute.repository/sarojgharat/ai-email-processor"


