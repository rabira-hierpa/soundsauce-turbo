import "./globals.css";
import "@repo/ui/styles";
import type { Metadata } from "next";
import { Inter } from "next/font/google";
const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Create Turborepo",
  description: "Generated by create turbo",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}): JSX.Element {
  return (
    <html lang="en">
      <body className={inter.className}>
        <h1 className="text-3xl text-blue-500">Tailwindcss</h1>
        {children}
      </body>
    </html>
  );
}
