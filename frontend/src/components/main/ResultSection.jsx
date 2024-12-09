import React, { useContext } from "react";
import { assets } from "../../assets/assets";
import { FaUserCircle } from "react-icons/fa";
import Loader from "./Loader";
import Cards from "../TextCards";
import { GeminiContext } from "../Context/GeminiContext";

const ResultSection = () => {
  const { recentPrompt, result, loading, messages, prompt} =
    useContext(GeminiContext);
  return (
    <>
      {/* {messages.map((message, index) => {
        return (
            <Cards
              key={index}
              role={message.role}
              message={message.text}
              loading={loading}
            />
         
        );
      })} */}
    <div className="result mt-8">
       
      <div className="result-title ml-1 text-blue-500">
        <div className="userMessage flex gap-2">
          <span>
            <FaUserCircle className="text-white text-[2.2rem]" />
          </span>
          <div class="bg-slate-100 text-black p-4 rounded-lg shadow-md">
            <p>{messages.map(message=>message.text)}</p>
          </div>
        </div>
      </div> 
      <div className="result-data flex gap-2">
        <img className="rounded-full text-xl" src={assets.Cyber} alt="" />
        {loading ? (
          <Loader />
        ) : (
          <div class="bg-gradient-to-r from-white/5 to-white/10 backdrop-blur-md text-white p-4 rounded-xl shadow-lg">
            <p
              className="text-xs md:text-base"
              dangerouslySetInnerHTML={{ __html: result }}
            ></p>
          </div>
        )}
      </div>
      </div>
   </>
  );
};

export default ResultSection;
