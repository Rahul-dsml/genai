import React, { useContext, useState } from "react";
import { GeminiContext } from "../components/Context/GeminiContext";
import TopMenu from "../components/main/TopMenu";
import HeroSection from "../components/main/HeroSection";
import { Result } from "../components/Result";
import BottomSearch from "../components/main/BottomSearch";


const MemeGenerator = () => {
  const {
   
    showResult
  } = useContext(GeminiContext);

  return (
    <div className="main">
      <TopMenu />
      <div className="main-container">
        <Result/>
        <BottomSearch />
      </div>
    </div>
  );
};

export default MemeGenerator;
