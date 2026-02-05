# FashNet - Multimodal RAG Ecommerce System (Rebuild)

A modern, containerized reconstruction of the FashNet system, featuring AI-powered Fashion Styling, Product Retrieval (RAG), Trends Analysis, and Virtual Try-On.

## Features

-   **AI Stylist Chat**: Chat with an intelligent agent powered by Google Gemini Pro.
-   **RAG Product Search**: Get grounded product recommendations from a vector database (Qdrant).
-   **Virtual Try-On**: Visualize clothes on yourself (Demo Mock Mode included).
-   **Trends Dashboard**: Stay updated with the latest fashion trends.
-   **Secure Authentication**: Full Login/Register flow with Bcrypt hashing and JWT.

## Architecture

-   **Frontend**: React, Vite, Tailwind CSS, Shadcn/UI
-   **Backend**: FastAPI, Python 3.11
-   **AI Service**: FastAPI, Google Gemini SDK, Qdrant Client
-   **Databases**: MongoDB (Metadata), Qdrant (Vectors)
-   **Infrastructure**: Docker Compose

## Prerequisites

-   Docker Desktop (Running)
-   Google Cloud API Key (for Gemini)

## Quick Start

1.  **Configure Environment**:
    Open `.env` in this directory and add your keys:
    ```env
    GOOGLE_API_KEY=your_key_here
    # Other keys can be left as default for dev
    ```

2.  **Start Services**:
    ```bash
    docker-compose up -d --build
    ```

3.  **Seed Data** (First Time Only):
    Populate the Qdrant database with mock products:
    ```bash
    docker-compose exec ai-service python seed_data.py
    ```

4.  **Access the App**:
    -   Frontend: [http://localhost:3000](http://localhost:3000)
    -   Backend Docs: [http://localhost:8000/docs](http://localhost:8000/docs)
    -   AI Service Docs: [http://localhost:8001/docs](http://localhost:8001/docs)

## Development workflow

-   **Backend Code**: `apps/backend/src`
-   **AI Logic**: `apps/ai-service/src`
-   **Frontend Code**: `apps/frontend/src`

All services connect via the `fashnet-network` Docker network.
