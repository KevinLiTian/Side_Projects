import { useNavigate } from 'react-router-dom';
import { GoogleLogin, googleLogout } from '@react-oauth/google';
import { IconContext } from 'react-icons/lib';
import { TiCamera } from 'react-icons/ti';
import jwt_decode from 'jwt-decode';

import { client } from '../client';
import { DecodedResponse } from '../utils';
import shareVideo from '../assets/share.mp4';

const Login = () => {
  const navigate = useNavigate();

  const createOrGetUser = async (response: any) => {
    const decoded: DecodedResponse = jwt_decode(response.credential);
    const { name, picture, sub } = decoded;

    const user = {
      _id: sub,
      _type: 'user',
      userName: name,
      image: picture,
    };

    localStorage.setItem('user', JSON.stringify(user));
    client.createIfNotExists(user).then(() => {
      navigate('/', { replace: true });
    });
  };

  return (
    <div className="flex justify-start items-center flex-col h-screen">
      <div className="relative w-full h-full">
        <video
          src={shareVideo}
          itemType="video/mp4"
          loop
          controls={false}
          muted
          autoPlay
          className="w-full h-full object-cover"
        />
        <div className="absolute flex flex-col justify-center items-center top-0 right-0 left-0 bottom-0 bg-blackOverlay">
          <div className="flex justify-center items-center p-5">
            <IconContext.Provider value={{ color: 'white', size: '70' }}>
              <TiCamera />
            </IconContext.Provider>
            <h1 className="text-white font-bold text-[28px] pt-1 pl-2">
              WHITE BOOK
            </h1>
          </div>
          <GoogleLogin
            onSuccess={(response) => {
              createOrGetUser(response);
            }}
            onError={() => console.log('error')}
          />
        </div>
      </div>
    </div>
  );
};

export default Login;
