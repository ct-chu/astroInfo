"use client";

import * as React from "react";
import { useState } from "react";
import Link from "next/link";

import { ThemeProvider } from "@mui/material/styles";
import {
  CssBaseline,
  AppBar,
  Box,
  Toolbar,
  Typography,
  Button,
  Fab,
  IconButton,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Divider,
} from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import CloudIcon from "@mui/icons-material/Cloud";
import NightlightRoundIcon from "@mui/icons-material/NightlightRound";
import AutoAwesomeIcon from "@mui/icons-material/AutoAwesome";
import InfoIcon from "@mui/icons-material/Info";
import WbSunnyIcon from "@mui/icons-material/WbSunny";
import RefreshIcon from "@mui/icons-material/Refresh";

import ThemeDark from "../styles/themeDark";

export default function Menu() {
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  const forceUpdate = () => window.location.reload(true);

  return (
    <>
      <ThemeProvider theme={ThemeDark}>
        <CssBaseline />
        <div id="overlay"></div>
        <Box sx={{ flexGrow: 1 }}>
          <AppBar position="static">
            <Toolbar>
              <IconButton
                size="large"
                edge="start"
                color="inherit"
                aria-label="menu"
                sx={{ mr: 2 }}
                onClick={() => setIsDrawerOpen(true)}
              >
                <MenuIcon />
              </IconButton>
              <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                可觀天文資訊
              </Typography>
              {/* <Button color="inherit" variant="small" >紅光模式</Button> */}
              <Drawer
                open={isDrawerOpen}
                PaperProps={{
                  sx: {
                    backgroundColor: "rgba(30, 30, 30, 0.9)",
                    color: "rgba(255,255,255,1)",
                  },
                }}
                onClose={() => setIsDrawerOpen(false)}
              >
                <List>
                  <ListItem key={"天氣"} disablePadding>
                    <Link href="/" passHref>
                      <ListItemButton onClick={() => setIsDrawerOpen(false)}>
                        <ListItemIcon>
                          <CloudIcon />
                        </ListItemIcon>
                        <ListItemText primary="天氣" />
                      </ListItemButton>
                    </Link>
                  </ListItem>
                  <ListItem key={"太陽"} disablePadding>
                    <Link href="/sun" passHref>
                      <ListItemButton onClick={() => setIsDrawerOpen(false)}>
                        <ListItemIcon>
                          <WbSunnyIcon />
                        </ListItemIcon>
                        <ListItemText primary="太陽" />
                      </ListItemButton>
                    </Link>
                  </ListItem>
                  <ListItem key={"月球與行星"} disablePadding>
                    <Link href="/planets" passHref>
                      <ListItemButton onClick={() => setIsDrawerOpen(false)}>
                        <ListItemIcon>
                          <NightlightRoundIcon />
                        </ListItemIcon>
                        <ListItemText primary="月球與行星" />
                      </ListItemButton>
                    </Link>
                  </ListItem>
                  <ListItem key={"即時中西星圖"} disablePadding>
                    <Link href="/skymap" passHref>
                      <ListItemButton onClick={() => setIsDrawerOpen(false)}>
                        <ListItemIcon>
                          <AutoAwesomeIcon />
                        </ListItemIcon>
                        <ListItemText primary="即時中西星圖" />
                      </ListItemButton>
                    </Link>
                  </ListItem>
                </List>
                <Divider />
                <List>
                  <ListItem key={"關於"} disablePadding>
                    <Link href="/about" passHref>
                      <ListItemButton onClick={() => setIsDrawerOpen(false)}>
                        <ListItemIcon>
                          <InfoIcon />
                        </ListItemIcon>
                        <ListItemText primary="關於" />
                      </ListItemButton>
                    </Link>
                  </ListItem>
                </List>
              </Drawer>
            </Toolbar>
          </AppBar>
        </Box>
        <Box
          role="presentation"
          sx={{
            position: "fixed",
            bottom: 32,
            right: 32,
            zIndex: 2000,
          }}
        >
          <Fab variant="extended" onClick={forceUpdate}>
            <RefreshIcon />
            Refresh
          </Fab>
        </Box>
      </ThemeProvider>
    </>
  );
}
