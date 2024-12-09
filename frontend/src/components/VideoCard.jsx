import { useState } from "react";
import { FaRepeat } from "react-icons/fa6";
import { IoMdDownload } from "react-icons/io";
import { FaRegCopy } from "react-icons/fa6";

const VideoCard = ({ videoUrl, initialMessage, onRegenerate }) => {
  const [message, setMessage] = useState(initialMessage);
  const [isEditing, setIsEditing] = useState(false);

  const handleEdit = () => setIsEditing(true);
  const handleBlur = (e) => {
    setMessage(e.target.innerText);
    setIsEditing(false);
  };

  return (
    <div className="bg-gradient-to-r from-white/5 to-white/10 backdrop-blur-md text-white p-4 rounded-xl shadow-lg space-y-4">
      <video controls className="w-full h-auto rounded-lg">
        <source src={videoUrl} type="video/mp4" />
        Your browser does not support the video tag.
      </video>

      <div
        contentEditable={isEditing}
        suppressContentEditableWarning={true}
        onClick={handleEdit}
        onBlur={handleBlur}
        className="mt-2 text-sm cursor-pointer p-2 border border-transparent hover:border-gray-500 rounded"
      >
        {message}
      </div>

      <div className=" sharebuttons flex items-center justify-end px-2 gap-2 mt-4  ">
        <button className="text-xs" onClick={onRegenerate}>
          <FaRepeat className="text-sm hover:text-cyan-400 hover:translate-y-[2px] transition-all ease-in" />
        </button>
        <a
          href={videoUrl}
          target="_blank"
          download="image.jpg"
          className="text-xs"
        >
          <IoMdDownload className="text-sm hover:text-cyan-400 hover:translate-y-[2px] transition-all ease-in" />
        </a>
        <button
          className="text-xs"
          onClick={() => navigator.clipboard.writeText(message)}
        >
          <FaRegCopy className="text-sm hover:text-cyan-400 hover:translate-y-[2px] transition-all ease-in" />
        </button>
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

export default VideoCard;