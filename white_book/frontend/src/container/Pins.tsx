import React from 'react';
import { User } from '../utils';

interface PinsProps {
  user: User | boolean | null;
}

const Pins = ({ user }: PinsProps) => {
  return <div>Pins</div>;
};

export default Pins;
