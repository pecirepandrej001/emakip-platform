$ErrorActionPreference = "Stop"
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Created .env from .env.example"
}
docker compose -f docker/docker-compose.yml up --build -d
Write-Host ""
Write-Host "EMAKIP is starting:"
Write-Host "UI:      http://localhost:8501"
Write-Host "API:     http://localhost:8000/docs"
Write-Host "MLflow:  http://localhost:5000"
Write-Host "Qdrant:  http://localhost:6333/dashboard"
Write-Host ""
Write-Host "Seed demo user with:"
Write-Host "docker compose -f docker/docker-compose.yml exec api python scripts/seed_database.py"
