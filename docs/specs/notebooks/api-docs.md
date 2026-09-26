# Notebooks API Documentation

This document provides plain English documentation of the API endpoints for the **Notebooks** domain, detailing the request flow and usage.

## Overview

The Notebooks API allows users to manage notebooks and their statuses. Notebooks serve as the primary container for simulation configurations and runs.

## Endpoints

### 1. List Notebooks
**GET `/api/notebooks`**

Retrieves a list of notebooks, optionally filtered by their status.

- **Query Parameters**: 
  - `status` (optional): Filter notebooks by status. Allowed values: `active`, `archived`.
- **Response**: Returns a list of `Notebook` objects.
- **Usage**: Used to populate the main dashboard or list views where users select a notebook to work on.

### 2. Create Notebook
**POST `/api/notebooks`**

Creates a new notebook.

- **Request Body**:
  - `title` (string): The title of the notebook.
  - `description` (string): A detailed description of the notebook.
- **Response**: Returns the newly created `Notebook` object.
- **Usage**: Called when a user clicks "New Notebook" and submits the initial details.

### 3. Get Single Notebook
**GET `/api/notebooks/:id`**

Retrieves the details of a specific notebook by its ID.

- **Path Parameters**:
  - `id`: The unique identifier of the notebook.
- **Response**: Returns the `Notebook` object.
- **Usage**: Used to fetch full notebook details when a user opens a specific notebook.

### 4. Update Notebook
**PUT `/api/notebooks/:id`**

Updates the details of an existing notebook.

- **Path Parameters**:
  - `id`: The unique identifier of the notebook.
- **Request Body**:
  - `title` (string, optional): The new title.
  - `description` (string, optional): The new description.
- **Response**: Returns the updated `Notebook` object.
- **Usage**: Called when a user edits the notebook settings.

### 5. Archive Notebook
**DELETE `/api/notebooks/:id`**

Archives a notebook, changing its status to `archived`. (Note: This does not necessarily delete the notebook permanently, but hides it from active views).

- **Path Parameters**:
  - `id`: The unique identifier of the notebook.
- **Response**: Returns a success confirmation `{ success: boolean }`.
- **Usage**: Called when a user decides they no longer need a notebook active in their workspace.

## Request Flow

1. **Initialization**: A user queries `GET /api/notebooks` to see all active projects.
2. **Creation**: If starting fresh, the user submits `POST /api/notebooks` with basic details.
3. **Interaction**: The user works within the notebook, potentially updating its details via `PUT /api/notebooks/:id`.
4. **Conclusion**: Once the project is complete, the user issues a `DELETE /api/notebooks/:id` to archive it.
