import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ESBot",
  description: "Your AI learning assistant",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
