import './globals.css'
import { Inter } from 'next/font/google'
import { ThemeProvider } from '@mui/material/styles';
import { CssBaseline } from '@mui/material';

import ThemeDark from  "./styles/themeDark"
import Menu from "./components/menu"

const inter = Inter({ subsets: ['latin'] })

export const metadata = {
  title: 'Astro Info',
  description: 'Realtime info for astronomical observation, provided by HKNEAC',
}

export default function RootLayout({ children }) {
  return (
    <ThemeProvider theme={ThemeDark}>
      
      <html lang="en">
        
        <body className={inter.className}>
          <Menu />
          {children}
          </body>
      </html>
    </ThemeProvider>
  )
}
