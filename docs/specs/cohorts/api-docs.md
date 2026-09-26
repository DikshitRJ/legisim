# Cohorts API Documentation

This document describes the API endpoints for managing cohorts, JEV models, and reactions in LegiSim.

## Endpoints

### 1. Get Baseline Personas
**GET** `/api/cohorts/personas`
Retrieves the list of 2000 baseline personas used in the system.
- **Response**: Array of `PersonaSchema` objects.

### 2. Generate Targeting Profile
**POST** `/api/cohorts/jev/targeting-profile`
Uses the Strong LLM to parse a policy and create a Targeting Profile.
- **Request Body**: `PolicyInput`
- **Response**: `TargetingProfile`

### 3. Run JEV Selection
**POST** `/api/cohorts/jev/select`
Runs the JEV cross-encoder inference to score personas against a targeting profile.
- **Request Body**: 
  - `policy_id`: string
  - `targeting_profile`: TargetingProfile object
  - `threshold`: float (default 0.65)
- **Response**: `JEVSelectionResult` containing scores and selected persona IDs.

### 4. Hydrate Prompts
**POST** `/api/cohorts/prompts/hydrate`
Constructs the LLM prompts for the selected personas by injecting local economic context and historical analogues.
- **Request Body**:
  - `persona_ids`: Array of strings
  - `local_context`: Object
  - `memory_summary`: String
- **Response**: Array of `HydratedPrompt` objects.

### 5. Submit Cohort Reactions
**POST** `/api/cohorts/reactions`
Submits the cohort reactions generated during a simulation step.
- **Request Body**: Array of `CohortReaction` objects.
- **Response**: 201 Created.

### 6. Get Cohort Categories
**GET** `/api/cohort-categories`
Returns categories for the simulation wizard.
- **Response**: Array of `CohortCategory` objects.
