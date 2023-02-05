import React from "react";

import Cell from "../atomes/Cell";

function TableRow({
  rowContent, rowType,
}) {
  const cells = rowContent.map(cell => <Cell type={rowType} text={cell}/>);

  return <div
    className="tableRow"
    onClick={() => {console.log('jeszcze nie zaimplementowane')}}
  >
    {cells}
  </div>;
}