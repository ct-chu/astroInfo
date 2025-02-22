"use client";

import * as React from "react";
import { useState, useEffect, useContext } from "react";
import {
  Typography,
  Grid,
  Button,
  ImageList,
  ImageListItem,
  Box,
} from "@mui/material";
import Lightbox from "yet-another-react-lightbox";
import "yet-another-react-lightbox/styles.css";
import Zoom from "yet-another-react-lightbox/plugins/zoom";
import axios from "axios";
import ImageFilter from "react-image-filter";
import themeDark from "./styles/themeDark";
import { ThemeSwitchContext } from "./components/ThemeSwitchContext";

import { prefix } from './prefix.js';

export default function Home() {
  const [open, setOpen] = useState(false);
  const [weatherData, setWeatherData] = useState([]);
  const [error, setError] = useState(false);
  const [state, setState] = useState("");
  const [updateTime, setUpdateTime] = useState("");
  const [theme, setTheme] = useContext(ThemeSwitchContext);
  const noFilter = [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0,];
  const redFilter = [
    0.5, 0.3, 0.5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0,
  ];

  const currentTimeStamp = "?" + new Date().getTime();

  const hokoonAscLink =
    theme == themeDark
      ? "http://hokoon.edu.hk/astroInfo/images/Hokoon_ASC.png" + currentTimeStamp
      : "http://hokoon.edu.hk/astroInfo/images/Hokoon_ASC_red.png" + currentTimeStamp;

  const ascList = [
    {
      site: `鶴咀 Cape D'Aguilar`,
      url: "https://www.hko.gov.hk/gts/astronomy/image/asc_HKCD0.jpg",
    },
    {
      site: "石壁 Shek Pik",
      url: "https://www.hko.gov.hk/gts/astronomy/image/asc_HKSP0.jpg",
    },
    {
      site: "天文公園 Astropark",
      url: "https://www.hko.gov.hk/gts/astronomy/image/asc_astropark0.jpg",
    },
    {
      site: "遙控天文台 iObservatory",
      url: "https://www.hko.gov.hk/gts/astronomy/image/asc_iobservatory0.jpg",
    },
    {
      site: "香港太空館 HK Space Museum",
      url: "https://www.hko.gov.hk/gts/astronomy/image/asc_hksm0.jpg",
    },
    {
      site: "屯門 Tuen Mun",
      url: "https://www.hko.gov.hk/gts/astronomy/image/asc_tuenmun0.jpg",
    },
  ];

  useEffect(() => {
    setState("loading");
    axios
      .get(
        "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=en"
      )
      .then((res) => {
        setState("success");
        setUpdateTime(new Date().toLocaleString());
        let uvDescription =
          typeof res.data.uvindex.data === "undefined"
            ? "N/A"
            : res.data.uvindex.data[0].desc;
        setWeatherData([
          `https://www.hko.gov.hk/images/HKOWxIconOutline/pic${res.data.icon[0]}.png`,
          res.data.temperature.data[14].value,
          res.data.humidity.data[0].value,
          uvDescription,
        ]);
      })
      .catch((err) => {
        console.error("Error:", err);
        setState("error");
        setError(err);
      });
  }, []);
  if (state === "error") return <h1>{error.toString()}</h1>;

  const WeatherCard = () => {
    return (
      <>
        <Grid
          container
          direction="row"
          alignItems="stretch"
          justifyContent="space-around"
          sx={{ width: 1 }}
        >
          <Grid item xs={8}>
            <Typography component="div" variant="content">
              Air temp: {weatherData[1]} °C
            </Typography>
            <Typography component="div" variant="content">
              Humidity: {weatherData[2]} %
            </Typography>
            <Typography component="div" variant="content">
              UV intensity: {weatherData[3]} <br /> <br />
            </Typography>
          </Grid>
          <Grid item xs={4}>
            <ImageFilter
              image={weatherData[0]}
              style={{ maxWidth: 80 }}
              alt="Current weather"
              filter={theme == themeDark ? noFilter : redFilter}
            />
          </Grid>
        </Grid>
        <Typography component="div" variant="small">
          Last updated time: {updateTime}
        </Typography>
      </>
    );
  };

  return (
    <>
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
        <Box sx={{ height: "2rem" }} />
        <Grid item sx={{ width: 0.85 }}>
          <Typography variant="sectionTitle">
            天氣報告 Current Weather Info
            <br />
            <br />
          </Typography>

          {state === "loading" ? <h1>Loading...</h1> : <WeatherCard />}
        </Grid>

        <Grid item sx={{ width: 0.85 }}>
          <Typography variant="sectionTitle">
            <br />
            即時全天影像 Realtime All-sky images
            <br />
            <br />
          </Typography>
          <Typography variant="content">
            可觀中心 Ho Koon <br />{" "}
          </Typography>
          <Typography variant="small">
            按圖放大可觀全天影像
            <br />
            Press the Ho Koon all-sky image to magnify
            <br />
          </Typography>
          <ImageList sx={{ width: 1 }} cols={1}>
            <ImageListItem>
              <img src={hokoonAscLink} onClick={() => setOpen(true)} />
            </ImageListItem>
          </ImageList>
          <Box sx={{ height: "2rem" }} />
          <ImageList
            sx={{
              gridTemplateColumns:
                "repeat(auto-fill, minmax(280px, 1fr))!important",
            }}
            gap={50}
          >
            {ascList.map((image) => (
              <ImageListItem key={image.url}>
                <Typography variant="content">
                  {image.site}
                  <br />
                  <br />
                </Typography>
                <ImageFilter
                  image={image.url}
                  alt={image.site}
                  loading="lazy"
                  filter={theme == themeDark ? noFilter : redFilter}
                />
              </ImageListItem>
            ))}
          </ImageList>
          <Box sx={{ height: "1rem" }} />
          <Typography variant="content">
            動畫序列 Animated Sequence <br />
            <br />
          </Typography>
          <Button
            variant="outlined"
            href="https://www.hko.gov.hk/tc/gts/astronomy/site_all.htm"
          >
            Go to HKO site
          </Button>
          <Box sx={{ height: "2rem" }} />
        </Grid>
        <Box sx={{ height: "4rem" }} />
      </Grid>
      <Lightbox
        open={open}
        close={() => setOpen(false)}
        plugins={[Zoom]}
        slides={[
          {
            src: hokoonAscLink,
          },
        ]}
        render={{
          buttonPrev: () => null,
          buttonNext: () => null,
        }}
      />
    </>
  );
}
