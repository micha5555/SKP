import React from "react";
import Button, {LOUG} from "../atoms/Button";

import './css/card.css';

const Card = ({
  content,
  onSave,
  onCanel,
}) => {
  return <div
    className="card"
  >
    <div
      className="content"
    >
      {content}
    </div>
    <div
      className="buttonContainer"
    >
      <Button text='Anuluj' type={LOUG} click={onCanel}/>
      <Button text='Zatwierdz' click={onSave}/>
    </div>
  </div>
}

export default Card;