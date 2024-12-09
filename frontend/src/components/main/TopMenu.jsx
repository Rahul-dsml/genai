import React, { useState } from "react";
import { NavLink } from "react-router-dom";
const TopMenu = () => {
  const navLinks = [
    {
      name: 'Home',
      link: '/'
    },
    {
      name: 'Text',
      link: '/text'
    },
    {
      name: 'Images',
      link: '/images'
    },
    {
      name: 'Memes',
      link: '/memes'
    },
    {
      name: 'Videos',
      link: '/videos'
    },
  ]
  return (
    <div className="top-main-menu text-white flex w-full ">
      <p className="text-xl md:text-3xl">MetaMindAI</p>
      <div className="postFormats md:w-72 p-1 md:p-2 ml-20 md:mx-auto translate-x-[-3rem] lg:translate-x-[-6rem] gap-2 rounded-md md:rounded-full flex justify-between mt-4 z-10 relative ">
      {navLinks.map((link, index) => (
          <NavLink
            key={index}
            to={link.link}
            className={({ isActive }) =>
              `transition-all ease-in cursor-pointer text-white p-2 lg:p-4 text-base lg:text-xl rounded-3xl px-4 lg:px-6 hover:backdrop-blur-md ${
                isActive
                  ? 'bg-gradient-to-r from-white/5 to-white/10' // Active styles
                  : 'hover:bg-gradient-to-r hover:from-white/5 hover:to-white/10'
              }`
            }
          >
            {link.name}
          </NavLink>
        ))}
      </div>
    </div>
  );
};

export default TopMenu;
