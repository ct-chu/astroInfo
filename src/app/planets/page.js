"use client";

import * as React from "react";
import { useContext, useState } from "react";
import { ImageList, ImageListItem, Grid } from "@mui/material";
import themeDark from "../styles/themeDark";
import { ThemeSwitchContext } from "../components/ThemeSwitchContext";

export default function Planets() {
  const [theme, setTheme] = useContext(ThemeSwitchContext)
  const planetImgLink = (theme == themeDark)?
    "https://live.staticflickr.com/65535/53121429242_f313301d18_o_d.png":
    "https://live.staticflickr.com/65535/53152185275_2139249a3d_o_d.png"; //for testing

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
    </Grid>
  );
}
