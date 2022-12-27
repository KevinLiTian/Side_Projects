import React, { SetStateAction } from 'react';

interface SearchProps {
  searchTerm: string;
  setSearchTerm: React.Dispatch<SetStateAction<string>>;
}

const Search = ({ searchTerm, setSearchTerm }: SearchProps) => {
  return <div>Search</div>;
};

export default Search;
