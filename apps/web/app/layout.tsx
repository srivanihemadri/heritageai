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
  description: "AI-powered heritage discovery and preservation platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return React.createElement("html", { lang: "en" },
    React.createElement("body", { className: `${geistSans.variable} ${geistMono.variable}` },
      React.createElement(AuthProvider, null, children)
    )
  );
}
