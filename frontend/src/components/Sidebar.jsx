import React, { useContext } from "react";
import { assets } from "../assets/assets";
import { useState } from "react";
import { GeminiContext } from "./Context/GeminiContext";
import { CiMenuFries } from "react-icons/ci";
import { IoAddSharp } from "react-icons/io5";

const Sidebar = () => {
    // const [extend, setExtend] = useState(null);
    const {
      onSent,
      setPrevPrompt,
      prevPrompt,
      recentPrompt,
      setRecentPrompt,
      newChatbtn,
      summaryResult,
      setSummaryResult,
      extend, setExtend
    } = useContext(GeminiContext);
  
    return (
      <>
        <div
          className={`bg-slate-700 px-3 ${extend && "relative z-10 w-96"}`}
        >
          <div className="top-menu">
            <CiMenuFries
              className="text-3xl mt-8 cursor-pointer ml-4 text-slate-200 hover:text-cyan-400 transition-all ease-in "
              onClick={() => setExtend(!extend)}
            />
            <div
              onClick={() => newChatbtn()}
              className="flex cursor-pointer mt-10 items-center gap-2 bg-slate-500 rounded-lg p-2 justify-between max-w-40"
            >
              <IoAddSharp className="text-3xl text-white" />
              {extend ? <p className="text-sm text-white">New Summary</p> : null}
            </div>
            {extend ? (
              <div className="Summary mt-10">
                <h3 className="text-lg font-bold text-white">Summary</h3>
                <div className="summaryMessages mt-4 rounded-md max-h-[30rem] overflow-y-scroll overflow-x-hidden">
                  {summaryResult !== "" && (
                    <div className="summaryResult w-full bg-slate-600 text-white mt-2 rounded-lg p-3">
                      {/* Render the summary */}
                      <p className="text-base leading-relaxed mb-4">
                        {summaryResult.summary}
                      </p>
  
                      {/* Render metadata */}
                      {summaryResult.metadata?.length > 0 && (
                        <div>
                          <h4 className="text-md font-semibold mb-2">Related Articles</h4>
                          <ul className="space-y-2">
                            {summaryResult.metadata.map((item, index) => (
                              <li
                                key={index}
                                className="bg-slate-700 p-3 rounded-md hover:bg-slate-500 transition-colors"
                              >
                                <a
                                  href={item.link}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="text-blue-400 hover:underline font-medium block mb-1"
                                >
                                  {item.title}
                                </a>
                                <p className="text-sm text-gray-300">
                                  {item.snippet}
                                </p>
                                <p className="text-xs text-gray-400 mt-1">
                                  {item.source}
                                </p>
                              </li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>
            ) : null}
          </div>
        </div>
      </>
    );
  };
  
  export default Sidebar;
  