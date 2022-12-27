import React, { SetStateAction } from 'react';

import { User } from '../utils';

interface SidebarProps {
  user: User | boolean | null;
  closeToggle?: React.Dispatch<SetStateAction<boolean>>;
}

const Sidebar = ({ user, closeToggle }: SidebarProps) => {
  return <div>Sidebar</div>;
};

export default Sidebar;
