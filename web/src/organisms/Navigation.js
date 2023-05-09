import React from "react";
import NavElem from '../atoms/NavElem';

import './css/navigation.css';

const Navigation = () => {
  const names = [
    'Problematyczne przypadki',
    'Raporty',
    'Użytkownicy',
  ];

  const elems = names.map(name => <NavElem key={name} text={name} />)
  
  return <div
    className="navigation"
  >
    {elems}
  </div>
}

export default Navigation;