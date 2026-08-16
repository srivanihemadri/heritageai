import React from "react";
import type { Metadata } from "next";
import localFont from "next/font/local";
import "./globals.css";
import { AuthProvider } from "@/providers/AuthProvider";

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
});

const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
});

export const metadata: Metadata = {
  title: "HeritageAI",
  description:
    "AI-powered heritage discovery, understanding and preservation platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return React.createElement(
    "html",
    { lang: "en" },
    React.createElement(
      "body",
      {
        className: `${geistSans.variable} ${geistMono.variable} overflow-x-hidden`,
      },
      React.createElement(
        "div",
        {
          className:
            "pointer-events-none fixed inset-0 -z-10 overflow-hidden",
          "aria-hidden": "true",
        },
        React.createElement("div", {
          className:
            "absolute -left-40 top-[-12rem] h-[32rem] w-[32rem] rounded-full bg-[rgba(212,175,90,0.035)] blur-[100px]",
        }),
        React.createElement("div", {
          className:
            "absolute -right-40 top-[30%] h-[28rem] w-[28rem] rounded-full bg-[rgba(155,117,48,0.025)] blur-[100px]",
        }),
      ),
      React.createElement(
        AuthProvider,
        null,
        children,
      ),
    ),
  );
}
