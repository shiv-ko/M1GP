import "./globals.css";

export const metadata = {
  title: "Jump Game",
  description: "A simple jump game using Next.js App Router",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ja">
      <body>{children}</body>
    </html>
  );
}