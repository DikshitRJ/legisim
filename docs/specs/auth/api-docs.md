# API Documentation: Authentication

This document provides a plain English explanation of the authentication endpoints, their purpose, and request flow.

## Overview
The authentication API handles officer login, session validation, and logout. It ensures that only authorized officers can access the LegiSim platform and interact with simulations.

## Endpoints

### 1. Login
- **Endpoint:** `POST /api/auth/login`
- **Purpose:** Authenticates an officer using their ID (email or username) and password.
- **Request Flow:**
  1. Client sends `officerId` and `password`.
  2. Server verifies credentials against the database.
  3. On success, creates a session and returns an authentication token along with the officer's profile data (`id`, `name`, `role`).
  4. On failure, returns a `401 Unauthorized` error.

### 2. Logout
- **Endpoint:** `POST /api/auth/logout`
- **Purpose:** Terminates the current active session.
- **Request Flow:**
  1. Client calls the endpoint with their current authentication token (in headers).
  2. Server invalidates the session in the database/cache.
  3. Returns a success confirmation `{ success: true }`.

### 3. Get Current User (Me)
- **Endpoint:** `GET /api/auth/me`
- **Purpose:** Retrieves the profile of the currently authenticated officer. Used on page reloads to restore the user session state on the frontend.
- **Request Flow:**
  1. Client calls the endpoint with their authentication token.
  2. Server validates the token.
  3. Returns the officer's profile (`id`, `name`, `role`).
  4. If the token is invalid or expired, returns `401 Unauthorized`.
