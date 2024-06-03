import "./globals.css";
import { CssBaseline } from "@mui/material";
import localFont from "next/font/local";

import Menu from "./components/menu";
import LayoutComponent from "./components/layoutComponent";
import Script from 'next/script'
import { prefix } from './prefix.js';

const prefixString = `${prefix}`

export const metadata = {
  title: "可觀天文助理",
  description: "Realtime info for astronomical observation, provided by HKNEAC",
  manifest: `${prefix}/manifest.json`,
  appleWebApp: {
    title: "可觀天文助理",
    statusBarStyle: "black-translucent",
    startupImage: [`${prefix}/icons/cover.jpg`],
  },
  viewport: {
    width: "device-width",
    initalScale: 1,
    maximumScale: 1,
    userScalable: "no",
  },
};

export default function RootLayout({ children }) {
  return (
    <LayoutComponent>
      <html lang="en">
        <head>        
          <div className="container">
            <Script src="https://www.googletagmanager.com/gtag/js?id=G-93TZWJBQCF" />
            <Script id="google-analytics">
              {`
                window.dataLayer = window.dataLayer || [];
                function gtag(){dataLayer.push(arguments);}
                gtag('js', new Date());
      
                gtag('config', 'G-93TZWJBQCF');
              `}
            </Script>
          </div>
          <link rel="icon" href={`${prefix}/icons/favicon.ico`} sizes="any"/>
          <link
            rel="apple-touch-icon"
            href={`${prefix}/icons/apple-icon.png`}
            type="image"
            sizes="any"
          />
          <link
            rel="icon"
            href={`${prefix}/icons/icon?<generated>`}
            type="image/<generated>"
            sizes="<generated>"
          />
          <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@100..900&display=swap" rel="stylesheet" />
        </head>
        <body>
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
    </LayoutComponent>
  );
}
