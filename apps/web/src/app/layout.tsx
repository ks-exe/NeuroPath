import type { Metadata } from "next";
import type { ReactNode } from "react";
import { bodyFont, headingFont, monoFont } from "./fonts";
import "./globals.css";

export const metadata: Metadata = {
  title: "NEUROPATH",
  description: "Technology. Engineered to Solve.",
};

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en" className={`${headingFont.variable} ${bodyFont.variable} ${monoFont.variable}`}>
      <body>{children}</body>
    </html>
  );
}
