# Multi-stage build for LLM Council
# Stage 1: Build frontend
FROM node:20-alpine AS frontend-builder

WORKDIR /app/frontend

# Copy frontend package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci

# Copy frontend source
COPY frontend/ ./

# Build frontend
RUN npm run build

# Stage 2: Build backend
FROM python:3.11-slim AS backend

WORKDIR /app

# Install uv for faster dependency installation
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Copy Python dependency files
COPY pyproject.toml uv.lock ./

# Install Python dependencies
RUN uv sync --frozen --no-dev

# Copy backend source
COPY backend/ ./backend/
COPY main.py ./

# Copy built frontend from previous stage
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Create data directory
RUN mkdir -p data/conversations

# Expose port (Railway will set PORT env variable)
EXPOSE 8001

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8001

# Run the application
CMD ["uv", "run", "python", "-m", "backend.main"]
