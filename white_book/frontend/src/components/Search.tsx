import { useState, useEffect } from 'react';

import MasonryLayout from './MasonryLayout';
import { client } from '../client';
import { feedQuery, searchQuery } from '../utils/queries';
import Spinner from './Spinner';
import { Pin } from '../utils/interfaces';

interface SearchProps {
  searchTerm: string;
}

const Search = ({ searchTerm }: SearchProps) => {
  const [pins, setPins] = useState<Pin[] | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (searchTerm) {
      setLoading(true);
      const query = searchQuery(searchTerm.toLowerCase());
      client.fetch(query).then((data: Pin[]) => {
        setPins(data);
        setLoading(false);
      });
    } else {
      client.fetch(feedQuery).then((data: Pin[]) => {
        setPins(data);
        setLoading(false);
      });
    }
  }, [searchTerm]);

  return (
    <div>
      {loading && <Spinner message="Searching for pins" />}
      {pins && pins.length !== 0 && <MasonryLayout pins={pins} />}
      {pins && pins.length === 0 && searchTerm !== '' && !loading && (
        <div className="mt-10 text-center text-xl">No pins found</div>
      )}
    </div>
  );
};

export default Search;
