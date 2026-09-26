import type { ExportFormat } from "./types";

export class ApiError extends Error {
  readonly status: number;
  readonly body: unknown;

  constructor(message: string, status: number, body?: unknown) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.body = body;
  }
}

const TOKEN_KEY = "legisim.auth.token";

function configuredBaseUrl(): string {
  return (process.env.NEXT_PUBLIC_API_BASE_URL ?? "").replace(/\/$/, "");
}

function isBrowser(): boolean {
  return typeof window !== "undefined";
}

export function getAuthToken(): string | null {
  return isBrowser() ? window.localStorage.getItem(TOKEN_KEY) : null;
}

export function setAuthToken(token: string): void {
  if (isBrowser()) window.localStorage.setItem(TOKEN_KEY, token);
}

export function clearAuthToken(): void {
  if (isBrowser()) window.localStorage.removeItem(TOKEN_KEY);
}

export function apiUrl(path: string): string {
  if (!path.startsWith("/")) throw new Error(`API path must start with '/': ${path}`);
  return `${configuredBaseUrl()}${path}`;
}

async function readBody(response: Response): Promise<unknown> {
  if (response.status === 204) return undefined;
  const contentType = response.headers.get("content-type") ?? "";
  if (contentType.includes("application/json")) return response.json();
  const text = await response.text();
  return text || undefined;
}

export interface ApiRequestOptions extends Omit<RequestInit, "body" | "headers"> {
  body?: unknown;
  headers?: HeadersInit;
  /** Requests to protected endpoints attach the locally stored bearer token. */
  authenticated?: boolean;
}

/**
 * A small fetch boundary shared by all domain clients.  It does not silently
 * coerce invalid responses; API errors retain both status and server body.
 */
export async function request<T>(path: string, options: ApiRequestOptions = {}): Promise<T> {
  const { body, headers, authenticated = true, ...init } = options;
  const requestHeaders = new Headers(headers);
  const token = authenticated ? getAuthToken() : null;

  if (token) requestHeaders.set("Authorization", `Bearer ${token}`);
  if (body !== undefined && !requestHeaders.has("Content-Type")) {
    requestHeaders.set("Content-Type", "application/json");
  }

  let response: Response;
  try {
    response = await fetch(apiUrl(path), {
      ...init,
      body: body === undefined ? undefined : JSON.stringify(body),
      headers: requestHeaders,
      credentials: "same-origin",
    });
  } catch (error) {
    throw new ApiError(
      error instanceof Error ? error.message : "Unable to reach the LegiSim API",
      0,
    );
  }

  const responseBody = await readBody(response);
  if (!response.ok) {
    const message =
      typeof responseBody === "object" && responseBody !== null && "message" in responseBody
        ? String(responseBody.message)
        : `API request failed (${response.status})`;
    throw new ApiError(message, response.status, responseBody);
  }
  return responseBody as T;
}

export async function download(path: string, format: ExportFormat): Promise<Blob> {
  const token = getAuthToken();
  const headers = new Headers();
  if (token) headers.set("Authorization", `Bearer ${token}`);
  const response = await fetch(apiUrl(path), { headers, credentials: "same-origin" });
  if (!response.ok) {
    const body = await readBody(response);
    throw new ApiError(`Export failed (${response.status})`, response.status, body);
  }
  return response.blob();
}

/**
 * Native EventSource cannot send Authorization headers.  The backend must set
 * an auth cookie for SSE, or an operator can explicitly opt in to a token
 * query parameter for a trusted same-origin deployment.
 */
export function runEventsUrl(runId: string): string {
  const url = new URL(apiUrl(`/api/runs/${encodeURIComponent(runId)}/events`), window.location.origin);
  const token = getAuthToken();
  if (token && process.env.NEXT_PUBLIC_SSE_TOKEN_QUERY === "true") {
    url.searchParams.set("access_token", token);
  }
  return url.toString();
}
