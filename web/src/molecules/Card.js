import React from "react";

import Button, {LOUG} from "../atoms/Button";

const Card = ({
  content,
  onSave,
  onCanel,
}) => {
  return <div
    className="card"
  >
    <div>
      {content}
    </div>
    <Button text='Anuluj' type={LOUG} click={onCanel}/>
    <Button text='Zatwierdz' click={onSave}/>
  </div>
}