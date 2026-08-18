"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { GoogleLogin } from "@react-oauth/google";

import { useAuth } from "@/providers/AuthProvider";

export default function LoginForm() {
  const router = useRouter();
  const { loginWithGoogle } = useAuth();

  const [errorMessage, setErrorMessage] = useState<string | null>(
    null,
  );
  const [isSigningIn, setIsSigningIn] = useState(false);

  const handleGoogleSuccess = async (credentialResponse: {
    credential?: string;
  }) => {
    const idToken = credentialResponse.credential;

    if (idToken) {
      try {
        const tokenParts = idToken.split(".");
        const encodedPayload = tokenParts[1];

        if (!encodedPayload) {
          throw new Error("Google ID token payload is missing.");
        }

        const payload = JSON.parse(
          atob(
            encodedPayload
              .replace(/-/g, "+")
              .replace(/_/g, "/"),
          ),
        );

        console.log("===== GOOGLE ID TOKEN CLAIM AUDIT =====");
        console.log("EMAIL:", payload.email);
        console.log("NAME:", payload.name);
        console.log("PICTURE:", payload.picture);
      } catch {
        console.warn("Could not decode Google ID token payload.");
      }
    }

    if (!idToken) {
      setErrorMessage(
        "Google did not return a valid identity token.",
      );
      return;
    }

    setErrorMessage(null);
    setIsSigningIn(true);

    try {
      await loginWithGoogle(idToken);
      router.replace("/");
    } catch {
      setErrorMessage(
        "Google sign-in failed. Please try again.",
      );
    } finally {
      setIsSigningIn(false);
    }
  };

  return (
    <section
      aria-label="HeritageAI Google sign in"
      className="mx-auto w-full max-w-md rounded-3xl border border-white/10 bg-white/[0.04] p-8 shadow-2xl backdrop-blur-xl"
    >
      <div className="mb-8 text-center">
        <p className="mb-3 text-xs font-semibold uppercase tracking-[0.3em] text-amber-300/80">
          HERITAGEAI
        </p>

        <h2 className="text-3xl font-semibold tracking-tight text-white">
          Welcome back
        </h2>

        <p className="mt-3 text-sm leading-6 text-white/60">
          Sign in securely with your Google account.
        </p>
      </div>

      <div className="flex justify-center">
        <div className="relative min-h-11">
          {isSigningIn ? (
            <div className="flex h-11 items-center justify-center rounded-full border border-white/10 bg-white/[0.06] px-6 text-sm text-white/70">
              Signing in...
            </div>
          ) : (
            <GoogleLogin
              onSuccess={handleGoogleSuccess}
              onError={() => {
                setErrorMessage(
                  "Google sign-in was cancelled or failed.",
                );
              }}
              useOneTap={false}
              theme="outline"
              size="large"
              text="signin_with"
              shape="pill"
            />
          )}
        </div>
      </div>

      {errorMessage ? (
        <p
          role="alert"
          className="mt-5 text-center text-sm text-red-300"
        >
          {errorMessage}
        </p>
      ) : null}

      <p className="mt-8 text-center text-xs leading-5 text-white/40">
        By continuing, you use Google to authenticate your
        HeritageAI account.
      </p>
    </section>
  );
}
