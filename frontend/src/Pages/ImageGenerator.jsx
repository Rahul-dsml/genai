import React, { useContext, useState } from "react";
import { GeminiContext } from "../components/Context/GeminiContext";
import TopMenu from "../components/main/TopMenu";
import HeroSection from "../components/main/HeroSection";
import { Result } from "../components/Result";
import BottomSearch from "../components/main/BottomSearch";


const ImageGenerator = () => {
  const {
    input,
    setInput,
    showResult,
    recentPrompt,
    result,
    onSent,
    loading,
    messages,
    prompt,
    setPrompt,
    handleInputSubmit,
    chat,
    setChat,
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

export default ImageGenerator;
