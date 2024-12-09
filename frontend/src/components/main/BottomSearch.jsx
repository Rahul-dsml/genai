import React from "react";
import { assets } from "../../assets/assets";
import { IoIosSend } from "react-icons/io";
import { useContext } from "react";
import { GeminiContext } from "../Context/GeminiContext";
import { useLocation } from "react-router-dom";


const BottomSearch = () => {
  const {  onSent, loading, prompt, setPrompt, handleInputSubmit  } =
  useContext(GeminiContext);
  
const location = useLocation();
const currentPage = location.pathname.replace("/", ""); // e.g., "text", "image", "video", "meme"
  return (
    <div className="main-bottom">
      <div
        className="search"
        onKeyDown={(e) => e.key === "Enter" &&  handleInputSubmit(prompt,currentPage)}
      >
        <input
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          disabled = {loading}
          type="text"
          placeholder="What would you like to generate"
        />
        <div className="searchbar-image">
          {/* <img src={assets.Add_Record} alt="" />
          <img src={assets.Add_Image} alt="" /> */}
          {prompt && (
            <span className="cursor-pointer" onClick={() => handleInputSubmit(prompt,currentPage)}>
              <IoIosSend className=" text-xl md:text-3xl mr-4 text-white hover:text-cyan-400 transition-all ease-in"/>
            </span>
          )}
        </div>
      </div>
      <p className="bottomtext text-white">
        Please crosscheck the information from cited links
      </p>
    </div>
  );
};

export default BottomSearch;
