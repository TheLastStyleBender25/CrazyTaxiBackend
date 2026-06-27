# Crazy Taxi Backend

A production-style backend system built with **FastAPI**, inspired by
city taxi simulation games and designed to demonstrate modern backend
engineering practices.

## Tech Stack

-   FastAPI
-   PostgreSQL
-   Redis
-   SQLAlchemy
-   Alembic
-   JWT Authentication
-   Docker
-   AWS EC2
-   Nginx

## Features

### Authentication & Authorization

-   User registration and login
-   JWT access tokens
-   Refresh token rotation
-   Role-based authorization
-   Redis-backed rate limiting

### Taxi Garage System

-   Purchase and manage taxis
-   Owned and available taxi inventory
-   Player progression support

### Ride Pool System

-   Dynamic ride generation
-   Ride expiration handling
-   Reward and fuel calculations
-   Redis caching for frequently accessed data

### Real-Time Features

-   WebSocket support for live ride pool updates
-   Connection manager for player sessions
-   Real-time synchronization

### Infrastructure

-   Dockerized deployment
-   PostgreSQL persistence
-   Redis caching layer
-   AWS EC2 deployment with Nginx reverse proxy

## Architecture

The project follows a layered architecture:

    Routes -> Services -> Repositories -> Database

Key architectural principles: - Separation of concerns - Dependency
injection - Stateless API design - Containerized deployment - Scalable
service structure

## Learning Goals

This project was built to gain hands-on experience with: - Backend
architecture - Authentication systems - Database design - Caching
strategies - Real-time communication - Cloud deployment -
Microservice-ready patterns

## Repository Structure

    app/
    ├── routes/
    ├── services/
    ├── repositories/
    ├── models/
    ├── schemas/
    ├── core/
    ├── websocket/
    └── utils/
