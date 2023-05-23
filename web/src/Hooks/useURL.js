import { useState, useEffect } from 'react';

const useURL = () => {
  const [url, setURL] = useState('');

  useEffect(() => {
    const currentURL = window.location.href;
    setURL(currentURL);
  }, []);

  return url;
};

export default useURL;
