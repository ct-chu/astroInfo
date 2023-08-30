"use client";

import React from 'react';
import { useState } from 'react';
import { ThemeProvider } from "@mui/material/styles";

import themeDark from "../styles/themeDark";
import { ThemeSwitchContext } from "./ThemeSwitchContext";

export default function LayoutComponent({ children })  {

    const [theme, setTheme] = useState(themeDark);
  
    return (
      <ThemeSwitchContext.Provider value={[theme, setTheme]}>
        <ThemeProvider theme={theme}>
            {children}
        </ThemeProvider>
      </ThemeSwitchContext.Provider>
    );
  }