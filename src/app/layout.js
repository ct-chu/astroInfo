"use client";

import "./globals.css";
import { useState } from 'react';
import { ThemeProvider } from "@mui/material/styles";
import { CssBaseline } from "@mui/material";
import localFont from "next/font/local";

import themeDark from "./styles/themeDark";
import Menu from "./components/menu";
import { ThemeSwitchContext } from "./components/ThemeSwitchContext";

const NotoSanstc_R = localFont({ src: "./pages/NotoSansTC-Regular.otf" });

export const metadata = {
  title: "可觀天文資訊",
  description: "Realtime info for astronomical observation, provided by HKNEAC",
  manifest: '/manifest.json',
  appleWebApp: {
    title: '可觀天文',
    statusBarStyle: 'black-translucent',
    startupImage: [
      "/cover.jpg",
    ],
  },
};

export default function RootLayout({ children }) {

  const [theme, setTheme] = useState(themeDark);

  return (
    <ThemeSwitchContext.Provider value={[theme, setTheme]}>
    <ThemeProvider theme={theme}>
      <html lang="en">
        <head>
          <link rel="icon" href="/favicon.ico" />
          <link
            rel="apple-touch-icon"
            href="/apple-icon?<generated>"
            type="image/<generated>"
            sizes="<generated>"
          />
        </head>
        <body className={NotoSanstc_R.className}>
          <CssBaseline />
          <Menu />
          <div
            style={{
              display: "flex",
              justifyContent: "center",
            }}
          >
            {children}
          </div>
        </body>
      </html>
    </ThemeProvider>
    </ThemeSwitchContext.Provider>
  );
}
