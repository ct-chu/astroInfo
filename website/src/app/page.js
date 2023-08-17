"use client";

import * as React from "react";
import { useState, useEffect } from "react";
import {
  Card,
  CardMedia,
  CardContent,
  Typography,
  Grid,
  Button,
  ImageList,
  ImageListItem,
  ImageListItemBar,
  Box
} from "@mui/material";
import Lightbox from "yet-another-react-lightbox";
import "yet-another-react-lightbox/styles.css";
import Zoom from "yet-another-react-lightbox/plugins/zoom";
import axios from "axios";

export default function Home() {
  const [open, setOpen] = useState(false);
  const [weatherData, setWeatherData] = useState("");
  const [error, setError] = useState(false);
  const [state, setState] = useState("");
  const [updateTime, setUpdateTime] = useState("");
  const [ascList, setAscList] =useState([]);

  const hokoonAscLink = "https://live.staticflickr.com/65535/53122437995_7e97aa9c5a_o_d.png" //for testing only

  useEffect(() => {
    setAscList([
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
        url: "https://www.hko.gov.hk/gts/astronomy/image/asc_tuenmun0.jpg"
      },
    ]);
  }, 1000);

  useEffect(() => {
    setState("loading");
    axios
      .get(
        "https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=en"
      )
      .then((res) => {
        setState("success");
        setUpdateTime(new Date().toLocaleString());
        setWeatherData([
          `https://www.hko.gov.hk/images/HKOWxIconOutline/pic${res.data.icon[0]}.png`,
          res.data.temperature.data[14].value,
          res.data.humidity.data[0].value,
          res.data.uvindex.data[0].desc,
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
      <CardContent sx={{ flex: "1 0 auto", width: 1 }}>
        <Grid
          container
          direction="row"
          alignItems="stretch"
          justifyContent="space-around"
        >
          <Grid item>
            <Typography component="div" variant="content">
              Air temp: {weatherData[1]} °C
            </Typography>
            <Typography component="div" variant="content">
              Humidity: {weatherData[2]} %
            </Typography>
            <Typography component="div" variant="content">
              UV intensity: {weatherData[3]} <br /> <br />
            </Typography>
            <Typography component="div" variant="small">
              Last updated time: {updateTime.substring(0, 9)}{" "}
              {updateTime.substring(11, 21)}
            </Typography>
          </Grid>
          <Grid item xs={2}>
            <CardMedia
              component="img"
              sx={{ width: 1 }}
              image={weatherData[0]}
              alt="Current weather"
            />
          </Grid>
        </Grid>
      </CardContent>
    );
  };

  return (
    <>
      <Grid container direction="column" alignItems="center" spacing={2}>
        <Grid item sx={{ width: 0.85 }}>
          <Typography variant="sectionTitle">
          <br />即時全天影像 Realtime All-sky images<br /><br />
          </Typography>
          <Typography variant="content">可觀中心 Ho Koon <br /> </Typography>
          <Typography variant="small">按圖放大可觀全天影像<br />Press the Ho Koon all-sky image to magnify<br /></Typography>
          <ImageList sx={{width: 1}} cols={1} gap={8}>
            <ImageListItem>
              <img
              src={hokoonAscLink}
              onClick={() => setOpen(true)}
              />
            </ImageListItem>
          </ImageList>
          <Box sx={{ height:"2rem" }} />
          <ImageList sx={{width: 1}} cols={1} gap={8}>
          {ascList.map((image) => (
            <ImageListItem key={image.url}>
              <Typography variant="content">
              {image.site}<br />
              </Typography>
              <img
                src={image.url}
                alt={image.site}
                loading="lazy"
              />
            </ImageListItem>
          ))}
          </ImageList>
          <Box sx={{ height:"1rem" }} />
          <Typography variant="content">
            動畫序列 Animated Sequence <br /><br />
          </Typography>
          <Button
            variant="outlined"
            href="https://www.hko.gov.hk/en/gts/astronomy/site_all.htm"
          >
            Go to HKO site
          </Button>
          <Box sx={{ height:"2rem" }} />
    </Grid>
      <Grid item>
        <Card sx={{ width: 1 }}>
          <CardContent>
            <Typography variant="sectionTitle">
              天氣報告 Current Weather Info
            </Typography>
          </CardContent>
          {state === "loading" ? <h1>Loading...</h1> : <WeatherCard />}
        </Card>
      </Grid>
      </Grid >

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
