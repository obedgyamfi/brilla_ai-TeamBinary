import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import TopNavbar from "@/components/ui/custom/TopNavbar";
import BottomDock from "../components/ui/custom/BottomDock";
import { QuizProvider } from "@/components/QuizContext";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "NSMQ AI",
  description: "NSMQ AI app by Team Binary",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <QuizProvider>
          <TopNavbar />
          {children}
          <BottomDock />
        </QuizProvider>
      </body>
    </html>
  );
}
