"use client";

import * as React from "react";
import { useState } from "react";
import { Grid, ImageList, ImageListItem, Typography, Box } from "@mui/material";
import Lightbox from "yet-another-react-lightbox";
import "yet-another-react-lightbox/styles.css";
import Zoom from "yet-another-react-lightbox/plugins/zoom";

export default function Sun() {
  const currentTimeStamp = "?" + new Date().getTime();
  const sunHmi =
    "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIIF.jpg" + currentTimeStamp;
  const sunAia =
    "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0304.jpg" + currentTimeStamp;
  const sunActive =
    "http://jsoc.stanford.edu/doc/data/hmi/harp/harp_nrt/latest_nrt.png" + currentTimeStamp;
    const [open, setOpen] = useState(false);
  const [lightboxURL, setLightboxURL] = useState(sunHmi);

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
      <Grid item sx={{ width: 0.85 }}>
        <Box sx={{ height: "2rem" }} />
        <Typography variant="sectionTitle">
          太陽影像 Solar image
          <br />
        </Typography>
        <Typography align="center" variant="small">
          Lastest images from Solar Dynamics Observatory, NASA. Press image to zoom 按圖放大
          <br />
          <br />
        </Typography>
        <Typography variant="content">
          HMI<br />
        </Typography>
        <ImageList sx={{ width: 1 }} cols={1} gap={8}>
          <ImageListItem>
            <img src={sunHmi} onClick={() => {
                setOpen(true);
                setLightboxURL(sunHmi);
              }}/>
          </ImageListItem>
        </ImageList>
        <Box sx={{ height: "2rem" }} />
        <Typography align="center" variant="content">
          AIA 304 Å <br />
        </Typography>
        <ImageList sx={{ width: 1 }} cols={1} gap={8}>
          <ImageListItem>
            <img src={sunAia} onClick={() => {
                setOpen(true);
                setLightboxURL(sunAia);
              }}/>
          </ImageListItem>
        </ImageList>
        <Box sx={{ height: "2rem" }} />
        <Typography align="center" variant="content">
          HMI Active Region Patch<br /><br />
        </Typography>
        <ImageList sx={{ width: 1 }} cols={1} gap={8}>
          <ImageListItem>
            <img src={sunActive} onClick={() => {
                setOpen(true);
                setLightboxURL(sunActive);
              }}/>
          </ImageListItem>
        </ImageList>
      </Grid>
      <Box sx={{ height: "2rem" }} />
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
      <Box sx={{ height: "5rem" }} />
    </Grid>
  );
}
