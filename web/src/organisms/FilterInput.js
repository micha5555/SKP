import React, { useState } from "react";
import Button from "../atoms/Button";
import InputLabel from "../molecules/InputLabel";

import './css/filterInput.css';

const FilterInput = () => {
  const [page, setPage] = useState(1);
  const [onPage, setOnPage] = useState(10);

  const filtr = () => {
    console.log('Not implemented')
  }

  return <div
    className="filterInput"
  >
    <InputLabel labelValue={"Strona"} inputValue={page} setInputValue={setPage} placeholder={"Wprowadź stronę"} />
    <InputLabel labelValue={"Ile na stone"} inputValue={onPage} setInputValue={setOnPage} placeholder={"Wprowadź ile na strone"}/>
    <Button text={"Filtruj"} click={filtr} />
  </div>
}

export default FilterInput;