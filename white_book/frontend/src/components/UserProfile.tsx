import { useState, useEffect } from 'react';
import { AiOutlineLogout } from 'react-icons/ai';
import { useParams, useNavigate } from 'react-router-dom';
import { googleLogout } from '@react-oauth/google';

import {
  userCreatedPinsQuery,
  userQuery,
  userSavedPinsQuery,
} from '../utils/queries';
import { client } from '../client';
import MasonryLayout from './MasonryLayout';
import Spinner from './Spinner';
import { Pin, User } from '../utils/interfaces';

const randomImage =
  'https://source.unsplash.com/1600x900/?nature,photography,technology';

const activeBtnStyles =
  'bg-red-500 text-white font-bold p-2 rounded-full w-20 outline-none';
const notActiveBtnStyles =
  'bg-primary mr-4 text-black font-bold p-2 rounded-full w-20 outline-none';

const UserProfile = () => {
  const [user, setUser] = useState<User | null>(null);
  const [pins, setPins] = useState<[Pin] | null>(null);
  const [text, setText] = useState('Created');
  const [activeBtn, setActiveBtn] = useState('created');

  const navigate = useNavigate();
  const { userId } = useParams();

  useEffect(() => {
    const query = userQuery(userId!);
    client.fetch(query).then((data: [User]) => [setUser(data[0])]);
  }, [userId]);

  useEffect(() => {
    if (text === 'Created') {
      const createdPinsQuery = userCreatedPinsQuery(userId!);
      client.fetch(createdPinsQuery).then((data: [Pin]) => {
        setPins(data);
      });
    } else {
      const savedPinsQuery = userSavedPinsQuery(userId!);
      client.fetch(savedPinsQuery).then((data: [Pin]) => {
        setPins(data);
      });
    }
  }, [text, userId]);

  if (!user) return <Spinner message="Loading profile..." />;

  return (
    <div className="relative pb-2 h-full justify-center items-center">
      <div className="flex flex-col pb-5">
        <div className="relative flex flex-col mb-7">
          <div className="flex flex-col justify-center items-center">
            <img
              src={randomImage}
              alt="banner-pic"
              className="w-full h-370 2xl:h-510 shadow-lg object-cover"
            />
            <img
              src={user.image}
              alt="user-pic"
              className="rounded-full w-20 h-20 -mt-10 shadow-xl object-cover"
            />
            <h1 className="font-bold text-3xl text-center mt-3">
              {user.userName}
            </h1>
            <div className="absolute top-0 z-1 right-0 p-2">
              {userId === user._id && (
                <button
                  className="p-2 rounded-full bg-white opacity-70 hover:opacity-100"
                  onClick={() => {
                    googleLogout();
                    localStorage.clear();
                    navigate('/login');
                  }}
                >
                  <AiOutlineLogout color="red" fontSize={25} />
                </button>
              )}
            </div>
          </div>
          <div className="text-center mb-7">
            <button
              type="button"
              onClick={(e) => {
                const { textContent } = e.target as HTMLButtonElement;
                setText(textContent!);
                setActiveBtn('created');
              }}
              className={`${
                activeBtn === 'created' ? activeBtnStyles : notActiveBtnStyles
              }`}
            >
              Created
            </button>
            <button
              type="button"
              onClick={(e) => {
                const { textContent } = e.target as HTMLButtonElement;
                setText(textContent!);
                setActiveBtn('saved');
              }}
              className={`${
                activeBtn === 'saved' ? activeBtnStyles : notActiveBtnStyles
              }`}
            >
              Saved
            </button>
          </div>

          {pins ? (
            <div className="px-2">
              <MasonryLayout pins={pins} />
            </div>
          ) : (
            <Spinner message="Loading the pins..." />
          )}
        </div>
      </div>
    </div>
  );
};

export default UserProfile;
