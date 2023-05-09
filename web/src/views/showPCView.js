import React from "react";
import FilterInput from "../organisms/FilterInput";
import Table from "../organisms/Table";

import './css/showPCView.css';

const ShowPCView = () => {
  return <div
    className="showPCView"
  >
    <FilterInput />
    <Table />
  </div>
}

export default ShowPCView;