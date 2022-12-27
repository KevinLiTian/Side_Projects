import React from 'react';
import { Circles } from 'react-loader-spinner';

interface SpinnerProps {
  message: string;
}

const Spinner = ({ message }: SpinnerProps) => {
  return (
    <div className="flex flex-col justify-center items-center w-full h-full">
      <Circles
        height="50"
        width="200"
        color="#00BFFF"
        ariaLabel="circles-loading"
        visible={true}
        wrapperClass="m-5"
      />
      <p className="text-lg text-center px-2">{message}</p>
    </div>
  );
};

export default Spinner;
