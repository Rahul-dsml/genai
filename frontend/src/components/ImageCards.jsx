import { useState } from "react";
import { FaRegCopy } from "react-icons/fa";
import { IoMdDownload } from "react-icons/io";
import { FaRepeat } from "react-icons/fa6";

const ImageCard = ({ imageUrl }) => {
 

  return (
    <div className="bg-gradient-to-r w-full from-white/5 to-white/10 backdrop-blur-md text-white p-4 rounded-xl shadow-lg space-y-4">
      <img src={imageUrl} alt="Image" className="w-full h-auto rounded-lg" />



      <div className=" sharebuttons flex items-center justify-end px-2 gap-2 mt-4  ">
       
        <a
          href={imageUrl}
          target="_blank"
          download="image.jpg"
          className="text-xs"
        >
          <IoMdDownload className="text-sm hover:text-cyan-400 hover:translate-y-[2px] transition-all ease-in" />
        </a>
       
        {/* <button
          className="text-xs "
          onClick={() => alert("Share functionality coming soon!")}
        >
          Share
        </button> */}
      </div>
    </div>
  );
};
export default ImageCard;
