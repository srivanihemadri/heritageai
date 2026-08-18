import React from "react";
import LoginForm from "@/components/auth/LoginForm";
import LoginNotice from "@/components/auth/LoginNotice";

export default function LoginPage() {
  return React.createElement(
    "main",
    {
      className:
        "flex min-h-screen items-center justify-center px-4 py-10 sm:px-6",
    },
    React.createElement(
      "div",
      {
        className: "w-full max-w-md",
      },
      React.createElement(LoginNotice),
      React.createElement(LoginForm),
    ),
  );
}
