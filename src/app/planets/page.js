"use client";

import * as React from "react";
import { useContext, useState } from "react";
import { ImageList, ImageListItem, Grid, Box } from "@mui/material";
import themeDark from "../styles/themeDark";
import { ThemeSwitchContext } from "../components/ThemeSwitchContext";

export default function Planets() {
  const [theme, setTheme] = useContext(ThemeSwitchContext);
  const planetImgLink =
    theme == themeDark
      ? "http://hokoon.edu.hk/astroInfo/images/moonNplanet.png"
      : "http://hokoon.edu.hk/astroInfo/images/moonNplanet_red.png"; //for testing

  return (
    <Grid
      container
      direction="column"
      alignItems="center"
      spacing={2}
      xs={12}
      sm={10}
      md={8}
      lg={6}
    >
      <Grid item>
        <ImageList sx={{ width: 1 }} cols={1} gap={8}>
          <ImageListItem>
            <img src={planetImgLink} />
          </ImageListItem>
        </ImageList>
      </Grid>
      <Box sx={{ height: "6rem" }} />
    </Grid>
  );
}
