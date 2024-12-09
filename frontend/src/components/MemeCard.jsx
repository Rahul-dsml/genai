import { useState } from "react";
import { FaRegCopy } from "react-icons/fa";
import { IoMdDownload } from "react-icons/io";
import { FaRepeat } from "react-icons/fa6";

const MemeCard = ({ memeUrl, initialMessage }) => {
  const [message, setMessage] = useState(initialMessage);
  const [isEditing, setIsEditing] = useState(false);

  const handleEdit = () => setIsEditing(true);
  const handleBlur = (e) => {
    setMessage(e.target.innerText);
    setIsEditing(false);
  };

  return (
    <div className="bg-gradient-to-r w-full from-gray-800 to-gray-900 backdrop-blur-md text-white p-4 rounded-xl shadow-lg space-y-4">
      {/* Meme Image */}
      <img
        src={memeUrl}
        alt={message}
        className="w-full h-auto rounded-lg object-cover"
      />

      {/* Meme Title/Message */}
      <div
        contentEditable={isEditing}
        suppressContentEditableWarning={true}
        onClick={handleEdit}
        onBlur={handleBlur}
        className="mt-2 text-sm cursor-pointer p-2 border border-transparent hover:border-gray-500 rounded focus:outline-none"
      >
        {message}
      </div>

      {/* Action Buttons */}
      <div className="sharebuttons flex items-center justify-end px-2 gap-2 mt-4">
        {/* Regenerate Button */}

        {/* Download Button */}
        <a
          href={memeUrl}
          target="_blank"
          rel="noopener noreferrer"
          download="meme.jpg"
          className="text-xs"
          title="Download Meme"
        >
          <IoMdDownload className="text-sm hover:text-cyan-400 hover:translate-y-[2px] transition-all ease-in" />
        </a>

        {/* Copy to Clipboard */}
        <button
          className="text-xs"
          onClick={() => navigator.clipboard.writeText(message)}
          title="Copy Title"
        >
          <FaRegCopy className="text-sm hover:text-cyan-400 hover:translate-y-[2px] transition-all ease-in" />
        </button>
      </div>
    </div>
  );
};

export default MemeCard;
