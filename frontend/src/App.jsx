import { useEffect, useState } from "react";
import axios from "axios";
import Header from "./components/Header";

function App(){
  return(
    <div style={{background:"#000", color:"#fff", minHeight:"100vh", display:"flex", flexDirection:"column"}}>
        <Header/>
    </div>
  );
}

export default App;