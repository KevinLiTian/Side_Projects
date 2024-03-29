import Masonry from 'react-masonry-css';

import Pin from './Pin';
import { Pin as typePin } from '../utils/interfaces';

const breakpointObj = {
  default: 4,
  3000: 6,
  2000: 5,
  1200: 3,
  1000: 2,
  500: 1,
};

interface MasonryLayoutProps {
  pins: typePin[];
}

const MasonryLayout = ({ pins }: MasonryLayoutProps) => {
  return (
    <Masonry className="flex animate-slide-fwd" breakpointCols={breakpointObj}>
      {pins.map((pin) => (
        <Pin key={pin._id} pin={pin} />
      ))}
    </Masonry>
  );
};

export default MasonryLayout;
