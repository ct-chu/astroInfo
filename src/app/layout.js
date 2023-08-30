import "./globals.css";
import { CssBaseline } from "@mui/material";
import localFont from "next/font/local";

import Menu from "./components/menu";
import LayoutComponent from "./components/layoutComponent";

const NotoSanstc_R = localFont({ src: "./pages/NotoSansTC-Regular.otf" });

export const metadata = {
  title: "可觀天文助理",
  description: "Realtime info for astronomical observation, provided by HKNEAC",
  manifest: "http://hokoon.edu.hk/astroInfo/manifest.json",
  appleWebApp: {
    title: "可觀天文助理",
    statusBarStyle: "black-translucent",
    startupImage: ["http://www.hokoon.edu.hk/astroInfo/icons/cover.jpg"],
  },
};

export default function RootLayout({ children }) {
  return (
    <LayoutComponent>
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
    </LayoutComponent>
  );
}
