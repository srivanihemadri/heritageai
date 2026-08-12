import React from "react";
import LoginForm from "@/components/auth/LoginForm";

export default function LoginPage() {
  return React.createElement(
    "main",
    null,
    React.createElement("h1", null, "Sign in to HeritageAI"),
    React.createElement(LoginForm),
  );
}
