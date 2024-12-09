import { useContext, useRef, useEffect } from "react";
import { GeminiContext } from "./Context/GeminiContext";
import { assets } from "../assets/assets";
import { FaUserCircle } from "react-icons/fa";
import Loader from "./main/Loader";
import autoAnimate from "@formkit/auto-animate";
import TextCards from "./TextCards";
import ImageCards from "./ImageCards";
import VideoCard from "./VideoCard";
import { useLocation } from "react-router-dom";
import MemeCard from "./MemeCard";

export const Result = () => {
  const location = useLocation();
  const currentPage = location.pathname.replace("/", "");
  const parent = useRef(null);
  const bottomRef = useRef(null);
  const { recentPrompt, result, loading, messages, prompt, handleRegenerate } =
    useContext(GeminiContext);

  // only for aut animations
  useEffect(() => {
    parent.current && autoAnimate(parent.current);
  }, [parent]);

  //for scrolling bottom
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="result mt-8" ref={parent}>
      {messages[currentPage]?.map((message, index) => (
        <div key={index} className="message">
          {message.role === "user" ? (
            <div className="flex gap-4 items-start">
              <FaUserCircle className="text-white text-[2.2rem]" />
              <div className="bg-slate-100 text-black p-4 rounded-lg shadow-md">
                {message.text}
              </div>
            </div>
          ) : (
            <div className="ai-message flex gap-4 items-start">
              <img className="rounded-full h-10" src={assets.Cyber} alt="AI" />
              {message.loading ? (
                <Loader />
              ) : (
                <>
                  {currentPage === "text" && (
                    <TextCards
                      message={message.text}
                     
                    />
                  )}
                  {currentPage === "images" && (
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                      {message.text.image_post.map((imageUrl, index) => (
                        <ImageCards
                          key={index}
                          imageUrl={imageUrl} // Pass each image URL as an array
                         
                         
                        />
                      ))}
                    </div>
                  )}
                  {currentPage === "videos" && (
                    <VideoCard
                      videoUrl={
                        message.videoUrl ||
                        "https://www.w3schools.com/html/mov_bbb.mp4"
                      }
                      initialMessage={
                        message.text ||
                        "This feature is under development and will be available"
                      }
                     
                    />
                  )}
                  {currentPage === "memes" &&
                    message.text.memes_url &&
                    Array.isArray(message.text.memes_url) && (
                      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                        {message.text.memes_url.map(
                          ([url, title], memeIndex) => (
                            <MemeCard
                              key={memeIndex}
                              memeUrl={url}
                              initialMessage={
                                title ||
                                "This feature is under development and will be available"
                              }
                            
                            />
                          )
                        )}
                      </div>
                    )}
                </>
              )}
            </div>
          )}
        </div>
      ))}
      <div className="scrollIndicatore" ref={bottomRef}></div>
    </div>
  );
};
