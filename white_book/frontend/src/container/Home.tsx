import { useState, useRef, useEffect } from 'react';
import { HiMenu } from 'react-icons/hi';
import { AiFillCloseCircle } from 'react-icons/ai';
import { TiCamera } from 'react-icons/ti';
import { IconContext } from 'react-icons/lib';
import { Link, Route, Routes, useNavigate } from 'react-router-dom';

import { Sidebar, UserProfile } from '../components';
import Pins from './Pins';
import { userQuery, fetchUser } from '../utils/queries';
import { User } from '../utils/interfaces';
import { client } from '../client';

const Home = () => {
  const navigate = useNavigate();

  const userInfo = fetchUser();

  const [toggleSidebar, setToggleSidebar] = useState(false);
  const [user, setUser] = useState<User | null>(null);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!userInfo) {
      navigate('login');
      return;
    }

    const query = userQuery(userInfo._id);
    client.fetch(query).then((data: [User]) => {
      setUser(data[0]);
    });
  }, []);

  useEffect(() => {
    scrollRef.current?.scrollTo(0, 0);
  }, []);

  return (
    <div className="flex bg-gray-50 md:flex-row flex-col h-screen transaction-height duration-75 ease-out">
      <div className="hidden md:flex h-screen flex-initial">
        <Sidebar user={user} />
      </div>
      <div className="flex md:hidden flex-row">
        <div className="p-2 w-full flex flex-row justify-between items-center shadow-md">
          <HiMenu
            fontSize={40}
            className="cursor-pointer"
            onClick={() => setToggleSidebar(true)}
          />
          <Link to="/">
            <div className="flex justify-center items-center">
              <IconContext.Provider value={{ color: 'black', size: '50' }}>
                <TiCamera />
              </IconContext.Provider>
              <h1 className="font-bold text-[24px] pt-1 pl-2">WHITE BOOK</h1>
            </div>
          </Link>
          <Link to={`user-profile/${user?._id}`}>
            <img src={user?.image} alt="userImage" className="w-28" />
          </Link>
        </div>
        {toggleSidebar && (
          <div className="fixed w-4/5 bg-white h-screen overflow-y-auto shadow-md z-10 animate-slide-in">
            <div className="absolute w-full flex justify-end items-center p-2">
              <AiFillCloseCircle
                fontSize={30}
                className="cursor-pointer"
                onClick={() => setToggleSidebar(false)}
              />
            </div>
            <Sidebar user={user} closeToggle={setToggleSidebar} />
          </div>
        )}
      </div>
      <div className="pb-2 flex-1 h-screnn overflow-y-scroll" ref={scrollRef}>
        <Routes>
          <Route path="/user-profile/:userId" element={<UserProfile />} />
          <Route path="/*" element={<Pins user={user} />} />
        </Routes>
      </div>
    </div>
  );
};

export default Home;
