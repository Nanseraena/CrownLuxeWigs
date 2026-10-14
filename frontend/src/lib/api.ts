const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api/v1";

export function getCartToken(): string {
  if (typeof window === "undefined") return "";
  let token = localStorage.getItem("crownluxe_cart_token");
  if (!token) {
    token = crypto.randomUUID();
    localStorage.setItem("crownluxe_cart_token", token);
  }
  return token;
}

export function getAuthToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("crownluxe_access_token");
}

export function setAuthTokens(access: string, refresh: string) {
  if (typeof window === "undefined") return;
  localStorage.setItem("crownluxe_access_token", access);
  localStorage.setItem("crownluxe_refresh_token", refresh);
}

export function clearAuthTokens() {
  if (typeof window === "undefined") return;
  localStorage.removeItem("crownluxe_access_token");
  localStorage.removeItem("crownluxe_refresh_token");
}

export async function fetchApi<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const cartToken = getCartToken();
  const authToken = getAuthToken();

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

  if (authToken) {
    headers["Authorization"] = `Bearer ${authToken}`;
  }

  const url = endpoint.startsWith("http") ? endpoint : `${API_BASE}${endpoint}`;

  const res = await fetch(url, {
    ...options,
    headers,
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
