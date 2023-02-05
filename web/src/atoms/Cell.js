import React from "react";

export const TITLE = 'title';
export const NR1 = 'nr1';
export const NR2 = 'nr2';

const Cell = ({type = NR1, text = ''}) => {
  return <div
    className={`cell ${type}`}
  >
    <span>{text}</span>
  </div>
}