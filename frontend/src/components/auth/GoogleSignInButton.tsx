"use client";

import { useEffect, useRef, useState } from "react";
import { Loader2 } from "lucide-react";

declare global {
  interface Window {
    google?: { accounts: { id: { initialize: (options: Record<string, unknown>) => void; renderButton: (element: HTMLElement, options: Record<string, unknown>) => void } } };
  }
}

type Props = { onCredential: (credential: string) => Promise<void>; onError: (message: string) => void };

let googleSdkPromise: Promise<void> | null = null;

function loadGoogleSdk(): Promise<void> {
  if (window.google) return Promise.resolve();
  if (!googleSdkPromise) {
    googleSdkPromise = new Promise((resolve, reject) => {
      const existing = document.querySelector<HTMLScriptElement>('script[src="https://accounts.google.com/gsi/client"]');
      const script = existing || document.createElement("script");
      const onLoad = () => resolve();
      const onError = () => reject(new Error("Google sign-in could not be loaded."));
      script.addEventListener("load", onLoad, { once: true });
      script.addEventListener("error", onError, { once: true });
      if (!existing) {
        script.src = "https://accounts.google.com/gsi/client";
        script.async = true;
        document.head.appendChild(script);
      }
    });
  }
  return googleSdkPromise;
}

/** Official Google Identity Services button. Only the signed ID token reaches the API. */
export default function GoogleSignInButton({ onCredential, onError }: Props) {
  const target = useRef<HTMLDivElement>(null);
  const [ready, setReady] = useState(false);
  const clientId = process.env.NEXT_PUBLIC_GOOGLE_CLIENT_ID;

  useEffect(() => {
    if (!clientId || !target.current) return;
    let cancelled = false;
    loadGoogleSdk().then(() => {
      if (cancelled || !window.google || !target.current) return;
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
    }).catch(() => onError("Google sign-in could not be loaded. Please use email and password."));
    return () => { cancelled = true; };
  }, [clientId, onCredential, onError]);

  if (!clientId) return null;
  return <div className="min-h-10 flex justify-center" aria-label="Continue with Google">{!ready && <Loader2 className="w-4 h-4 animate-spin text-neutral-400" />}<div ref={target} /></div>;
}
