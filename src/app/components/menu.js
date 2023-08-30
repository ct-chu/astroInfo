"use client";

import * as React from "react";
import { useState, useContext } from "react";
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
  Avatar,
  Switch
} from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import CloudIcon from "@mui/icons-material/Cloud";
import NightlightRoundIcon from "@mui/icons-material/NightlightRound";
import AutoAwesomeIcon from "@mui/icons-material/AutoAwesome";
import InfoIcon from "@mui/icons-material/Info";
import WbSunnyIcon from "@mui/icons-material/WbSunny";
import RefreshIcon from "@mui/icons-material/Refresh";
import StarIcon from '@mui/icons-material/Star';
import { alpha, styled } from '@mui/material/styles';
import { red } from '@mui/material/colors';

import themeRed from "../styles/themeRed";
import themeDark from "../styles/themeDark";
import {ThemeSwitchContext} from "./ThemeSwitchContext";

export default function Menu() {
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  const forceUpdate = () => window.location.reload(true);
  const [checked, setChecked] = useState(false);
  const [theme, setTheme] = useContext(ThemeSwitchContext)

  const handleToggle = () => {
    if (theme == themeDark) {
      setTheme(themeRed)
      setChecked(true)
    } else {
      setTheme(themeDark)
      setChecked(false)
    }
  }

  function ModeSwitch() {
    
    const RedSwitch = styled(Switch)(({ theme }) => ({
      '& .MuiSwitch-switchBase.Mui-checked': {
        color: red[900],
        '&:hover': {
          backgroundColor: alpha(red[900], theme.palette.action.hoverOpacity),
        },
      },
      '& .MuiSwitch-switchBase.Mui-checked + .MuiSwitch-track': {
        backgroundColor: red[900],
      },
    }));

    return (
      <ListItem>

        <RedSwitch
          edge="start"
          onChange={() => handleToggle()}
          checked={checked}
        />
        <ListItemText primary={
          <Typography variant="menu">
            &nbsp; 紅光模式
          </Typography>
        }/>

      </ListItem>
    )
  }

  return (
    <>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <div id="overlay"></div>
        <Box sx={{ flexGrow: 1 }}>
          <AppBar position="static">
            <Toolbar>
              <IconButton
                size="large"
                edge="start"
                variant="menu"
                color="primary"
                aria-label="menu"
                sx={{ mr: 0 }}
                onClick={() => setIsDrawerOpen(true)}
              >
                <MenuIcon />
              </IconButton>
              
              <Typography variant="sectionTitle" component="div" sx={{ flexGrow: 1 }}>
              
                可觀天文資訊
              </Typography>
              <Link href="/" passHref>
                <Avatar variant="rounded" src={(theme == themeDark)? "./apple-icon.png" : "../red-icon.png"} />
                </Link>
              <Drawer
                open={isDrawerOpen}
                PaperProps={{
                  sx: {
                    backgroundColor: theme == themeDark? "rgba(30, 30, 30, 0.9)" : "rgba(15, 0, 0, 0.9)",
                    color: "rgba(255,255,255,1)",
                  },
                }}
                onClose={() => setIsDrawerOpen(false)}
              >
                <List>
                  <ListItem key={"天氣"} disablePadding>
                    <Link href="/" passHref>
                      <ListItemButton onClick={() => setIsDrawerOpen(false)} sx={{width: 1}}>
                        <ListItemIcon>
                          <CloudIcon color="primary"/>
                        </ListItemIcon>
                        <ListItemText primary={
                          <Typography variant="menu">
                            天氣
                          </Typography>
                        }/>
                      </ListItemButton>
                    </Link>
                  </ListItem>
                  <ListItem key={"太陽"} disablePadding>
                    <Link href="/sun" passHref>
                      <ListItemButton onClick={() => setIsDrawerOpen(false)}>
                        <ListItemIcon>
                          <WbSunnyIcon color="primary" />
                        </ListItemIcon>
                        <ListItemText primary={
                          <Typography variant="menu">
                            太陽
                          </Typography>
                        }/>
                      </ListItemButton>
                    </Link>
                  </ListItem>
                  <ListItem key={"月球與行星"} disablePadding>
                    <Link href="/planets" passHref>
                      <ListItemButton onClick={() => setIsDrawerOpen(false)}>
                        <ListItemIcon>
                          <NightlightRoundIcon color="primary" />
                        </ListItemIcon>
                        <ListItemText primary={
                          <Typography variant="menu">
                            月球與行星
                          </Typography>
                        }/>
                      </ListItemButton>
                    </Link>
                  </ListItem>
                  <ListItem key={"即時中西星圖"} disablePadding>
                    <Link href="/skymap" passHref>
                      <ListItemButton onClick={() => setIsDrawerOpen(false)}>
                        <ListItemIcon>
                          <AutoAwesomeIcon color="primary" />
                        </ListItemIcon>
                        <ListItemText primary={
                          <Typography variant="menu">
                            即時中西星圖
                          </Typography>
                        }/>
                      </ListItemButton>
                    </Link>
                  </ListItem>
                  <ListItem key={"北極星"} disablePadding>
                    <Link href="/pole" passHref>
                      <ListItemButton onClick={() => setIsDrawerOpen(false)}>
                        <ListItemIcon>
                          <StarIcon color="primary" />
                        </ListItemIcon>
                        <ListItemText primary={
                          <Typography variant="menu">
                            北極星
                          </Typography>
                        }/>
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
                          <InfoIcon color="primary" />
                        </ListItemIcon>
                        <ListItemText primary={
                          <Typography variant="menu">
                            關於
                          </Typography>
                        }/>
                      </ListItemButton>
                    </Link>
                  </ListItem>
                  <ModeSwitch />
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
          <Fab color="secondary" variant="extended" onClick={forceUpdate}>
            <RefreshIcon color="primary" />
            <Typography variant="menu">Refresh</Typography>
          </Fab>
        </Box>
      </ThemeProvider>
    </>
  );
}
