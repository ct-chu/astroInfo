"use client";

import * as React from "react";
import { useState, useContext } from "react";
import { ImageList, ImageListItem, Grid, Typography, Box } from "@mui/material";
import Lightbox from "yet-another-react-lightbox";
import "yet-another-react-lightbox/styles.css";
import Zoom from "yet-another-react-lightbox/plugins/zoom";
import themeDark from "../styles/themeDark";
import { ThemeSwitchContext } from "../components/ThemeSwitchContext";

export default function Skymap() {
  const [theme, setTheme] = useContext(ThemeSwitchContext);
  const skymapLink =
    theme == themeDark
      ? "http://hokoon.edu.hk/astroInfo/images/Hokoon_skymap.png"
      : "http://hokoon.edu.hk/astroInfo/images/Hokoon_skymap_red.png";
  const skymapChnLink =
    theme == themeDark
      ? "http://hokoon.edu.hk/astroInfo/images/Hokoon_skymap_CHN.png"
      : "http://hokoon.edu.hk/astroInfo/images/Hokoon_skymap_CHN_red.png";
  const [open, setOpen] = useState(false);
  const [lightboxURL, setLightboxURL] = useState(skymapLink);

  return (
    <Grid
      container
      direction="column"
      alignItems="center"
      xs={12}
      sm={10}
      md={8}
      lg={6}
    >
      <Box sx={{ height: "2rem" }} />

      <Grid item sx={{ width: 0.85 }}>
        <ImageList sx={{ width: 1 }} cols={1} gap={8}>
          <Typography variant="sectionTitle">
            即時星圖 Realtime Skymap
            <br />
          </Typography>
          <Typography variant="small">
            按圖放大 Press image to zoom <br />
          </Typography>

          <ImageListItem>
            <img
              src={skymapLink}
              onClick={() => {
                setOpen(true);
                setLightboxURL(skymapLink);
              }}
            />
          </ImageListItem>

          <Box sx={{ height: "2rem" }} />

          <Typography variant="sectionTitle">
            即時中國星圖 Realtime Chinese Skymap
            <br />
          </Typography>
          <Typography variant="small">
            按圖放大 Press image to zoom <br />
          </Typography>

          <ImageListItem>
            <img
              src={skymapChnLink}
              onClick={() => {
                setOpen(true);
                setLightboxURL(skymapChnLink);
              }}
            />
          </ImageListItem>
        </ImageList>
        <Box sx={{ height: "6rem" }} />
      </Grid>

      <Lightbox
        open={open}
        close={() => setOpen(false)}
        plugins={[Zoom]}
        slides={[
          {
            src: lightboxURL,
          },
        ]}
        render={{
          buttonPrev: () => null,
          buttonNext: () => null,
        }}
      />
    </Grid>
  );
}
