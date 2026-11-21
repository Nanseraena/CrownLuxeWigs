"use client";

import { useEffect, useRef, useState } from "react";
import { Loader2 } from "lucide-react";

declare global {
  interface Window {
    google?: { accounts: { id: { initialize: (options: Record<string, unknown>) => void; renderButton: (element: HTMLElement, options: Record<string, unknown>) => void } } };
  }
}

type Props = { onCredential: (credential: string) => Promise<void>; onError: (message: string) => void };

/** Official Google Identity Services button. Only the signed ID token reaches the API. */
export default function GoogleSignInButton({ onCredential, onError }: Props) {
  const target = useRef<HTMLDivElement>(null);
  const [ready, setReady] = useState(false);
  const clientId = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID;

  useEffect(() => {
    if (!clientId || !target.current) return;
    const initialize = () => {
      if (!window.google || !target.current) return;
      window.google.accounts.id.initialize({
        client_id: clientId,
        callback: async ({ credential }: { credential?: string }) => {
          if (!credential) return onError("Google did not return a credential. Please try again.");
          try { await onCredential(credential); } catch (error: any) { onError(error.message || "Google sign-in failed."); }
        },
      });
      target.current.innerHTML = "";
      window.google.accounts.id.renderButton(target.current, { theme: "outline", size: "large", text: "continue_with", width: target.current.clientWidth || 320, shape: "pill" });
      setReady(true);
    };
    const existing = document.querySelector('script[src="https://accounts.google.com/gsi/client"]');
    if (existing) { initialize(); return; }
    const script = document.createElement("script");
    script.src = "https://accounts.google.com/gsi/client";
    script.async = true;
    script.onload = initialize;
    script.onerror = () => onError("Google sign-in could not be loaded. Please use email and password.");
    document.head.appendChild(script);
  }, [clientId, onCredential, onError]);

  if (!clientId) return null;
  return <div className="min-h-10 flex justify-center" aria-label="Continue with Google">{!ready && <Loader2 className="w-4 h-4 animate-spin text-neutral-400" />}<div ref={target} /></div>;
}
