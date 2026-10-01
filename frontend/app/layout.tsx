import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "FastFood POS",
  description: "Multi-location fast-food POS dashboard",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
