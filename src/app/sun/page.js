"use client";

import * as React from "react";
import { useState, useEffect } from "react";
import { Grid, ImageList, ImageListItem, Typography, Box } from "@mui/material";
import Lightbox from "yet-another-react-lightbox";
import "yet-another-react-lightbox/styles.css";
import Zoom from "yet-another-react-lightbox/plugins/zoom";
import Cookies from "universal-cookie";

export default function Sun() {
  const currentTimeStamp = "?" + new Date().getTime();
  const sunHmi =
    "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIIF.jpg" + currentTimeStamp;
  const sunNSO =
    "https://www.spaceweatherlive.com/images/SDO/SDO_HMIIF_512.jpg" + currentTimeStamp;
  const sunSUVI =
    "https://services.swpc.noaa.gov/images/animations/suvi/primary/304/latest.png" + currentTimeStamp;
  const sunAia =
    "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_0304.jpg" + currentTimeStamp;
  const sunC3 = 
    "https://soho.nascom.nasa.gov/data/realtime/c3/1024/latest.jpg" + currentTimeStamp;
  const sunC3gif = 
    "https://soho.nascom.nasa.gov/data/LATEST/current_c3small.gif" + currentTimeStamp;
  const sunMag = 
    "https://sdo.gsfc.nasa.gov/assets/img/latest/latest_1024_HMIBpfss.jpg" + currentTimeStamp;
  const sunActive =
    "http://jsoc.stanford.edu/doc/data/hmi/harp/harp_nrt/latest_nrt.png" + currentTimeStamp;
    const [open, setOpen] = useState(false);
  const [lightboxURL, setLightboxURL] = useState(sunHmi);
  const [sunspotno, setSunspotno] = useState('N/A');

  const text = {
    hk: {
      title: "太陽影像",
      zoom: "按圖放大",
      hmi: "可觀測太陽黑子的最新狀況",
      aia: "可觀測日珥的最新狀況", 
      c3: "可觀測日冕、太陽拋出物質的最新狀況", 
      c3gif: "可觀測日冕、太陽拋出物質的最新狀況（gif動畫，畫面中間的太陽被遮掩）",
      mag: "可觀測太陽活躍區域和磁場線的最新狀況",
      active: "可觀測太陽活躍區域和其標示的最新狀況", 
    },
    en: {
      title: "Solar Images",
      zoom: "Press image to zoom",
      hmi: "where sunspots could be observed",
      aia: "where solar prominence could be observed",
      c3: "where solar corona and mass ejected from the sun could be observed",
      c3gif: "where solar corona and mass ejected from the sun could be observed (gif animation, the sun in the middle covered)",
      mag: "where active regions and magnetic field lines of the sun could be observed",
      active: "where active regions of the sun and relevant markings could be observed",
    },
  };
  const [showText, setShowText] = useState(text.hk)

  const [eng, setEng] = useState(false);
  const cookies = new Cookies(null, { path: '/' });
  useEffect(() => {
    if (cookies.get("eng") === true) {
      setShowText(text.en);
    } else {
      setEng(text.hk);
    }
  }, []);

  // const GetSunspotNo = () => {
  //   fetch("http://hokoon.edu.hk/astroInfo/sunspot.json" + currentTimeStamp, {mode: 'cors'})
  //     .then((res) => res.json())
  //     .then((json) => {
  //       var ssn = JSON.stringify(json.ssn)
  //       console.log("t= " + json.ssn)
  //       setSunspotno(String(ssn))
  //       console.log("v= " +  sunspotno)
  //     })
  //     .catch((e) => console.error(e));
  //   // fetch("http://hokoon.edu.hk/astroInfo/images/sunspot.html" + currentTimeStamp , {mode: 'cors'})
  //   //   .then((res) => res.text())
  //   //   .then((text) => {
  //   //     var ssn = String(text)
  //   //     console.log("t= " + ssn)
  //   //     setSunspotno(ssn)
  //   //     console.log("v= " +  sunspotno)
  //   //   })
  //   return (
  //     <>
  //       <Typography variant="sectionTitle">
  //       Provisional Sunspot Number: {sunspotno}<br />
  //       </Typography>
  //       <Box sx={{ height: "1rem" }} />
  //     </>
  //   )}

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
        {/* <GetSunspotNo /> */}
        <Typography variant="sectionTitle">
          {showText.title}
          <br />
        </Typography>
        <Typography align="center" variant="small">
          {showText.zoom}<br />
        </Typography>
        <Typography align="center" variant="small">
          Lastest images from Solar Dynamics Observatory and Solar and Heliospheric Observatory, NASA. *
          <br />
          <br />
        </Typography>
        <Typography variant="content">
          {/* HMI<br /> */}
          National Solar Observatory<br />
        </Typography>
        <Typography variant="small">
          {showText.hmi}<br />
        </Typography>
        <ImageList sx={{ width: 1 }} cols={1} gap={8}>
          <ImageListItem>
            {/* <img src={sunHmi} onClick={() => {
                setOpen(true);
                setLightboxURL(sunHmi);
              }}/> */}
            <img src={sunNSO} onClick={() => {
                setOpen(true);
                setLightboxURL(sunNSO);
              }}/>
          </ImageListItem>
        </ImageList>
        <Box sx={{ height: "2rem" }} />
        <Typography align="center" variant="content">
          {/* AIA 304 Å <br /> */}
          304 Å (GOES-R SUVI)<br />
        </Typography>
        <Typography variant="small">
          {showText.aia}<br />
        </Typography>
        <ImageList sx={{ width: 1 }} cols={1} gap={8}>
          <ImageListItem>
            {/* <img src={sunAia} onClick={() => {
                setOpen(true);
                setLightboxURL(sunAia);
              }}/> */}
            <img src={sunSUVI} onClick={() => {
                setOpen(true);
                setLightboxURL(sunSUVI);
              }}/>
          </ImageListItem>
        </ImageList>
        {/* <Box sx={{ height: "2rem" }} />
        <Typography align="center" variant="content">
          SOHO LASCO C3 <br />
        </Typography>
        <Typography variant="small">
          {showText.c3}<br />
        </Typography>
        <ImageList sx={{ width: 1 }} cols={1} gap={8}>
          <ImageListItem>
            <img src={sunC3} onClick={() => {
                setOpen(true);
                setLightboxURL(sunC3);
              }}/>
          </ImageListItem>
        </ImageList> */}
        <Box sx={{ height: "2rem" }} />
        <Typography align="center" variant="content">
          SOHO LASCO C3 (gif) <br />
        </Typography>
        <Typography variant="small">
          {showText.c3gif}<br />
        </Typography>
        <ImageList sx={{ width: 1 }} cols={1} gap={8}>
          <ImageListItem>
            <img src={sunC3gif} onClick={() => {
                setOpen(true);
                setLightboxURL(sunC3gif);
              }}/>
          </ImageListItem>
        </ImageList>
        {/* <Box sx={{ height: "2rem" }} />
        <Typography align="center" variant="content">
          HMI Magnetogram (with Field Lines) <br />
        </Typography>
        <Typography variant="small">
          {showText.mag}<br />
        </Typography>
        <ImageList sx={{ width: 1 }} cols={1} gap={8}>
          <ImageListItem>
            <img src={sunMag} onClick={() => {
                setOpen(true);
                setLightboxURL(sunMag);
              }}/>
          </ImageListItem>
        </ImageList>
        <Box sx={{ height: "2rem" }} />
        <Typography align="center" variant="content">
          HMI Active Region Patch<br />
        </Typography>
        <Typography variant="small">
          {showText.active}<br />
        </Typography>
        <ImageList sx={{ width: 1 }} cols={1} gap={8}>
          <ImageListItem>
            <img src={sunActive} onClick={() => {
                setOpen(true);
                setLightboxURL(sunActive);
              }}/>
          </ImageListItem>
        </ImageList> */}
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
      <Typography align="center" variant="small">
      (*update: images from SDO are temporarily replaced with images from other sources, including the National Solar Observatory, and GOES-R (NASA) due to SDO&apos;s server outage from 26 NOV 2024)
          <br />
          <br />
      </Typography>
      <Box sx={{ height: "5rem" }} />
    </Grid>
  );
}
