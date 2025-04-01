import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Business English Flash',
  description: 'Learn business English phrases in just 5-10 minutes a day',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}
