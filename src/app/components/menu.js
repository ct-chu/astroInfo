"use client";

import * as React from "react";
import { useState, useContext, useLayoutEffect } from "react";
import Link from "next/link";
import Cookies from "universal-cookie";

import { ThemeProvider } from "@mui/material/styles";
import {
  CssBaseline,
  AppBar,
  Box,
  Toolbar,
  Typography,
  Fab,
  IconButton,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Divider,
  Switch,
} from "@mui/material";
import MenuIcon from "@mui/icons-material/Menu";
import CloudIcon from "@mui/icons-material/Cloud";
import NightlightRoundIcon from "@mui/icons-material/NightlightRound";
import AutoAwesomeIcon from "@mui/icons-material/AutoAwesome";
import InfoIcon from "@mui/icons-material/Info";
import WbSunnyIcon from "@mui/icons-material/WbSunny";
import RefreshIcon from "@mui/icons-material/Refresh";
import StarIcon from "@mui/icons-material/Star";
import HelpIcon from '@mui/icons-material/Help';
import FacebookIcon from "@mui/icons-material/Facebook";
import InstagramIcon from "@mui/icons-material/Instagram";
import YouTubeIcon from "@mui/icons-material/YouTube";
import { alpha, styled } from "@mui/material/styles";
import { red } from "@mui/material/colors";

import themeRed from "../styles/themeRed";
import themeDark from "../styles/themeDark";
import { ThemeSwitchContext } from "./ThemeSwitchContext";

