const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api/v1";
let csrfTokenFromApi: string | null = null;
let csrfRequest: Promise<string | null> | null = null;

export function getCartToken(): string {
  if (typeof window === "undefined") return "";
  let token = localStorage.getItem("crownluxe_cart_token");
  if (!token) {
    token = crypto.randomUUID();
    localStorage.setItem("crownluxe_cart_token", token);
  }
  return token;
}

function csrfToken(): string | undefined {
  if (typeof document === "undefined") return undefined;
  return document.cookie.split("; ").find((value) => value.startsWith("csrftoken="))?.split("=")[1];
}

/**
 * Works both same-origin and with local development hosts such as
 * localhost:3000 -> 127.0.0.1:8000, where JavaScript cannot read the API
 * host's cookie. Django still validates the matching cookie server-side.
 */
export async function ensureCsrfToken(): Promise<string | null> {
  if (csrfTokenFromApi) return csrfTokenFromApi;
  const fromCookie = csrfToken();
  if (fromCookie) return decodeURIComponent(fromCookie);
  if (!csrfRequest) {
    csrfRequest = fetch(`${API_BASE}/auth/csrf/`, {
      credentials: "include",
      headers: { Accept: "application/json" },
    })
      .then(async (response) => {
        if (!response.ok) return null;
        const payload = await response.json();
        csrfTokenFromApi = payload.csrfToken || null;
        return csrfTokenFromApi;
      })
      .finally(() => { csrfRequest = null; });
  }
  return csrfRequest;
}

export async function fetchApi<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const cartToken = getCartToken();

  const headers: Record<string, string> = {
    Accept: "application/json",
    ...(options.headers as Record<string, string> || {}),
  };

  // A GET has no JSON body. Omitting this non-simple header keeps read-only
  // catalog calls as small as possible; writes still receive it automatically.
  if (options.body && !headers["Content-Type"]) {
    headers["Content-Type"] = "application/json";
  }

  if (cartToken) {
    headers["X-Cart-Token"] = cartToken;
  }

  if (!["GET", "HEAD", "OPTIONS"].includes((options.method || "GET").toUpperCase())) {
    const csrf = await ensureCsrfToken();
    if (csrf) headers["X-CSRFToken"] = csrf;
  }

  const url = endpoint.startsWith("http") ? endpoint : `${API_BASE}${endpoint}`;

  const res = await fetch(url, {
    ...options,
    headers,
    credentials: "include",
  });

  if (!res.ok) {
    let errorData = null;
    try {
      errorData = await res.json();
    } catch {
      errorData = { detail: res.statusText };
    }
    const err = new Error(errorData?.detail || errorData?.message || errorData?.cart || "An error occurred with the request.");
    (err as any).data = errorData;
    (err as any).status = res.status;
    throw err;
  }

  if (res.status === 204) {
    return {} as T;
  }

  return res.json();
}
