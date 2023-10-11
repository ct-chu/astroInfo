"use client";

import * as React from "react";
import { Box, Grid, Typography, ImageList, ImageListItem } from "@mui/material";

export default function About() {

  const iospwaURL = "http://hokoon.edu.hk/astroInfo/ios_pwa.jpg";
  const androidpwaURL = "http://hokoon.edu.hk/astroInfo/android_pwa.jpg";

  return (
    <Grid
      container
      direction="row"
      justifyContent="center"
      alignItems="center"
    >
      <Grid item sx={{ width: 0.9 }}>
        <Box sx={{ height: "3rem" }} />
        <Typography variant="sectionTitle">
          幫助 Help
          <br />
        </Typography>
        <Box sx={{ height: "1rem" }} />
        <Typography variant="content">
          更新資料<br />
          Update info<br />
        </Typography>
        <Typography variant="small">
          本網頁提供有便計劃天文觀測的即時資訊，各項資料均附有更新時間，請以右下角的「REFRESH」按鈕取得最新資料。
          <br />
          This website provides convenient realtime info for planning astronimcal observations, all info comes with a &quot;last updated time&quot;, for the latest data, please use the &quot;REFRESH&quot; button at the lower right corner.
          <br />
          <br />
        </Typography>
        <Typography variant="content">
          「加入主畫面」功能<br />
          &quot;Add to home screen&quot; feature<br />
        </Typography>
        <Typography variant="small">
          手機用戶可將此網頁加至主畫面，以得到更快速和整合的體驗。<br />
          Mobile users can add this website to the home page for a faster and more integrated experience. <br /> <br />
          iOS/ iPadOS (Safari) 用戶：<br />
          For iOS/ iPadOS (Safari) users:
        </Typography>
      </Grid>
      <Grid item
        xs={10}
        sm={7}
        md={5}
        lg={3}
      >
        <ImageList sx={{ width: 1 }} cols={1} gap={8}>
          <ImageListItem>
            <img src={iospwaURL} />
          </ImageListItem>
        </ImageList>
      </Grid>
      <Grid item sx={{ width: 0.9 }}>
        <Typography variant="small">
          <br />Android (Chrome) 用戶：<br />
          For Android (Chrome) users:
        </Typography>
      </Grid>
      <Grid item
        xs={10}
        sm={7}
        md={5}
        lg={3}
      >
        <ImageList sx={{ width: 1 }} cols={1} gap={8}>
          <ImageListItem>
            <img src={androidpwaURL} />
          </ImageListItem>
        </ImageList>
      </Grid>
      <Box sx={{ height: "4rem" }} />
      <Grid item sx={{ width: 0.9 }}>
        <Typography variant="content">
          頁面說明<br />
          Page description<br />
        </Typography>
        <Typography variant="small">
          用戶可以從左側選單選擇查看不同資訊。<br />
          「天氣」頁面提供簡略即時天氣報告和各區全天影像<br />
          「太陽」頁面提供最新太陽影像和觀測資料<br />
          「月球與行星」頁面提供相位、星等、出沒時間等月球和行星資料和天文曙光時間<br />
          「即時中西星圖」頁面提供即時的標準88星座星圖和中國星官星圖，顯示各星座在天空的位置<br />
          「極軸鏡」頁面提供北極星在北天極（天球北極）旁的角度位置，供使用者對準極軸鏡時參考<br />
          除非另外註明，否則資料均以可觀中心的地理位置計算得出。<br />
          <br />
          User can access different info from the side menu on the left. <br />
          &quot;Weather&quot; provides basic realtime weather report and All-sky images across Hong Kong. <br />
          &quot;The Sun&quot; provides the latest solar images and observation data. <br />
          &quot;Moon & Planets&quot; provides info for the moon and planets (including phase, magnitude, rise and set time) and astronimcal twilight. <br />
          &quot;Realtime Skymap&quot; provides realtime skymaps for the standard 88 IAU constellations and Chinese constellations, showing the location of the constellations on the sky. <br />
          &quot;Polarscope&quot; provides the angular direction of polaris from the North Celestial Pole, for user&lsquo;s reference during polar alignment. <br />
          Unless specified otherwise, information is calculated for the geographical location of Ho Koon Centre.<br />    
        </Typography>
        <Box sx={{ height: "8rem" }} />
      </Grid>
    </Grid>
  );
}