export default function Menu() {
  const [isDrawerOpen, setIsDrawerOpen] = useState(false);
  const forceUpdate = () => window.location.reload(true);
  const [checked, setChecked] = useState(false);
  const [eng, setEng] = useState(false);
  const [theme, setTheme] = useContext(ThemeSwitchContext);
  const cookies = new Cookies(null, { path: '/' });

  const menuText = {
    title: { hk: "可觀天文助理", en: "Ho Koon Astro-info" },
    weather: { hk: "天氣", en: "Weather" },
    sun: { hk: "太陽", en: "The Sun" },
    moon: { hk: "月球與行星", en: "Moon & Planets" },
    skychart: { hk: "即時中西星圖", en: "Realtime Skymap" },
    pole: { hk: "極軸鏡", en: "Polarscope" },
    about: { hk: "關於", en: "About" },
    help: { hk: "幫助", en: "Help" },
    redlight: { hk: "紅光模式", en: "Red-light Mode" },
  };

  const handleToggle = () => {
    if (theme == themeDark) {
      setTheme(themeRed);
      setChecked(true);
      cookies.set("red", true, { path: "/" });
    } else {
      setTheme(themeDark);
      setChecked(false);
      cookies.set("red", false, { path: "/" });
    }
  };

  useLayoutEffect(() => {
    if (cookies.get("eng") === true) {
      setEng(true);
    } else {
      setEng(false);
    }
    if (cookies.get("red") === true) {
      setTheme(themeRed);
      setChecked(true);
    } else {
      setTheme(themeDark);
      setChecked(false);
    }
  }, []);

  const langToggle = () => {
    if (eng === false) {
      setEng(true);
      cookies.set("eng", true, { path: "/" });
    } else {
      setEng(false);
      cookies.set("eng", false, { path: "/" });
    }
  };

  function LangSwitch() {
    const RedSwitch = styled(Switch)(({ theme }) => ({
      "& .MuiSwitch-switchBase": {
        color: "#930",
        "&:hover": {
          backgroundColor: alpha(red[900], theme.palette.action.hoverOpacity),
        },
        "& + .MuiSwitch-track": {
          opacity: 1,
          backgroundColor: "#300",
        },
      },
      "& .MuiSwitch-switchBase.Mui-checked": {
        color: red[900],
        "&:hover": {
          backgroundColor: alpha(red[900], theme.palette.action.hoverOpacity),
        },
      },
      "& .MuiSwitch-switchBase.Mui-checked + .MuiSwitch-track": {
        backgroundColor: "#900",
      },
    }));
    if (theme == themeDark) {
      return (
        <ListItem>
          <Switch edge="start" onChange={() => langToggle()} checked={eng} />
          <ListItemText
            primary={<Typography variant="menu">&nbsp; English</Typography>}
          />
        </ListItem>
      );
    } else {
      return (
        <ListItem>
          <RedSwitch edge="start" onChange={() => langToggle()} checked={eng} />
          <ListItemText
            primary={<Typography variant="menu">&nbsp; English</Typography>}
          />
        </ListItem>
      );
    }
  }

  function ModeSwitch() {
    const RedSwitch = styled(Switch)(({ theme }) => ({
      "& .MuiSwitch-switchBase.Mui-checked": {
        color: red[900],
        "&:hover": {
          backgroundColor: alpha(red[900], theme.palette.action.hoverOpacity),
        },
      },
      "& .MuiSwitch-switchBase.Mui-checked + .MuiSwitch-track": {
        backgroundColor: "#F00",
      },
    }));

    return (
      <ListItem>
        <RedSwitch
          edge="start"
          onChange={() => handleToggle()}
          checked={checked}
        />
        <ListItemText
          primary={
            <Typography variant="menu">
              &nbsp;{" "}
              {eng === false ? menuText.redlight.hk : menuText.redlight.en}
            </Typography>
          }
        />
      </ListItem>
    );
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

              <Typography
                variant="sectionTitle"
                component="div"
                sx={{ flexGrow: 1 }}
              >
                {eng === false ? menuText.title.hk : menuText.title.en}
              </Typography>
              <Link href="https://www.facebook.com/hokoon.astro" target="_blank" rel="noopener noreferrer">
                <IconButton edge="end" color="primary" sx={{ ml: 0 }}>
                  <FacebookIcon />
                </IconButton>
              </Link>
              <Link href="https://www.instagram.com/hokoon.astro/" target="_blank" rel="noopener noreferrer">
                <IconButton edge="end" color="primary" sx={{ ml: 0.5 }}>
                  <InstagramIcon />
                </IconButton>
              </Link>
              <Link href="https://www.youtube.com/@HokoonChannel" target="_blank" rel="noopener noreferrer">
                <IconButton edge="end" color="primary" sx={{ ml: 0.5 }}>
                  <YouTubeIcon />
                </IconButton>
              </Link>
              <Drawer
                open={isDrawerOpen}
                PaperProps={{
                  sx: {
                    backgroundColor:
                      theme == themeDark
                        ? "rgba(30, 30, 30, 0.9)"
                        : "rgba(15, 0, 0, 0.9)",
                    color: "rgba(255,255,255,1)",
                  },
                }}
                onClose={() => setIsDrawerOpen(false)}
              >
                <List>
                  <ListItem key={"天氣"} disablePadding>
                    <Link href="./" passHref>
                      <ListItemButton
                        onClick={() => setIsDrawerOpen(false)}
                        sx={{ width: 1 }}
                      >
                        <ListItemIcon>
                          <CloudIcon color="primary" />
                        </ListItemIcon>
                        <ListItemText
                          primary={
                            <Typography variant="menu">
                              {eng === false
                                ? menuText.weather.hk
                                : menuText.weather.en}
                            </Typography>
                          }
                        />
                      </ListItemButton>
                    </Link>
                  </ListItem>
                  <ListItem key={"太陽"} disablePadding>
                    <Link href="sun.html" passHref>
                      <ListItemButton onClick={() => setIsDrawerOpen(false)}>
                        <ListItemIcon>
                          <WbSunnyIcon color="primary" />
                        </ListItemIcon>
                        <ListItemText
                          primary={
                            <Typography variant="menu">
                              {eng === false
                                ? menuText.sun.hk
                                : menuText.sun.en}
                            </Typography>
                          }
                        />
                      </ListItemButton>
                    </Link>
                  </ListItem>
                  <ListItem key={"月球與行星"} disablePadding>
                    <Link href="planets.html" passHref>
                      <ListItemButton onClick={() => setIsDrawerOpen(false)}>
                        <ListItemIcon>
                          <NightlightRoundIcon color="primary" />
                        </ListItemIcon>
                        <ListItemText
                          primary={
                            <Typography variant="menu">
                              {eng === false
                                ? menuText.moon.hk
                                : menuText.moon.en}
                            </Typography>
                          }
                        />
                      </ListItemButton>
                    </Link>
                  </ListItem>
                  <ListItem key={"即時中西星圖"} disablePadding>
                    <Link href="skymap.html" passHref>
                      <ListItemButton onClick={() => setIsDrawerOpen(false)}>
                        <ListItemIcon>
                          <AutoAwesomeIcon color="primary" />
                        </ListItemIcon>
                        <ListItemText
                          primary={
                            <Typography variant="menu">
                              {eng === false
                                ? menuText.skychart.hk
                                : menuText.skychart.en}
                            </Typography>
                          }
                        />
                      </ListItemButton>
                    </Link>
                  </ListItem>
                  <ListItem key={"北極星"} disablePadding>
                    <Link href="pole.html" passHref>
                      <ListItemButton onClick={() => setIsDrawerOpen(false)}>
                        <ListItemIcon>
                          <StarIcon color="primary" />
                        </ListItemIcon>
                        <ListItemText
                          primary={
                            <Typography variant="menu">
                              {eng === false
                                ? menuText.pole.hk
                                : menuText.pole.en}
                            </Typography>
                          }
                        />
                      </ListItemButton>
                    </Link>
                  </ListItem>
                </List>
                <Divider />
                <List>
                  <ListItem key={"幫助"} disablePadding>
                    <Link href="help.html" passHref>
                      <ListItemButton onClick={() => setIsDrawerOpen(false)}>
                        <ListItemIcon>
                          <HelpIcon color="primary" />
                        </ListItemIcon>
                        <ListItemText
                          primary={
                            <Typography variant="menu">
                              {eng === false
                                ? menuText.help.hk
                                : menuText.help.en}
                            </Typography>
                          }
                        />
                      </ListItemButton>
                    </Link>
                  </ListItem>
                  <ListItem key={"關於"} disablePadding>
                    <Link href="about.html" passHref>
                      <ListItemButton onClick={() => setIsDrawerOpen(false)}>
                        <ListItemIcon>
                          <InfoIcon color="primary" />
                        </ListItemIcon>
                        <ListItemText
                          primary={
                            <Typography variant="menu">
                              {eng === false
                                ? menuText.about.hk
                                : menuText.about.en}
                            </Typography>
                          }
                        />
                      </ListItemButton>
                    </Link>
                  </ListItem>
                  <ModeSwitch />
                  <LangSwitch />
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
