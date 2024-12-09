import React, { useState } from "react";
import { assets } from "../assets/assets";
import { FaUserCircle } from "react-icons/fa";
import Loader from "./main/Loader";
import { useContext } from "react";
import { GeminiContext } from "./Context/GeminiContext";
import { IoIosSend } from "react-icons/io";
import { BallTriangle } from "react-loader-spinner";


const PopupDialog = () => {
  //   const [isOpen, setIsOpen] = useState(true);
  const [query, setQuery] = useState("");
  const [isUser, setIsUser] = useState(false);
  const [userQuery, setUserQuery] = useState("");

  const {
    loading,
    handleSummarySubmit,
    summaryResult,
    setSummaryResult,
    isOpen,
    setIsOpen,
    extend,
    setExtend,
  } = useContext(GeminiContext);

  const handleSubmit = async () => {
    if (!query.trim()) return; // Prevent empty submission
    setUserQuery(query);
    await handleSummarySubmit(query); // Send the query to the parent component
    setExtend(true);
    setQuery(""); // Clear input

    setIsOpen(false); // Close the dialog box
  };

  return (
    <>
      {/* Blur background */}
      {isOpen && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-40"></div>
      )}

      {/* Dialog Box */}
      {isOpen && (
        <div className="fixed inset-0 flex items-center justify-center z-50">
          <div className="bg-gradient-to-r from-white/10 to-white/20 backdrop-blur-md text-white w-96 h-96 lg:w-[40rem] lg:h-[30rem] p-6 rounded-lg shadow-lg flex flex-col justify-between">
            {/* <h2 className="text-2xl font-bold mb-4">
              Hi! What can we do for you?
            </h2> */}
            <div className="cardcontains flex flex-col gap-4">
              <div className="mx-auto  text-md md:text-xl text-center white">
                <span className="text-bold text-2xl md:text-3xl text-white">
                  MetamindAI
                </span>{" "}
                <p className="text-sm md:text-xl mt-6">
                Your smart assistant for personalized chats, images,
                videos, and more—tailored to your needs!
                </p>
              </div>

              {/* {isUser && (
                <div className="flex gap-4 items-start">
                  <FaUserCircle className="text-white text-[2.2rem]" />
                  <p className="bg-gradient-to-r from-white/5 to-white/10 backdrop-blur-md text-white p-2 text-xs rounded-xl shadow-lg">
                    {userQuery}
                  </p>
                </div>
              )} */}
              {loading ? (
                <div className="popUpLoader w-full m-3 display flex flex-col items-center gap-1">
                  {/* <Loader /> */}
                  <BallTriangle
                    height={100}
                    width={100}
                    radius={5}
                    color="#4fa94d"
                    ariaLabel="ball-triangle-loading"
                    wrapperStyle={{}}
                    wrapperClass=""
                    visible={true}
                  />
                  <p>Generating...</p>
                </div>
              ) : 
              <div className="containerer flex justify-center">
                <img className="h-52 w-52" src={assets.buildWithAi} alt="" />
              </div>
              }
            </div>
            <div className="SummarySearchInput w-full h-14 bg-gradient-to-r from-white/5 to-white/10 backdrop-blur-md text-white p-4 shadow-lg rounded-full mb-4 flex border justify-between items-center">
              <input
                className="w-[30rem] bg-transparent p-2 text-white border-none rounded-full focus:outline-none"
                placeholder="summary of trending LLMs used in Generative AI"
                disabled={loading}
                value={query}
                onChange={(e) => setQuery(e.target.value)}
              />
              <button
                className="bg-cyan-500 text-white ml-2 p-3 text-sm rounded-full hover:bg-cyan-600 transition-all ease-in-out shadow-md focus:outline-none"
                onClick={handleSubmit}
              >
                
                <IoIosSend className="text-xl text-white" />
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default PopupDialog;
