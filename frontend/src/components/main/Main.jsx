import React, { useContext, useState } from "react";
import { GeminiContext } from "../Context/GeminiContext";
import TopMenu from "./TopMenu";
import HeroSection from "./HeroSection";
import ResultSection from "./ResultSection";
import BottomSearch from "./BottomSearch";
import { Result } from "../Result";
import PopupDialog from "../PopupDialog";



const Main = () => {


  return (
    <div className="main">
      <TopMenu />
      <div className="main-container">
        <HeroSection/>
        <PopupDialog/>
        {/* <BottomSearch /> */}
      </div>
    </div>
  );
};

export default Main;
